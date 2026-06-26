import dataclasses
import unittest

from geo_agent.schema import AuditRun, PromptRecord, EngineSample, CitationRecord, MentionRecord, RecommendationRecord, PageSnapshot, ClaimRecord, DiagnosisRecord, OptimizationTask, RetestRecord, SkillOutcomeRecord


class EvidenceGraphSchemaTests(unittest.TestCase):
    def test_required_records_are_frozen_dataclasses(self):
        records = [AuditRun, PromptRecord, EngineSample, CitationRecord, MentionRecord, RecommendationRecord, PageSnapshot, ClaimRecord, DiagnosisRecord, OptimizationTask, RetestRecord, SkillOutcomeRecord]
        for record in records:
            self.assertTrue(dataclasses.is_dataclass(record), record.__name__)
            self.assertTrue(record.__dataclass_params__.frozen, record.__name__)


if __name__ == "__main__":
    unittest.main()
