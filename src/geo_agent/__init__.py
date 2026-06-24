"""GEO Agent domain model package."""

from .entity_profile import (
    EntityProfile,
    EntityProfileValidationError,
    ValidationIssue,
    validate_entity_profile,
)
from .evidence_store import EvidenceStore
from .query_space import INTENT_TYPES, QueryRecord, build_query_space

__all__ = [
    "EntityProfile",
    "EntityProfileValidationError",
    "ValidationIssue",
    "validate_entity_profile",
    "EvidenceStore",
    "INTENT_TYPES",
    "QueryRecord",
    "build_query_space",
]
