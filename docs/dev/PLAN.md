# Delivery plan

## Strategy and complete coverage

Deliver [SPEC](SPEC.md) in seven bounded releases, growing one usable browser game. Retain the [architecture](ARCHITECTURE.md) and [component boundaries](DECOMPOSITION.md) inside one HTML document. Every phase preserves the earlier playable path, adds its selected contracts, and integrates before its release and successor begin. A phase's release describes only its delivered subset.

| Phase / release | Useful outcome | Included contracts | Deliberate deferrals |
| --- | --- | --- | --- |
| 1 — Classic playable baseline / 0.1.0 | A complete classic game players can start, play, lose, pause and restart | G1 basic geometry/collision/rotation, G2 scoring/levels/completion, G3 failed-downward lock, basic U1/U2 information/buttons/help and U3 browser delivery | Uniform independent piece selection; no kicks, hold/preview/ghost/drop, penetrator, settings, results transfer or final optional-panel behavior |
| 2 — Modern rules / 0.2.0 | Bag/hold/preview and landing/timing conveniences | G1 kicks, G3 full-interval timing, G4, G5 ordinary ghost/drop; default CFG1 values in the domain | Player configuration, dynamic ghost, penetrator and all persistence; fixed visible ghost/preview, hold/drop on, general interval locking |
| 3 — Configurable penetrator gameplay / 0.3.0 | Six session-only settings, conditional ghost and earned penetration | CFG1 session-only/CFG4, G5 dynamic visibility, G6-G7 and remaining G3 policy selection | No setting cookies or query handling; no leaderboard/files |
| 4 — Persistent configuration / 0.4.0 | Settings follow reloads and shareable URLs | CFG2-CFG3 and persistent CFG4 integration | Results still have no persistence/history UI; file transfer remains independent |
| 5 — Portable session results / 0.5.0 | Top-ten completed results and manual JSON transfer of results/settings | F1-F2, F4-F5 JSON paths, leaderboard and Save/Restore portions of U1 | SQLite export/import; full optional-panel layout/toggles |
| 6 — SQLite snapshots / 0.6.0 | Equivalent JSON/SQLite transfer with bounded isolated decoding | F3 and remaining F4-F5 SQLite/error/resource paths | Final centered layout and three visibility toggles |
| 7 — Centered panel layout / 1.0.0 | Full five-panel arrangement and complete product acceptance | U1-U2 final interactions, A1-A8 complete integration and U3 final artifacts | None within the requested scope |

Phase 1 is a usable game, not an infrastructure skeleton or a first milestone hiding the entire target. Phase 2 groups the coupled queue/hold/landing/timing rules while leaving optional configuration and special penetration independent. Phase 3 connects all six settings to the special gameplay they select and demonstrates an explicitly nonpersistent increment. Phases 4–6 isolate browser-state and two distinct portable-file risks. Phase 7 changes presentation over verified behavior and closes the complete acceptance matrix. The narrow phases require no padding milestones solely to approach a numerical target.

## Milestones, demonstrations and exits

Each delivery milestone requires a capability-wide code review, relevant tests/regressions, blocker repairs, a committed milestone report with TODO disposition and a HANDOFF update. TASKS assigns these obligations to the final delivery task unless the standalone review threshold applies. Each phase ends with the separate one-task phase review milestone listed below.

