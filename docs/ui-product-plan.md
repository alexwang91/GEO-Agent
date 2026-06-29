# UI Productization Plan

## Goal

Move the desktop shell from a report viewer preview toward an operable audit workflow. Keep the implementation honest: no provider execution claims until the UI is wired to a verified backend path, and no credentials in reports, manifests, logs, databases, or UI state.

## Milestones

| Milestone | Status | Scope |
| :--- | :--- | :--- |
| UI-P1 | DONE | Editable Brand Profile form and query preview in the desktop shell. |
| UI-P2 | DONE | Manual capture/package import workflow with validation states and manual-only evidence copy. |
| UI-P3 | TODO | Reproducible UI preview or screenshot artifact for product review. |

## UI-P1 Acceptance

- Brand Profile is an editable form, not static description text.
- User can generate a query preview from the current profile.
- Query preview does not call providers or imply live sampling.
- Huawei smartwatch example remains available as resettable sample data.
- Structural tests cover form state, query preview generation, and styling hooks.

## UI-P2 Acceptance

- Manual capture/package import flow is visible as a first-class user path.
- Google AIO remains manual-only.
- UI distinguishes generated package loading from demo data.
- Validation errors are clear before any report render.
- The UI summarizes capture count, profile, engines, warnings, errors, and the `geo-agent capture-package` command without running providers.

## UI-P3 Acceptance

- CI or a deterministic script can render the desktop shell preview.
- A reviewer can inspect a generated PNG or equivalent static preview artifact.
- Screenshot/preview must be labeled as demo or fixture if it uses demo data.
