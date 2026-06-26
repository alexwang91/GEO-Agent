# Error State Taxonomy

Error states must help the user recover without overstating audit success or provider coverage.

| Error code | Stage | User-facing copy pattern | Recovery action |
| :--- | :--- | :--- | :--- |
| `project_profile_missing` | Project setup | Required project fields are missing. | Complete brand, domain, market, language, and competitor fields. |
| `query_space_empty` | Query review | No query space exists yet. | Generate, import, or manually add queries. |
| `provider_planned` | Evidence source | This provider is planned and is not available for audit execution. | Choose manual import, simulated fixture data, or an implemented configured provider. |
| `provider_not_configured` | Evidence source | This provider is implemented but not configured for this project. | Configure access or use manual import. |
| `manual_import_invalid` | Manual import | The imported evidence does not match the required schema. | Fix the import fields and retry. |
| `simulated_fixture_unavailable` | Simulated evidence | The fixture package could not be loaded. | Select a valid fixture package. |
| `crawl_partial_failure` | Page evidence | Some pages failed to load; available page evidence can still be reviewed. | Inspect per-page status and rerun only failed pages. |
| `sample_budget_too_low` | Audit interpretation | The sample budget is too low for stronger conclusions. | Treat metrics as directional or collect more samples. |
| `package_redaction_failed` | Artifact safety | Output safety checks failed before export. | Remove raw access values and regenerate the package. |
| `retest_not_comparable` | Retest | Baseline and follow-up are not comparable. | Match prompt, engine, region, language, and sample plan. |

## Error copy rules

- State the failed stage.
- State whether partial evidence is still usable.
- Preserve manual, simulated, live configured, and planned provider distinctions.
- Keep low-sample language directional.
- Do not render provider failure as audit success.
