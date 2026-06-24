# Entity Profile Schema

The entity profile is the M1 domain intake contract for GEO Agent. It gives later milestones a stable record for query generation, page inventory, engine sampling, scoring, diagnosis, and optimization planning.

## Required fields

| Field | Type | Validation rule |
| --- | --- | --- |
| `brand` | string | Non-empty brand name. |
| `aliases` | list[string] | Present as a list; may be empty when the brand has no known aliases. |
| `domain` | string | Canonical website host such as `example.com` or `https://example.com`. The validator stores the lowercase host without `www.`. |
| `competitors` | list[string] | At least one non-empty competitor entity. |
| `target_regions` | list[string] | At least one non-empty region code or region name. |
| `target_languages` | list[string] | At least one non-empty language code or language name. |
| `target_customer` | string | Non-empty customer segment. |
| `main_product` | string | Non-empty product or service description. |
| `category` | string | Non-empty market/category label. |
| `business_goal` | string | Non-empty outcome the GEO workflow should optimize for. |

## Validation behavior

`validate_entity_profile(payload)` accepts a dictionary-like object and returns a normalized `EntityProfile`. Invalid or missing fields raise `EntityProfileValidationError`.

Each validation issue includes:

- `field`: exact field or list item path;
- `message`: factual reason validation failed;
- `expected`: required shape;
- `received`: observed shape;
- `remediation`: concrete next edit for the intake payload.

This keeps intake failures actionable for UI forms, CLI imports, and future API responses without binding the schema to one transport layer.
