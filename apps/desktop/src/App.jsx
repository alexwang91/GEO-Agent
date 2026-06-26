import { buildReportArtifactView, sampleManifestArtifact, sampleReportArtifact } from './reportArtifacts';

const navItems = [
  'Providers',
  'Brand Profile',
  'Queries',
  'Audit Run',
  'Report',
  'Evidence Package',
];

const providers = [
  { name: 'OpenAI-compatible', capabilities: ['Answer', 'Model'], access: ['API Key', 'Platform'], status: 'Implemented', note: 'Implemented API boundary; not ChatGPT Search.' },
  { name: 'Static crawler', capabilities: ['Crawl'], access: ['Local'], status: 'Implemented', note: 'Fixture-backed local crawler boundary for deterministic tests.' },
  { name: 'Perplexity', capabilities: ['Answer', 'Search'], access: ['API Key'], status: 'Planned', note: 'Planned provider; not available for live audits.' },
  { name: 'Gemini', capabilities: ['Answer', 'Model'], access: ['API Key'], status: 'Planned', note: 'Planned provider; not available for live audits.' },
  { name: 'Crawl4AI', capabilities: ['Crawl'], access: ['Local', 'Platform'], status: 'Planned', note: 'Planned crawler provider.' },
  { name: 'Firecrawl', capabilities: ['Crawl'], access: ['API Key'], status: 'Planned', note: 'Planned crawler provider.' },
  { name: 'Google Search Console', capabilities: ['Analytics', 'Search'], access: ['OAuth'], status: 'Planned', note: 'Planned analytics/search provider.' },
  { name: 'Manual Import', capabilities: ['Answer'], access: ['Manual Import'], status: 'Implemented', note: 'Implemented manual/recorded evidence path.' },
];

const runPaths = [
  { label: 'Fixture package audit', status: 'Implemented for local fixtures', command: 'run_fixture_audit(fixture_path, output_dir)' },
  { label: 'Manual import path', status: 'Implemented for recorded evidence', command: 'manual_import(recorded_dataset)' },
  { label: 'Fake provider path', status: 'Implemented for deterministic tests', command: 'static_crawler + recorded answer adapter' },
];

const reportView = buildReportArtifactView(sampleManifestArtifact, sampleReportArtifact);
const packageFiles = ['manifest.json', ...reportView.files];

function statusClass(status) {
  return status.toLowerCase().replaceAll(' ', '-').replaceAll('/', '-');
}

function MetricCard({ label, value }) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function ListBlock({ title, values }) {
  const listValues = values.length ? values : ['No evidence in this artifact section.'];
  return (
    <article className="evidence-block">
      <h4>{title}</h4>
      <ul>
        {listValues.map((value) => (
          <li key={value}>{value}</li>
        ))}
      </ul>
    </article>
  );
}

export function App() {
  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Workflow navigation">
        <h1>GEO Agent</h1>
        <nav>
          {navItems.map((item) => (
            <a key={item} href={`#${item.toLowerCase().replaceAll(' ', '-')}`}>{item}</a>
          ))}
        </nav>
      </aside>

      <section className="workspace">
        <header className="hero">
          <p className="eyebrow">Tauri + React desktop shell</p>
          <h2>AI Search Visibility Audit</h2>
          <p>Connect providers, enter brand context, preview queries, run an audit, and review the evidence package.</p>
          <p className="security-note">Credentials are used only to run your audit. They are never written into reports, manifests, logs, or audit databases.</p>
        </header>

        <section id="providers" className="panel">
          <h3>Providers</h3>
          <p className="security-note">Provider status uses the registry language from docs/provider-status-language.md. Planned providers are not live or available for audit execution.</p>
          <div className="provider-grid">
            {providers.map((provider) => (
              <article className="provider-card" key={provider.name}>
                <div className="card-header">
                  <h4>{provider.name}</h4>
                  <span className={`status ${statusClass(provider.status)}`}>{provider.status}</span>
                </div>
                <p>Capabilities: {provider.capabilities.join(', ')}</p>
                <p>Access: {provider.access.join(', ')}</p>
                <p>{provider.note}</p>
                <button disabled={provider.status === 'Planned'}>{provider.status === 'Planned' ? 'Coming soon' : 'Configure'}</button>
              </article>
            ))}
          </div>
        </section>

        <section id="brand-profile" className="panel split">
          <div>
            <h3>Brand Profile</h3>
            <p>Brand name, domain, competitors, regions, languages, target customer, product, category, and business goal.</p>
          </div>
          <button>Generate Queries</button>
        </section>

        <section id="queries" className="panel">
          <h3>Queries</h3>
          <p>No queries generated yet. Complete your brand profile first.</p>
        </section>

        <section id="audit-run" className="panel">
          <h3>Audit Run</h3>
          <p className="eyebrow">Fixture, manual-import, and fake-provider run paths</p>
          <p className="eyebrow">Fixture-only audit path</p>
          <p className="security-note">Provider-backed audit execution uses implemented fixture/manual boundaries only unless a provider is explicitly configured and verified. Planned providers remain planned and unavailable for live audits.</p>
          <div className="run-path-grid">
            {runPaths.map((path) => (
              <article className="run-path-card" key={path.label}>
                <div className="card-header">
                  <h4>{path.label}</h4>
                  <span className={`status ${statusClass(path.status)}`}>{path.status}</span>
                </div>
                <p><strong>Command:</strong> {path.command}</p>
              </article>
            ))}
          </div>
          <button disabled>Run fixture audit from local file</button>
          <button disabled>Run selected audit path</button>
          <ol>
            <li>Build query space</li>
            <li>Crawl owned pages from fixture or fake/static provider data</li>
            <li>Read recorded or fake answer runs</li>
            <li>Store evidence</li>
            <li>Score visibility</li>
            <li>Diagnose failures</li>
            <li>Generate tasks</li>
            <li>Write audit package</li>
          </ol>
        </section>

        <section id="report" className="panel">
          <h3>Report</h3>
          <p>No audit report yet for a new project. Run or import an audit package to generate visibility evidence.</p>
          <p className="eyebrow">Generated package artifact: {reportView.source}</p>
          <p>Package: {reportView.packageId} generated at {reportView.generatedAt}</p>
          {reportView.warnings.map((warning) => (
            <p className="security-note" key={warning}>{warning}</p>
          ))}
          <div className="metric-grid">
            <MetricCard label="Visibility score" value={reportView.score.visibility_score} />
            <MetricCard label="Mention share" value={reportView.score.mention_share} />
            <MetricCard label="Citation share" value={reportView.score.citation_share} />
            <MetricCard label="Recommendation share" value={reportView.score.recommendation_share} />
          </div>
          <div className="report-grid">
            <ListBlock title="Missing queries" values={reportView.missingQueries} />
            <ListBlock title="Competitor map" values={reportView.competitorMap} />
            <ListBlock title="Cited sources" values={reportView.citedSources} />
            <ListBlock title="Failure diagnoses" values={reportView.failures} />
            <ListBlock title="Recommended tasks" values={reportView.recommendedActions} />
            <ListBlock title="Retest plan" values={reportView.retestPlan} />
          </div>
          <div className="download-actions" aria-label="Report export actions">
            <button disabled>Download report.json</button>
            <button disabled>Download report.md</button>
            <button disabled>Download audit package</button>
          </div>
        </section>

        <section id="evidence-package" className="panel">
          <h3>Evidence Package</h3>
          <ul>
            {packageFiles.map((output) => (
              <li key={output}>{output}</li>
            ))}
          </ul>
        </section>
      </section>
    </main>
  );
}
