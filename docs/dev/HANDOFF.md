# Project handoff

Checkpoint: T-038 Complete cross-format fault coverage and resource cleanup.

Completed both-format round trips, fault/resource coverage and embedded runtime artifact integrity. Fixed canceled delayed reads before they could launch stale codecs. Retained an actual independently inspected SQLite download.

## Scope and owners

Full T-001 through T-043 implementation and all seven phase releases remain user-authorized. Current executable owner: [TASKS](TASKS.md); requirements [SPEC](SPEC.md), strategy [PLAN](PLAN.md). Task/boundary evidence is under `reports/phases/6/`. Preparation QC passed and was integrated at main 1811ff44fcf8b822f94104158241dd21ef7d4d46; documentation milestone 1 closed.

## Branch and return

Working branch `phase/6-sqlite-snapshots`; creation parent/integration target `main`; branch-off `8df8cda7e219317ca69185f36a0bde6cd6614160`. No suspended campaign. Preserve all valid task commits and recover later effects from Git/hosted readback.

## Evidence and next action

174 full-suite pytest checks passed across both browsers. Tests include JSON/SQLite empty/top-ten/ties/default/nondefault settings and stable IDs/UTC, max-safe export inspected with sqlite3, exact unsafe integer rejection without a protective CHECK, schema/meta/index/storage corruption, header-bearing truncation, loader SRI failure, ten-second worker termination, network-independent JSON, busy/cancel/stale ownership and package integrity. Retained snapshot-demo.sqlite SHA-256 5320e4f326542637735b55d29cf3ad210b9dc5adc5ce4b4724fe863b70d2ab4d.

Publish/read back this task, close its issue and milestone, then continue the next eligible task in the authorized full range. These later effects remain pending at this snapshot. No extra approval is required within the existing grant.

Limitations: Only the pinned JavaScript loader is fetched; matching binary, worker and app are embedded. Tests use controlled transport serving verified upstream loader bytes and reject external binary requests; live CDN reachability is network-dependent and failure leaves JSON/gameplay usable. Managed headless browser/local Firefox override and unverified native OS focus/headed limits remain.