| Milestone | Outcome / demonstrable boundary | Required exit evidence |
| --- | --- | --- |
| 1.1 — Playable core | Spawn, move, rotate, fall, lock, clear, score and finish a game | Deterministic geometry/clear/score/game-over checks and actual Canvas/keyboard play; a complete run is playable |
| 1.2 — Usable browser delivery | Information, two gameplay buttons, pause/focus handling, help and deployable HTML | Pause/restart/visibility/input checks, responsive readable UI, both-browser smoke and verified browser package candidate |
| 1.3 — Phase review | Baseline review and release readiness | Cross-milestone code review, baseline A1/scoped A8, regressions, phase report and release-ready notes/package |
| 2.1 — Bag hold and preview | Predictable seven-bag consumption with hold and next display | Bag membership, preview non-consumption, hold/reset/spawn-loss cases and browser rendering/input |
| 2.2 — Landing and grounded timing | Kicks, ordinary ghost/drop and interval locking integrate | Kick failures/success, shared landing, hard-drop distance and failed/interval/immediate timing boundaries; prior core remains playable |
| 2.3 — Phase review | Modern-rules release readiness | Queue/hold/drop/lock interaction review, scoped A2/A8 and baseline regression |
| 3.1 — Session configuration | Six controls and dynamic ghost work without reload persistence | All CFG1 values/live transitions, midline straddling and session reload tests; prove no cookie/query reads or writes |
| 3.2 — Earned penetration | Earn/spend/cap/white/hold exclusion and shared penetrator landings | Barriers/cavities, legal-lock/move viability, activation/timing interactions and bonus indicator; A3 and configuration regressions |
| 3.3 — Phase review | Configurable special-gameplay release readiness | Cross-setting/penetrator code review, A2-A4 session subset and prior game regression |
| 4.1 — URL and cookie settings | Independent resolution and browser-state changes | Explicit defaults/omissions/invalid or repeated values, reload, unrelated URL preservation and recoverable-write rollback; A4 persistent subset |
| 4.2 — Phase review | Persistent-settings release readiness | Real-browser precedence/changes plus all six live-setting regressions, cookie limitation documentation |
| 5.1 — Session leaderboard | Rank completed games and retain stable top-ten records | Completion exactly once, unfinished restart exclusion, ties, zero score, truncation and reload reset |
| 5.2 — JSON snapshot transfer | One Save/Restore pair transfers complete JSON snapshots | Schema parity, semantic timestamps/IDs, malformed/duplicate/size errors and unchanged-state rejection; actual browser downloads/restores |
| 5.3 — Phase review | Portable-results release readiness | F1/F2/F4/F5 JSON interactions, persistent configuration regressions and schema-bearing release package |
| 6.1 — SQLite snapshot transfer | Bounded worker codec and both-format choice | Real SQLite metadata/schema/rows, cross-format equivalence, independent sqlite3 inspection, corruption/extra-schema/CDN/timeout rejection and cleanup |
| 6.2 — Phase review | Both-format persistence release readiness | A5-A6 complete across both browsers; JSON independence from CDN and stable IDs/settings/cookie/URL atomicity |
| 7.1 — Centered optional panels | Full order, three toggles, mandatory visibility and file controls | All eight visibility combinations, specified widths/device pixel ratios, keyboard/focus/readability and actual Canvas screenshots; A7 |
| 7.2 — Phase review | Complete product and final release readiness | A1-A8 complete, code review of all cross-capability interactions, regressions, final implementation report and aggregated TODOs |

At milestones 1.1, 3.2, 5.2 and 7.1 retain a concrete playable/visual demonstration and explain what it establishes for a human continue/amend/simplify/stop decision. These are evidence-bearing boundaries, not added approval pauses during an already authorized implementation range. A discovered material scope/contract decision still returns to its owner.

## Verification and risk control

Use deterministic domain/model checks with injected time/randomness/IDs, then the real HTML in isolated Chromium headless shell and managed Firefox. Use pytest as the test runner; Python can invoke a bounded Node harness for extracted inline-core checks and Playwright for browser execution. Runtime production remains browser-only. Pin development dependencies at implementation, keep browser installations/state dedicated, and follow the repository's browser/Playwright recovery policy before dependent execution. Document-only preparation installs nothing.

Establish representative repeated context/page/teardown and Canvas/input execution in Phase 1 before browser-dependent growth. Exercise actual file downloads, HTTP(S) cookie/URL reloads and screenshots where relevant. Browser cookie restrictions and optional CDN failure have explicit error cases. Full/headed-browser/native-window evidence is outside the required matrix; disclose policy-excluded behavior without claiming it passed. A failure of feasible required evidence blocks the affected boundary.

Before SQLite implementation relies on a CDN artifact, verify the pinned JavaScript loader, embedded binary integrity and isolated worker startup. Bound file size/startup/decode time and inspect successful databases independently. Share validation between formats and compare pre/post results/settings/cookies/URL for rejection. Timing and penetration use deterministic edge fixtures so frame rate or random games do not conceal contract defects.

## Integration, versioning and releases

Project documents must pass package QC and be explicitly integrated into published `main` before the first implementation branch. Execute each phase on its corresponding `phase/<number>-<slug>` branch from its recorded published parent. When tracking is enabled, activate only that eligible phase's label/milestones/task issues before execution; future phases remain local plans.

Every task closes with its verified result/evidence and initial checkbox in one commit, followed by push/readback and issue closure. Finish delivery milestones before their phase review; close the review milestone after the phase review passes. Verify the full phase, then explicitly merge with two parents into `main`, check the merged state and publish/read back. Partial ranges remain on their phase branch.

After integration, prepare the exact release body/version on actual default `main`, create/publish its eligible release commit and tag, and publish the GitHub release with the U3 assets. Asset names stay version-free across releases; project-local direct/CI checks enforce the naming gate. Build and verify the single HTML/package from the pinned release source; inspect hosted metadata and download/check its final bytes/checksums. Report installation, verified browsers/modes, unavailable checks and limitations. Publication is not a prerequisite for an earlier phase-review task's own commit; it is a required subsequent coordinator operation before the next phase starts.

All seven release publications are within the requested overall project scope, but implementation executes only the task range actually authorized at its checkpoint. A failed push, missing required tracking transition, failed feasible check or uncertain hosted effect retains the current operation and blocks dependent advancement. Release patch repairs use an appropriate patch bump; planned capability additions use the versions above, ending with 1.0.0 when the complete target is delivered.
