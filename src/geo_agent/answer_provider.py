"""Answer provider adapters for configured GEO Agent answer engines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from .engine_sampling import EngineRun, run_from_payload
from .provider_access import ApiKeySessionStore, ProviderAccessError, redact_credential_label

CredentialAccessMethod = Literal["api_key", "platform_managed"]


class HttpClient(Protocol):
    def post(self, url: str, *, headers: dict[str, str], json: dict[str, object]) -> dict[str, object]:
        ...


@dataclass(frozen=True)
class AnswerProviderConfig:
    provider_id: str = "openai_compatible"
    model: str = "gpt-4o-mini"
    endpoint_url: str = "https://api.openai.com/v1/chat/completions"
    temperature: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "model": self.model,
            "endpoint_url": self.endpoint_url,
            "temperature": self.temperature,
        }


@dataclass(frozen=True)
class AnswerCredentialRef:
    access_method: CredentialAccessMethod
    session_id: str | None = None
    platform_api_key: str | None = None

    def resolve_api_key(self, session_store: ApiKeySessionStore) -> str:
        if self.access_method == "api_key":
            if not self.session_id:
                raise ProviderAccessError("API key session id is required for OpenAI-compatible provider access.")
            return session_store.get_key(self.session_id)
        if self.access_method == "platform_managed":
            if not self.platform_api_key or not self.platform_api_key.strip():
                raise ProviderAccessError("Platform-managed API key is required for OpenAI-compatible provider access.")
            return self.platform_api_key
        raise ProviderAccessError(f"Unsupported answer provider access method: {self.access_method}")

    def to_dict(self) -> dict[str, str]:
        payload = {"access_method": self.access_method}
        if self.session_id:
            payload["session_id"] = self.session_id
        if self.platform_api_key:
            payload["redacted_label"] = redact_credential_label(self.platform_api_key)
        return payload


@dataclass(frozen=True)
class AnswerProviderRequest:
    query: str
    region: str
    language: str
    config: AnswerProviderConfig
    credential_ref: AnswerCredentialRef

    def to_dict(self) -> dict[str, object]:
        return {
            "query": self.query,
            "region": self.region,
            "language": self.language,
            "config": self.config.to_dict(),
            "credential_ref": self.credential_ref.to_dict(),
        }


class OpenAICompatibleAnswerProvider:
    """OpenAI-compatible answer provider with injectable HTTP transport.

    The adapter never performs default live calls in CI. Tests inject a fake HTTP
    client. Production callers must provide explicit credential references.
    """

    engine = "openai_compatible"

    def __init__(self, *, http_client: HttpClient, session_store: ApiKeySessionStore | None = None) -> None:
        self.http_client = http_client
        self.session_store = session_store or ApiKeySessionStore()

    def sample(self, request: AnswerProviderRequest, *, timestamp: str | None = None) -> EngineRun:
        if not request.query.strip():
            raise ProviderAccessError("Query text is required for answer provider sampling.")
        api_key = request.credential_ref.resolve_api_key(self.session_store)
        response = self.http_client.post(
            request.config.endpoint_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": request.config.model,
                "temperature": request.config.temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": request.query,
                    }
                ],
                "metadata": {
                    "geo_agent_region": request.region,
                    "geo_agent_language": request.language,
                },
            },
        )
        payload = _payload_from_openai_response(response)
        return run_from_payload(
            payload,
            engine=request.config.provider_id,
            query=request.query,
            region=request.region,
            language=request.language,
            timestamp=timestamp,
        )


def _payload_from_openai_response(response: dict[str, object]) -> dict[str, object]:
    if "error" in response:
        raise ProviderAccessError(_error_message(response["error"]))
    content = _message_content(response)
    metadata = response.get("geo")
    if not isinstance(metadata, dict):
        metadata = {}
    return {
        "raw_answer": content,
        "citations": _string_list(metadata.get("citations")),
        "mentions": _string_list(metadata.get("mentions")),
        "recommendations": _string_list(metadata.get("recommendations")),
        "timestamp": response.get("created_at", ""),
    }


def _message_content(response: dict[str, object]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ProviderAccessError("OpenAI-compatible response did not include answer choices.")
    first = choices[0]
    if not isinstance(first, dict):
        raise ProviderAccessError("OpenAI-compatible response choice is malformed.")
    message = first.get("message")
    if not isinstance(message, dict):
        raise ProviderAccessError("OpenAI-compatible response choice did not include a message.")
    content = message.get("content")
    if not isinstance(content, str):
        raise ProviderAccessError("OpenAI-compatible response message did not include text content.")
    return content


def _string_list(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ProviderAccessError("OpenAI-compatible GEO metadata lists must be arrays.")
    return tuple(str(item) for item in value)


def _error_message(error: object) -> str:
    if isinstance(error, dict) and isinstance(error.get("message"), str):
        return error["message"]
    return "OpenAI-compatible provider returned an error."