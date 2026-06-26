import unittest

from geo_agent.claim_fidelity import audit_claim_fidelity, audit_claims_fidelity


class ClaimFidelityTests(unittest.TestCase):
    def test_supported_claim_matches_evidence_terms(self):
        result = audit_claim_fidelity(
            "claim:1",
            "Acme provides AI visibility audits for ecommerce teams",
            {"evidence:1": "Acme provides AI visibility audits and reports for ecommerce teams."},
        )
        self.assertEqual("supported", result.status)
        self.assertGreaterEqual(result.support_score, 0.8)
        self.assertEqual(("evidence:1",), result.matched_evidence_ids)

    def test_partial_and_unsupported_claims(self):
        partial = audit_claim_fidelity("claim:2", "Acme supports audits dashboards and workflows", {"evidence:1": "Acme supports audits."})
        unsupported = audit_claim_fidelity("claim:3", "Acme offers payroll compliance", {"evidence:1": "Acme provides visibility audits."})
        self.assertEqual("partial", partial.status)
        self.assertEqual("unsupported", unsupported.status)
        self.assertIn("payroll", unsupported.missing_terms)

    def test_contradicted_claim(self):
        result = audit_claim_fidelity(
            "claim:4",
            "Acme supports offline exports",
            {"evidence:1": "Acme does not support offline exports."},
        )
        self.assertEqual("contradicted", result.status)

    def test_unknown_and_batch_audit(self):
        unknown = audit_claim_fidelity("claim:5", "", {})
        self.assertEqual("unknown", unknown.status)
        batch = audit_claims_fidelity({"claim:1": "Acme provides audits"}, {"evidence:1": "Acme provides audits."})
        self.assertEqual(1, len(batch))
        self.assertEqual("claim:1", batch[0].claim_id)


if __name__ == "__main__":
    unittest.main()
