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
  { name: 'Perplexity', capabilities: ['Answer', 'Search'], access: ['API Key'], status: 'Planned' },
  { name: 'Gemini', capabilities: ['Answer', 'Model'], access: ['API Key'], status: 'Planned' },
  { name: 'Crawl4AI', capabilities: ['Crawl'], access: ['Local', 'Platform'], status: 'Planned' },
  { name: 'Firecrawl', capabilities: ['Crawl'], access: ['API Key'], status: 'Planned' },
  { name: 'Google Search Console', capabilities: ['Analytics', 'Search'], access: ['OAuth'], status: 'Planned' },
  { name: 'Manual Import', capabilities: ['Answer'], access: ['Manual Import'], status: 'Available' },
];

const fixturePackage = {
  mode: 'Fixture-only audit path',
  command: 'run_fixture_audit(fixture_path, output_dir)',
  status: 'Ready for local fixtures',
  warning: 'Provider-backed audit execution is still planned for V5-7.',
  outputs: ['manifest.json', 'report.json', 'report.md', 'audit.sqlite'],
};

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
          <p>
            Connect providers, enter brand context, preview queries, run an audit, and review the evidence package.
          </p>
          <p className="security-note">
            Credentials are used only to run your audit. They are never written into reports, manifests, logs, or audit databases.
          </p>
        </header>

        <section id="providers" className="panel">
          <h3>Providers</h3>
          <div className="provider-grid">
            {providers.map((provider) => (
              <article className="provider-card" key={provider.name}>
                <div className="card-header">
                  <h4>{provider.name}</h4>
                  <span className={`status ${provider.status.toLowerCase().replaceAll(' ', '-')}`}>{provider.status}</span>
                </div>
                <p>Capabilities: {provider.capabilities.join(', ')}</p>
                <p>Access: {provider.access.join(', ')}</p>
                <button disabled={provider.status === 'Planned'}>
                  {provider.status === 'Planned' ? 'Coming soon' : 'Configure'}
                </button>
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
          <p className="eyebrow">{fixturePackage.mode}</p>
          <p>{fixturePackage.command} accepts a fixture path and output directory, then returns package metadata and report file paths.</p>
          <p className="security-note">{fixturePackage.warning}</p>
          <button disabled>Run fixture audit from local file</button>
          <ol>
            <li>Build query space</li>
            <li>Crawl owned pages from fixture data</li>
            <li>Read recorded answer runs</li>
            <li>Store evidence</li>
            <li>Score visibility</li>
            <li>Diagnose failures</li>
            <li>Generate tasks</li>
            <li>Write audit package</li>
          </ol>
        </section>

        <section id="report" className="panel">
          <h3>Report</h3>
          <p>No audit report yet. Run a fixture audit to generate visibility evidence.</p>
        </section>

        <section id="evidence-package" className="panel">
          <h3>Evidence Package</h3>
          <ul>
            {fixturePackage.outputs.map((output) => (
              <li key={output}>{output}</li>
            ))}
          </ul>
        </section>
      </section>
    </main>
  );
}