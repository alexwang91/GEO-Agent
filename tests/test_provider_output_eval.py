import unittest

from geo_agent.provider_output_eval import ProviderOutputEvalCase, evaluate_provider_output_cases, provider_response_to_run


def response_with_geo(**geo):
    return {
        "created_at": "2026-06-25T00:00:00Z",
        "choices": [{"message": {"content": "Acme AI is useful for marketing teams."}}],
        "geo": geo,
    }


class ProviderOutputEvalTests(unittest.TestCase):
    def test_eval_passes_answer_with_citations_mentions_and_recommendations(self):
        case = ProviderOutputEvalCase(
            name="with-citations",
            response=response_with_geo(
                citations=["https://acme.ai/guide"],
                mentions=["Acme AI"],
                recommendations=["Acme AI"],
            ),
            expected_citations=("https://acme.ai/guide",),
            expected_mentions=("Acme AI",),
            expected_recommendations=("Acme AI",),
        )

        summary = evaluate_provider_output_cases((case,))

        self.assertTrue(summary.passed)
        self.assertEqual(summary.passed_count, 1)
        self.assertEqual(summary.failed_count, 0)

    def test_eval_handles_answer_without_citations(self):
        case = ProviderOutputEvalCase(
            name="no-citations",
            response=response_with_geo(citations=[], mentions=["Acme AI"], recommendations=[]),
            expected_citations=(),
            expected_mentions=("Acme AI",),
            expected_recommendations=(),
        )

        run = provider_response_to_run(case)
        summary = evaluate_provider_output_cases((case,))

        self.assertEqual(run.citations, ())
        self.assertTrue(summary.passed)

    def test_eval_preserves_duplicate_citation_domains_for_regression_visibility(self):
        case = ProviderOutputEvalCase(
            name="duplicate-domains",
            response=response_with_geo(
                citations=["https://acme.ai/a", "https://acme.ai/b"],
                mentions=["Acme AI"],
                recommendations=["Acme AI"],
            ),
            expected_citations=("https://acme.ai/a", "https://acme.ai/b"),
            expected_mentions=("Acme AI",),
            expected_recommendations=("Acme AI",),
        )

        run = provider_response_to_run(case)
        summary = evaluate_provider_output_cases((case,))

        self.assertEqual(run.source_domains, ("acme.ai", "acme.ai"))
        self.assertTrue(summary.passed)

    def test_eval_accepts_unsupported_region_as_case_metadata_without_network(self):
        case = ProviderOutputEvalCase(
            name="unsupported-region-fixture",
            region="AQ",
            response=response_with_geo(citations=["https://acme.ai/"], mentions=[], recommendations=[]),
            expected_citations=("https://acme.ai/",),
        )

        run = provider_response_to_run(case)

        self.assertEqual(run.region, "AQ")
        self.assertEqual(run.engine, "openai_compatible")

    def test_eval_passes_expected_provider_error(self):
        case = ProviderOutputEvalCase(
            name="provider-error",
            response={"error": {"message": "provider quota exceeded"}},
            expected_error="provider quota exceeded",
        )

        summary = evaluate_provider_output_cases((case,))

        self.assertTrue(summary.passed)
        self.assertEqual(summary.results[0].message, "expected error")

    def test_eval_passes_expected_malformed_payload_error(self):
        case = ProviderOutputEvalCase(
            name="malformed-payload",
            response={"choices": []},
            expected_error="did not include answer choices",
        )

        summary = evaluate_provider_output_cases((case,))

        self.assertTrue(summary.passed)

    def test_eval_fails_when_forbidden_value_appears_in_output(self):
        case = ProviderOutputEvalCase(
            name="redaction-regression",
            response=response_with_geo(citations=[], mentions=["sample-access-value"], recommendations=[]),
            forbidden_substrings=("sample-access-value",),
        )

        summary = evaluate_provider_output_cases((case,))

        self.assertFalse(summary.passed)
        self.assertEqual(summary.failed_count, 1)
        self.assertIn("forbidden output", summary.results[0].message)

    def test_eval_summary_serializes_results(self):
        summary = evaluate_provider_output_cases(
            (
                ProviderOutputEvalCase(name="ok", response=response_with_geo()),
                ProviderOutputEvalCase(name="bad", response={"choices": []}, expected_error="answer choices"),
            )
        )

        payload = summary.to_dict()

        self.assertTrue(payload["passed"])
        self.assertEqual(payload["passed_count"], 2)
        self.assertEqual(payload["failed_count"], 0)
        self.assertEqual(len(payload["results"]), 2)


if __name__ == "__main__":
    unittest.main()
