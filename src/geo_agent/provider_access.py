"""Provider access domain model and registry for GEO Agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ProviderType = Literal["answer", "search", "crawl", "model", "analytics"]
ProviderCapability = Literal["answer", "search", "crawl", "model", "analytics", "manual_import"]
ProviderAccessMethod = Literal["api_key", "oauth", "platform_managed", "manual_import", "local"]
ProviderStatus = Literal["implemented", "planned"]
AuthStatus = Literal["connected", "missing_credential", "planned", "disconnected"]


class ProviderAccessError(ValueError):
    pass


@dataclass(frozen=True)
class ProviderDefinition:
    provider_id: str
    display_name: str
    provider_type: ProviderType
    capabilities: tuple[ProviderCapability, ...]
    access_methods: tuple[ProviderAccessMethod, ...]
    implementation_status: ProviderStatus

    def supports(self, method: ProviderAccessMethod) -> bool:
        return method in self.access_methods

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "display_name": self.display_name,
            "provider_type": self.provider_type,
            "capabilities": list(self.capabilities),
            "access_methods": list(self.access_methods),
            "implementation_status": self.implementation_status,
        }


@dataclass(frozen=True)
class ProviderConnection:
    provider_id: str
    access_method: ProviderAccessMethod
    auth_status: AuthStatus
    redacted_label: str
    scopes: tuple[str, ...] = ()
    expires_at: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "access_method": self.access_method,
            "auth_status": self.auth_status,
            "redacted_label": self.redacted_label,
            "scopes": list(self.scopes),
            "expires_at": self.expires_at,
        }


class ProviderRegistry:
    def __init__(self, definitions: tuple[ProviderDefinition, ...] = ()) -> None:
        self._definitions = {definition.provider_id: definition for definition in definitions}

    def list_definitions(self) -> tuple[ProviderDefinition, ...]:
        return tuple(self._definitions.values())

    def get(self, provider_id: str) -> ProviderDefinition:
        try:
            return self._definitions[provider_id]
        except KeyError as exc:
            raise ProviderAccessError(f"Unknown provider: {provider_id}") from exc

    def connect(self, provider_id: str, access_method: ProviderAccessMethod, *, credential_label: str | None = None, scopes: tuple[str, ...] = (), expires_at: str | None = None) -> ProviderConnection:
        definition = self.get(provider_id)
        if not definition.supports(access_method):
            raise ProviderAccessError(f"Provider {provider_id} does not support access method: {access_method}")
        if definition.implementation_status == "planned":
            return ProviderConnection(provider_id, access_method, "planned", "planned", scopes, expires_at)
        if access_method in {"api_key", "oauth"} and not credential_label:
            raise ProviderAccessError(f"Provider {provider_id} requires a credential label for {access_method}")
        return ProviderConnection(provider_id, access_method, "connected", redact_credential_label(credential_label or access_method), scopes, expires_at)


def default_provider_registry() -> ProviderRegistry:
    return ProviderRegistry((
        ProviderDefinition("openai_compatible", "OpenAI-compatible", "answer", ("answer", "model"), ("api_key", "platform_managed"), "planned"),
        ProviderDefinition("perplexity", "Perplexity", "answer", ("answer", "search"), ("api_key",), "planned"),
        ProviderDefinition("gemini", "Gemini", "answer", ("answer", "model"), ("api_key",), "planned"),
        ProviderDefinition("crawl4ai", "Crawl4AI", "crawl", ("crawl",), ("local", "platform_managed"), "planned"),
        ProviderDefinition("firecrawl", "Firecrawl", "crawl", ("crawl",), ("api_key",), "planned"),
        ProviderDefinition("google_search_console", "Google Search Console", "analytics", ("analytics", "search"), ("oauth",), "planned"),
        ProviderDefinition("manual_import", "Manual Import", "answer", ("answer", "manual_import"), ("manual_import",), "implemented"),
    ))


def redact_credential_label(label: str) -> str:
    if not label:
        return "redacted"
    if len(label) <= 4:
        return "****"
    return f"{label[:2]}…{label[-2:]}"
