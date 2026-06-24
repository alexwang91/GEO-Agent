"""Entity profile schema and validation for GEO Agent domain intake."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlparse


REQUIRED_FIELDS = (
    "brand",
    "aliases",
    "domain",
    "competitors",
    "target_regions",
    "target_languages",
    "target_customer",
    "main_product",
    "category",
    "business_goal",
)


@dataclass(frozen=True)
class ValidationIssue:
    """Actionable validation issue for one entity profile field."""

    field: str
    message: str
    expected: str
    received: str
    remediation: str


class EntityProfileValidationError(ValueError):
    """Raised when an entity profile cannot be validated."""

    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = issues
        details = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        super().__init__(f"Invalid entity profile: {details}")

    def to_dict(self) -> dict[str, list[dict[str, str]]]:
        return {"issues": [issue.__dict__.copy() for issue in self.issues]}


@dataclass(frozen=True)
class EntityProfile:
    """Normalized entity profile used by downstream GEO workflows."""

    brand: str
    aliases: tuple[str, ...]
    domain: str
    competitors: tuple[str, ...]
    target_regions: tuple[str, ...]
    target_languages: tuple[str, ...]
    target_customer: str
    main_product: str
    category: str
    business_goal: str

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "EntityProfile":
        """Validate and normalize a raw entity profile mapping."""

        return validate_entity_profile(payload)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable profile record."""

        return {
            "brand": self.brand,
            "aliases": list(self.aliases),
            "domain": self.domain,
            "competitors": list(self.competitors),
            "target_regions": list(self.target_regions),
            "target_languages": list(self.target_languages),
            "target_customer": self.target_customer,
            "main_product": self.main_product,
            "category": self.category,
            "business_goal": self.business_goal,
        }


def validate_entity_profile(payload: Mapping[str, Any]) -> EntityProfile:
    """Validate and normalize a domain intake profile.

    Missing or malformed required fields raise EntityProfileValidationError with
    field-level remediation guidance. The validator accepts only plain mappings
    so callers can pass decoded JSON, YAML, or form submissions without tying the
    schema to a transport layer.
    """

    issues: list[ValidationIssue] = []

    if not isinstance(payload, Mapping):
        raise EntityProfileValidationError(
            [
                ValidationIssue(
                    field="profile",
                    message="Profile must be an object with named fields.",
                    expected="mapping/object",
                    received=type(payload).__name__,
                    remediation="Pass a dictionary-like object containing all required intake fields.",
                )
            ]
        )

    for field in REQUIRED_FIELDS:
        if field not in payload:
            issues.append(
                ValidationIssue(
                    field=field,
                    message="Required field is missing.",
                    expected="present field",
                    received="missing",
                    remediation=f"Add `{field}` to the entity profile intake payload.",
                )
            )

    brand = _require_non_empty_string(payload, "brand", issues)
    aliases = _require_string_list(payload, "aliases", issues, allow_empty=True)
    domain = _require_domain(payload, "domain", issues)
    competitors = _require_string_list(payload, "competitors", issues, allow_empty=False)
    target_regions = _require_string_list(payload, "target_regions", issues, allow_empty=False)
    target_languages = _require_string_list(payload, "target_languages", issues, allow_empty=False)
    target_customer = _require_non_empty_string(payload, "target_customer", issues)
    main_product = _require_non_empty_string(payload, "main_product", issues)
    category = _require_non_empty_string(payload, "category", issues)
    business_goal = _require_non_empty_string(payload, "business_goal", issues)

    if issues:
        raise EntityProfileValidationError(issues)

    return EntityProfile(
        brand=brand,
        aliases=tuple(aliases),
        domain=domain,
        competitors=tuple(competitors),
        target_regions=tuple(target_regions),
        target_languages=tuple(target_languages),
        target_customer=target_customer,
        main_product=main_product,
        category=category,
        business_goal=business_goal,
    )


def _require_non_empty_string(
    payload: Mapping[str, Any], field: str, issues: list[ValidationIssue]
) -> str:
    value = payload.get(field)
    if isinstance(value, str) and value.strip():
        return value.strip()

    issues.append(
        ValidationIssue(
            field=field,
            message="Field must be a non-empty string.",
            expected="non-empty string",
            received=_describe_value(value),
            remediation=f"Set `{field}` to concise user-facing text.",
        )
    )
    return ""


def _require_string_list(
    payload: Mapping[str, Any], field: str, issues: list[ValidationIssue], *, allow_empty: bool
) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list):
        issues.append(
            ValidationIssue(
                field=field,
                message="Field must be a list of strings.",
                expected="list[str]",
                received=_describe_value(value),
                remediation=f"Set `{field}` to a JSON array of strings.",
            )
        )
        return []

    normalized: list[str] = []
    for index, item in enumerate(value):
        if isinstance(item, str) and item.strip():
            normalized.append(item.strip())
        else:
            issues.append(
                ValidationIssue(
                    field=f"{field}[{index}]",
                    message="List item must be a non-empty string.",
                    expected="non-empty string",
                    received=_describe_value(item),
                    remediation=f"Replace `{field}[{index}]` with a meaningful string value.",
                )
            )

    if not normalized and not allow_empty:
        issues.append(
            ValidationIssue(
                field=field,
                message="Field must contain at least one value.",
                expected="non-empty list[str]",
                received="empty list",
                remediation=f"Add at least one relevant value to `{field}`.",
            )
        )

    return normalized


def _require_domain(payload: Mapping[str, Any], field: str, issues: list[ValidationIssue]) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        issues.append(
            ValidationIssue(
                field=field,
                message="Domain must be a non-empty string.",
                expected="domain such as example.com or https://example.com",
                received=_describe_value(value),
                remediation="Set `domain` to the brand's canonical website host.",
            )
        )
        return ""

    candidate = value.strip()
    parsed = urlparse(candidate if "://" in candidate else f"https://{candidate}")
    hostname = parsed.hostname or ""
    if not hostname or "." not in hostname or any(char.isspace() for char in hostname):
        issues.append(
            ValidationIssue(
                field=field,
                message="Domain must include a valid host name.",
                expected="domain host with at least one dot",
                received=candidate,
                remediation="Use a canonical host such as `example.com`; omit paths, query strings, and marketing copy.",
            )
        )
        return ""

    return hostname.lower().removeprefix("www.")


def _describe_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, str):
        return "empty string" if not value.strip() else "string"
    if isinstance(value, list):
        return "list"
    return type(value).__name__
