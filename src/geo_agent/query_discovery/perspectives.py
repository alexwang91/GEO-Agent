"""Perspective definitions for deterministic query discovery."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QueryPerspective:
    perspective_id: str
    label: str
    user_role: str
    prompt_angle: str

    def to_dict(self) -> dict[str, str]:
        return {
            "perspective_id": self.perspective_id,
            "label": self.label,
            "user_role": self.user_role,
            "prompt_angle": self.prompt_angle,
        }


DEFAULT_PERSPECTIVES: tuple[QueryPerspective, ...] = (
    QueryPerspective("buyer", "Economic buyer", "budget owner", "shortlist and purchase confidence"),
    QueryPerspective("operator", "Operator", "daily user", "workflow fit and practical limitations"),
    QueryPerspective("technical", "Technical evaluator", "engineering or data owner", "integration, evidence, and security"),
    QueryPerspective("pr", "Communications owner", "PR or brand owner", "third-party sources and reputation risk"),
)
