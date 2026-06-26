export const evidenceSourceSetupCopy = {
  title: 'Evidence Source Setup',
  subtitle: 'Choose safe evidence inputs before running an audit.',
  safetyNote: 'Do not add live credentials to fixture or manual-import workflows.',
};

export const evidenceSourceOptions = [
  'Manual import',
  'Static crawler fixture',
  'Browser capture artifact',
  'Rendered HTML fallback',
  'Planned provider',
];

export const evidenceSourceGuardrails = [
  'Manual import accepts curated static evidence only.',
  'Crawler and browser capture paths remain fixture-safe in CI.',
  'Planned providers remain planned and unavailable for live audits.',
];
