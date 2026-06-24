"""Fake provider authorization flow boundary for GEO Agent.

This module intentionally does not call live OAuth providers. It models the
state/callback/token-redaction contract used by provider authorization flows.
"""

from __future__ import annotations

from dataclasses import dataclass
from secrets import token_urlsafe
from urllib.parse import urlencode

from .provider_access import ProviderAccessError, ProviderRegistry, default_provider_registry, redact_credential_label


@dataclass(frozen=True)
class AuthorizationStart:
    provider_id: str
    state: str
    authorization_url: str

    def to_dict(self) -> dict[str, str]:
        return {
            "provider_id": self.provider_id,
            "state": self.state,
            "authorization_url": self.authorization_url,
        }


@dataclass(frozen=True)
class TokenSession:
    session_id: str
    provider_id: str
    redacted_label: str
    scopes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "provider_id": self.provider_id,
            "redacted_label": self.redacted_label,
            "scopes": list(self.scopes),
        }


class FakeAuthorizationProvider:
    """Deterministic fake authorization provider for CI and local tests."""

    def __init__(self, base_url: str = "https://fake-auth.local/authorize") -> None:
        self.base_url = base_url

    def authorization_url(self, *, provider_id: str, state: str, redirect_uri: str, scopes: tuple[str, ...]) -> str:
        return f"{self.base_url}?{urlencode({'provider': provider_id, 'state': state, 'redirect_uri': redirect_uri, 'scope': ' '.join(scopes)})}"

    def exchange_code(self, code: str) -> str:
        if not code or not code.strip():
            raise ProviderAccessError("Authorization code is required.")
        return f"fake-token-{code.strip()}"


class AuthorizationSessionStore:
    """In-memory provider authorization state and token boundary."""

    def __init__(self, registry: ProviderRegistry | None = None, auth_provider: FakeAuthorizationProvider | None = None) -> None:
        self.registry = registry or default_provider_registry()
        self.auth_provider = auth_provider or FakeAuthorizationProvider()
        self._pending: dict[str, tuple[str, tuple[str, ...]]] = {}
        self._tokens: dict[str, str] = {}
        self._sessions: dict[str, TokenSession] = {}

    def start(self, provider_id: str, *, redirect_uri: str, scopes: tuple[str, ...] = ()) -> AuthorizationStart:
        definition = self.registry.get(provider_id)
        if not definition.supports("oauth"):
            raise ProviderAccessError(f"Provider {provider_id} does not support authorization flow access.")
        state = token_urlsafe(16)
        self._pending[state] = (provider_id, scopes)
        return AuthorizationStart(
            provider_id=provider_id,
            state=state,
            authorization_url=self.auth_provider.authorization_url(
                provider_id=provider_id,
                state=state,
                redirect_uri=redirect_uri,
                scopes=scopes,
            ),
        )

    def callback(self, *, state: str, code: str) -> TokenSession:
        try:
            provider_id, scopes = self._pending.pop(state)
        except KeyError as exc:
            raise ProviderAccessError("Invalid authorization state.") from exc
        token = self.auth_provider.exchange_code(code)
        session_id = token_urlsafe(16)
        session = TokenSession(
            session_id=session_id,
            provider_id=provider_id,
            redacted_label=redact_credential_label(token),
            scopes=scopes,
        )
        self._tokens[session_id] = token
        self._sessions[session_id] = session
        return session

    def get_token(self, session_id: str) -> str:
        try:
            return self._tokens[session_id]
        except KeyError as exc:
            raise ProviderAccessError("Unknown authorization session.") from exc

    def get_session(self, session_id: str) -> TokenSession:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise ProviderAccessError("Unknown authorization session.") from exc

    def disconnect(self, session_id: str) -> None:
        self._tokens.pop(session_id, None)
        self._sessions.pop(session_id, None)
