export const sampleManifestArtifact = {
  package_id: 'fixture-package-001',
  generated_at: '2026-06-25T00:00:00Z',
  files: {
    report_json: 'report.json',
    report_markdown: 'report.md',
    audit_database: 'audit.sqlite',
  },
};

export const sampleReportArtifact = {
  score: {
    visibility_score: 0.42,
    mention_share: 0.5,
    citation_share: 0.25,
    recommendation_share: 0.25,
  },
  missing_queries: ['Best GEO software tools for marketing teams in US'],
  competitor_map: { Globex: 1 },
  cited_sources: ['acme.ai', 'globex.com'],
  failures: ['missing_brand_mention,citation_gap'],
  recommended_actions: ['strengthen_page_evidence', 'add_comparison_content'],
  retest_plan: ['Re-run the same package after content updates.'],
};

export function buildReportArtifactView(manifest, report) {
  const warnings = [];
  if (!manifest) {
    warnings.push('Missing manifest.json; package provenance is unavailable.');
  }
  if (!report) {
    warnings.push('Missing report.json; report sections cannot be rendered.');
  }
  const safeReport = report || {};
  const files = manifest && manifest.files ? manifest.files : {};
  return {
    packageId: manifest?.package_id || 'unknown-package',
    generatedAt: manifest?.generated_at || 'unknown-time',
    source: files.report_json || 'report.json',
    warnings,
    score: safeReport.score || {},
    missingQueries: safeReport.missing_queries || [],
    competitorMap: mapEntries(safeReport.competitor_map || {}),
    citedSources: safeReport.cited_sources || [],
    failures: safeReport.failures || [],
    recommendedActions: safeReport.recommended_actions || [],
    retestPlan: safeReport.retest_plan || [],
    files: [files.report_json, files.report_markdown, files.audit_database].filter(Boolean),
  };
}

function mapEntries(mapping) {
  return Object.entries(mapping).map(([name, count]) => `${name}: ${count}`);
}
