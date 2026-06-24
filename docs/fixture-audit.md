# Fixture Audit Usage

This project currently supports fixture-based GEO audits. The fixture path keeps CI and demos deterministic and does not claim live engine access.

## Run the canonical fixture

```bash
geo-agent audit examples/acme-fixture.json --out out/acme
```

## Expected output

The command writes a reproducible audit package:

```text
out/acme/
  manifest.json
  report.json
  report.md
  audit.sqlite
```

## Artifact roles

- `manifest.json`: audit metadata, profile summary, engine, counts, generated timestamp, and artifact names.
- `report.json`: stable machine-readable report artifact.
- `report.md`: human-readable operational report.
- `audit.sqlite`: inspectable evidence database containing query records, page inventory, engine runs, diagnoses, tasks, and report artifacts.

## Current boundary

The example uses recorded answer evidence. It does not call live AI search engines, browsers, paid APIs, or external crawling services.
