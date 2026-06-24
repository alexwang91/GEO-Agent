"""GEO Agent domain model package."""

from .entity_profile import (
    EntityProfile,
    EntityProfileValidationError,
    ValidationIssue,
    validate_entity_profile,
)
from .query_space import INTENT_TYPES, QueryRecord, build_query_space

__all__ = [
    "EntityProfile",
    "EntityProfileValidationError",
    "ValidationIssue",
    "validate_entity_profile",
    "INTENT_TYPES",
    "QueryRecord",
    "build_query_space",
]
