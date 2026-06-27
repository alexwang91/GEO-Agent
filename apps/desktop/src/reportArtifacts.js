export const demoManifestArtifact = {
  package_id: 'demo-fixture-package-001',
  generated_at: '2026-06-25T00:00:00Z',
  artifact_kind: 'demo',
  files: {
    report_json: 'report.json',
    report_markdown: 'report.md',
    audit_database: 'audit.sqlite',
  },
};

export const demoReportArtifact = {
  artifact_kind: 'demo',
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

export function emptyReportArtifactView() {
  return buildReportArtifactView(null, null, { state: 'empty', sourceLabel: 'No package loaded' });
}

export function demoReportArtifactView() {
  return buildReportArtifactView(demoManifestArtifact, demoReportArtifact, { state: 'demo', sourceLabel: 'Demo fixture package' });
}

export function buildReportArtifactView(manifest, report, options = {}) {
  const warnings = [];
  if (!manifest) {
    warnings.push('Missing manifest.json; package provenance is unavailable.');
  }
  if (!report) {
    warnings.push('Missing report.json; report sections cannot be rendered.');
  }
  const safeReport = report || {};
  const files = manifest && manifest.files ? manifest.files : {};
  const state = options.state || 'loaded';
  const kind = manifest?.artifact_kind || safeReport.artifact_kind || state;
  if (kind === 'demo') {
    warnings.push('Demo fixture artifact: do not represent this as generated live audit output.');
  }
  return {
    state,
    artifactKind: kind,
    sourceLabel: options.sourceLabel || 'Generated audit package',
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

export async function loadReportArtifactViewFromFiles(files) {
  const byName = Object.fromEntries([...files].map((file) => [file.name, file]));
  const manifestFile = byName['manifest.json'];
  const reportFile = byName['report.json'];
  if (!manifestFile || !reportFile) {
    throw new Error('Select a generated audit package containing manifest.json and report.json.');
  }
  const manifest = await readJsonFile(manifestFile);
  const report = await readJsonFile(reportFile);
  return buildReportArtifactView(manifest, report, { state: 'loaded', sourceLabel: 'Generated audit package' });
}

function readJsonFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        resolve(JSON.parse(String(reader.result || '{}')));
      } catch (error) {
        reject(new Error(`${file.name} is not valid JSON: ${error.message}`));
      }
    };
    reader.onerror = () => reject(new Error(`Could not read ${file.name}.`));
    reader.readAsText(file);
  });
}

function mapEntries(mapping) {
  return Object.entries(mapping).map(([name, count]) => `${name}: ${count}`);
}
