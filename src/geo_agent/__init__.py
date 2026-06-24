"""GEO Agent domain model package."""

from .entity_profile import (
    EntityProfile,
    EntityProfileValidationError,
    ValidationIssue,
    validate_entity_profile,
)

__all__ = [
    "EntityProfile",
    "EntityProfileValidationError",
    "ValidationIssue",
    "validate_entity_profile",
]
