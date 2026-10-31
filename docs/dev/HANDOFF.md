# Project handoff

Checkpoint: T-006 Package and verify the single HTML baseline.

Build the versioned-source 0.1.0 browser candidate with stable HTML/ZIP/checksum names, exact archive inventory, install/license documents, direct/CI naming gates, build-only release verification workflow and hosted-download verification tooling. Complete milestone 1.2 local delivery readiness.

## Scope and owners

Full T-001 through T-043 implementation and all seven phase releases remain user-authorized. Current executable owner: [TASKS](TASKS.md); requirements [SPEC](SPEC.md), strategy [PLAN](PLAN.md). Task/boundary evidence is under `reports/phases/1/`. Preparation QC passed and was integrated at main 1811ff44fcf8b822f94104158241dd21ef7d4d46; documentation milestone 1 closed.

## Branch and return

Working branch `phase/1-classic-baseline`; creation parent/integration target `main`; branch-off `1811ff44fcf8b822f94104158241dd21ef7d4d46`. No suspended campaign. Preserve all valid task commits and recover later effects from Git/hosted readback.

## Evidence and next action

RED: the artifact contract failed because no producer existed. GREEN: all 31 core/browser/artifact checks passed in 41.87s, including actual packaged HTML in Chromium and Firefox, inventory/checksum byte comparisons and rejection of a deliberately versioned raw HTML filename. Rebuilt/rechecked after the install-doc update; both focused artifact checks passed. Both packaging commands and Python compilation passed. Workflow trigger/input/checkout/permission/naming-gate wiring inspected; live CI and hosted release checks are pending publication.

Publish/read back this task, close its issue and milestone, then continue the next eligible task in the authorized full range. These later effects remain pending at this snapshot. No extra approval is required within the existing grant.

Limitations: The 0.1.0 candidate is locally verified but not yet released. Live CI, release commit/tag/publication and actual hosted/latest downloads follow phase review/integration. Native OS focus delivery remains unverified; Firefox local tests use the diagnosed override.
