const navItems = [
  'Providers',
  'Brand Profile',
  'Queries',
  'Audit Run',
  'Report',
  'Evidence Package',
];

const providers = [
  { name: 'OpenAI-compatible', capabilities: ['Answer', 'Model'], access: ['API Key', 'Platform'], status: 'Configured boundary' },
  { name: 'Static crawler', capabilities: ['Crawl'], access: ['Local'], status: 'Fake/test available' },
  { name: 'Perplexity', capabilities: ['Answer', 'Search'], access: ['API Key'], status: 'Planned' },
  { name: 'Gemini', capabilities: ['Answer', 'Model'], access: ['API Key'], status: 'Planned' },
  { name: 'Crawl4AI', capabilities: ['Crawl'], access: ['Local', 'Platform'], status: 'Planned' },
  { name: 'Firecrawl', capabilities: ['Crawl'], access: ['API Key'], status: 'Planned' },
  { name: 'Google Search Console', capabilities: ['Analytics', 'Search'], access: ['OAuth'], status: 'Planned' },
  { name: 'Manual Import', capabilities: ['Answer'], access: ['Manual Import'], status: 'Available' },
];

const runPaths = [
  { label: 'Fixture package audit', status: 'Available for local fixtures', command: 'run_fixture_audit(fixture_path, output_dir)' },
  { label: 'Manual import path', status: 'Recorded evidence available', command: 'manual_import(recorded_dataset)' },
  { label: 'Fake provider path', status: 'Fake/test only', command: 'static_crawler + recorded answer adapter' },
];

const reportPreview = {
  source: 'Generated package artifact: report.json',
  score: {
    visibility_score: 0.42,
    mention_share: 0.5,
    citation_share: 0.25,
    recommendation_share: 0.25,
  },
  missing_queries: ['Best GEO software tools for marketing teams in US'],
  competitor_map: ['Globex: 1'],
  cited_sources: ['acme.ai', 'globex.com'],
  failures: ['missing_brand_mention,citation_gap'],
  recommended_actions: ['strengthen_page_evidence', 'add_comparison_content'],
  retest_plan: ['Re-run the same package after content updates.'],
};

const packageFiles = ['manifest.json', 'report.json', 'report.md', 'audit.sqlite'];

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
  return (
    <article className="evidence-block">
      <h4>{title}</h4>
      <ul>
        {values.map((value) => (
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
          <div className="provider-grid">
            {providers.map((provider) => (
              <article className="provider-card" key={provider.name}>
                <div className="card-header">
                  <h4>{provider.name}</h4>
                  <span className={`status ${statusClass(provider.status)}`}>{provider.status}</span>
                </div>
                <p>Capabilities: {provider.capabilities.join(', ')}</p>
                <p>Access: {provider.access.join(', ')}</p>
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
          <p className="security-note">Live provider execution remains a later V6 path. This screen represents local package artifacts and deterministic test providers only.</p>
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
          <p className="eyebrow">{reportPreview.source}</p>
          <div className="metric-grid">
            <MetricCard label="Visibility score" value={reportPreview.score.visibility_score} />
            <MetricCard label="Mention share" value={reportPreview.score.mention_share} />
            <MetricCard label="Citation share" value={reportPreview.score.citation_share} />
            <MetricCard label="Recommendation share" value={reportPreview.score.recommendation_share} />
          </div>
          <div className="report-grid">
            <ListBlock title="Missing queries" values={reportPreview.missing_queries} />
            <ListBlock title="Competitor map" values={reportPreview.competitor_map} />
            <ListBlock title="Cited sources" values={reportPreview.cited_sources} />
            <ListBlock title="Failure diagnoses" values={reportPreview.failures} />
            <ListBlock title="Recommended tasks" values={reportPreview.recommended_actions} />
            <ListBlock title="Retest plan" values={reportPreview.retest_plan} />
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