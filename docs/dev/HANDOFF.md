# Project handoff

Checkpoint: T-003 Complete locking line clearing scoring and game over.

Complete the playable classic core: legal lock/top-out, simultaneous line removal, score/levels/speed, soft-drop points, spawn loss and one completion event. Milestone 1.1 now demonstrates a complete keyboard-played run and restart.

## Scope and owners

Full T-001 through T-043 implementation and all seven phase releases remain user-authorized. Current executable owner: [TASKS](TASKS.md); requirements [SPEC](SPEC.md), strategy [PLAN](PLAN.md). Task/boundary evidence is under `reports/phases/1/`. Preparation QC passed and was integrated at main 1811ff44fcf8b822f94104158241dd21ef7d4d46; documentation milestone 1 closed.

## Branch and return

Working branch `phase/1-classic-baseline`; creation parent/integration target `main`; branch-off `1811ff44fcf8b822f94104158241dd21ef7d4d46`. No suspended campaign. Preserve all valid task commits and recover later effects from Git/hosted readback.

## Evidence and next action

RED: four new lock/clear/score/completion tests failed against the movement-only core (6 existing passed). GREEN: all 18 core and actual Chromium/Firefox browser checks passed in 22.62s. Native keyboard gameplay reached game over and restarted in both browsers; deterministic fixtures verified one/four-line clears, exact score/level/speed, above-top rejection and completion idempotence.

Publish/read back this task, close its issue and milestone, then continue the next eligible task in the authorized full range. These later effects remain pending at this snapshot. No extra approval is required within the existing grant.

Limitations: Pause/help/packaging and the remaining full project are still pending. Firefox uses the diagnosed trusted-local override; no full/headed/native-window compatibility is claimed.
