export function emptyManualCaptureView() {
  return {
    state: 'empty',
    sourceLabel: 'No manual capture package selected',
    warnings: [],
    errors: [],
    profile: null,
    captureCount: 0,
    engines: [],
    regions: [],
    languages: [],
    hasGoogleAio: false,
    command: 'geo-agent capture-package captures.json --out out/manual-package',
  };
}

export async function loadManualCaptureViewFromFile(file) {
  if (!file) {
    return {
      ...emptyManualCaptureView(),
      state: 'error',
      errors: ['Select a captures.json file before validating manual evidence.'],
    };
  }
  const payload = await readJsonFile(file);
  return buildManualCaptureView(payload, { sourceLabel: file.name });
}

export function buildManualCaptureView(payload, options = {}) {
  const errors = [];
  const warnings = [];
  const profile = payload && typeof payload === 'object' ? payload.profile : null;
  const captures = Array.isArray(payload?.captures) ? payload.captures : [];

  if (!profile || typeof profile !== 'object') {
    errors.push('Missing profile object. Manual capture packages must include profile metadata.');
  }
  if (!Array.isArray(payload?.captures)) {
    errors.push('Missing captures array. Add pasted or recorded engine answers before packaging.');
  }
  if (captures.length === 0) {
    warnings.push('No captures found yet; package validation is incomplete.');
  }

  const engines = unique(captures.map((capture) => capture.engine).filter(Boolean));
  const regions = unique(captures.map((capture) => capture.region).filter(Boolean));
  const languages = unique(captures.map((capture) => capture.language).filter(Boolean));
  const missingAnswers = captures.filter((capture) => !capture.answer_text && !capture.raw_answer).length;
  const missingQueries = captures.filter((capture) => !capture.query).length;
  const hasGoogleAio = engines.some((engine) => normalize(engine).includes('google_aio') || normalize(engine).includes('aio'));

  if (missingAnswers) {
    errors.push(`${missingAnswers} capture(s) are missing answer_text/raw_answer.`);
  }
  if (missingQueries) {
    errors.push(`${missingQueries} capture(s) are missing query.`);
  }
  if (hasGoogleAio) {
    warnings.push('Google AIO is manual-only: AIO share links are gated and not auto-capturable. Keep this as explicit manual evidence.');
  }
  if (engines.length > 1) {
    warnings.push('Multi-engine manual capture package detected. Interpret aggregate scores as directional and inspect per-engine components first.');
  }

  return {
    state: errors.length ? 'error' : 'ready',
    sourceLabel: options.sourceLabel || 'Manual capture package',
    warnings,
    errors,
    profile: profile
      ? {
          brand: profile.brand || 'unknown-brand',
          domain: profile.domain || 'unknown-domain',
        }
      : null,
    captureCount: captures.length,
    engines,
    regions,
    languages,
    hasGoogleAio,
    command: 'geo-agent capture-package captures.json --out out/manual-package',
  };
}

function unique(values) {
  return [...new Set(values.map((value) => String(value).trim()).filter(Boolean))].sort();
}

function normalize(value) {
  return String(value || '').toLowerCase().replaceAll('-', '_').replaceAll(' ', '_');
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
