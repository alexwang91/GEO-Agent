"""GEO Agent domain model package."""

from .answer_provider import (
    AnswerCredentialRef,
    AnswerProviderConfig,
    AnswerProviderRequest,
    OpenAICompatibleAnswerProvider,
)
from .audit_runner import AuditArtifacts, AuditRunner
from .crawl_provider import (
    CrawlProviderError,
    CrawlProviderRequest,
    CrawlProviderResult,
    StaticCrawlerProvider,
    pages_from_crawl_result,
)
from .entity_profile import (
    EntityProfile,
    EntityProfileValidationError,
    ValidationIssue,
    validate_entity_profile,
)
from .evidence_store import EvidenceStore, ReportArtifact
from .failure_debugger import FailureDiagnosis, diagnose_failure_v2
from .fixture_package import FixturePackageResult, run_fixture_package
from .manual_import import ManualImportError, ManualImportResult, validate_manual_import
from .provider_access import (
    ApiKeySession,
    ApiKeySessionStore,
    ProviderAccessError,
    ProviderConnection,
    ProviderDefinition,
    ProviderRegistry,
    default_provider_registry,
    redact_credential_label,
)
from .provider_auth_flow import (
    AuthorizationSessionStore,
    AuthorizationStart,
    FakeAuthorizationProvider,
    TokenSession,
)
from .provider_output_eval import (
    ProviderOutputEvalCase,
    ProviderOutputEvalResult,
    ProviderOutputEvalSummary,
    evaluate_provider_output_cases,
    provider_response_to_run,
)
from .query_space import INTENT_TYPES, QueryRecord, build_query_space
from .recorded_dataset import (
    RecordedAuditDataset,
    RecordedDatasetError,
    load_recorded_dataset,
    load_recorded_dataset_from_mapping,
)

__all__ = [
    "AnswerCredentialRef",
    "AnswerProviderConfig",
    "AnswerProviderRequest",
    "OpenAICompatibleAnswerProvider",
    "AuditArtifacts",
    "AuditRunner",
    "CrawlProviderError",
    "CrawlProviderRequest",
    "CrawlProviderResult",
    "StaticCrawlerProvider",
    "pages_from_crawl_result",
    "EntityProfile",
    "EntityProfileValidationError",
    "ValidationIssue",
    "validate_entity_profile",
    "EvidenceStore",
    "ReportArtifact",
    "FailureDiagnosis",
    "diagnose_failure_v2",
    "FixturePackageResult",
    "run_fixture_package",
    "ManualImportError",
    "ManualImportResult",
    "validate_manual_import",
    "ApiKeySession",
    "ApiKeySessionStore",
    "ProviderAccessError",
    "ProviderConnection",
    "ProviderDefinition",
    "ProviderRegistry",
    "default_provider_registry",
    "redact_credential_label",
    "AuthorizationSessionStore",
    "AuthorizationStart",
    "FakeAuthorizationProvider",
    "TokenSession",
    "ProviderOutputEvalCase",
    "ProviderOutputEvalResult",
    "ProviderOutputEvalSummary",
    "evaluate_provider_output_cases",
    "provider_response_to_run",
    "INTENT_TYPES",
    "QueryRecord",
    "build_query_space",
    "RecordedAuditDataset",
    "RecordedDatasetError",
    "load_recorded_dataset",
    "load_recorded_dataset_from_mapping",
]