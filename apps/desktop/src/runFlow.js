export const defaultBrandProfile = {
  brand: '',
  domain: '',
  competitors: '',
  region: 'US',
  language: 'en',
  category: '',
  audience: '',
};

export const desktopRunPaths = [
  { id: 'manual', label: 'Manual import path', statusKey: 'manual', executable: true },
  { id: 'configured', label: 'Configured provider path', statusKey: 'implemented', executable: true },
  { id: 'fixture', label: 'Fixture package audit', statusKey: 'simulated', executable: false },
  { id: 'blocked', label: 'Provider access issue', statusKey: 'unavailable', executable: false },
];

export function previewQueries(profile) {
  const brand = profile.brand || 'your brand';
  const category = profile.category || 'category';
  const competitors = profile.competitors || 'competitors';
  return [
    `Best ${category} tools for ${profile.audience || 'buyers'} in ${profile.region || 'US'}`,
    `${brand} vs ${competitors}`,
    `What sources cite ${brand} for ${category}?`,
  ];
}

export function prepareDesktopRun(profile, path) {
  if (!profile.brand || !profile.domain) {
    return { state: 'error', message: 'Brand and domain are required before running an audit.' };
  }
  if (!path.executable) {
    return { state: 'error', message: 'Selected path is not executable. Planned, unavailable, and simulated providers remain non-live.' };
  }
  return {
    state: 'ready_for_package',
    message: `${path.label} is ready. Generate or import the audit package, then load manifest.json and report.json in the Report panel.`,
  };
}
