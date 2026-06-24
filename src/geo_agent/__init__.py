"""GEO Agent domain model package."""

from .audit_runner import AuditArtifacts, AuditRunner
from .entity_profile import (
    EntityProfile,
    EntityProfileValidationError,
    ValidationIssue,
    validate_entity_profile,
)
from .evidence_store import EvidenceStore, ReportArtifact
from .failure_debugger import FailureDiagnosis, diagnose_failure_v2
from .query_space import INTENT_TYPES, QueryRecord, build_query_space
from .recorded_dataset import (
    RecordedAuditDataset,
    RecordedDatasetError,
    load_recorded_dataset,
    load_recorded_dataset_from_mapping,
)

__all__ = [
    "AuditArtifacts",
    "AuditRunner",
    "EntityProfile",
    "EntityProfileValidationError",
    "ValidationIssue",
    "validate_entity_profile",
    "EvidenceStore",
    "ReportArtifact",
    "FailureDiagnosis",
    "diagnose_failure_v2",
    "INTENT_TYPES",
    "QueryRecord",
    "build_query_space",
    "RecordedAuditDataset",
    "RecordedDatasetError",
    "load_recorded_dataset",
    "load_recorded_dataset_from_mapping",
]
