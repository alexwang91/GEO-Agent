export const runAuditCopy = {
  title: 'Run Audit',
  subtitle: 'Run a fixture-safe or manual-import audit with explicit provider boundaries.',
  networkNote: 'CI and fixture audit paths do not make live provider, crawler, or browser calls.',
};

export const runAuditControls = [
  'Select project',
  'Select query set',
  'Select evidence source',
  'Set sample count',
  'Run fixture audit',
  'Run manual import audit',
];

export const runAuditStatusLabels = [
  'Ready',
  'Running',
  'Completed',
  'Failed',
  'Provider unavailable',
];
