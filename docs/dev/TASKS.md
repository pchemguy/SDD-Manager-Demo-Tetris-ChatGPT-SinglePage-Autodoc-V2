# Implementation tasks

Executable work derived from [PLAN](PLAN.md), [SPEC](SPEC.md) and [layout](layout.md). Each task has one owner, explicit prerequisites and observable completion evidence.

## Execution and evidence rules

Before the first task, complete whole-package documentation QC and verified published preparation integration into `main`, then activate the eligible phase tracking. A later phase also requires its predecessor review, milestone closures, integration and verified release. These are prerequisite gates in addition to task-ID dependencies; no future phase is activated by this list.

For every behavior change use the selected contract-driven test-first cycle, inspect RED/GREEN results, run applicable regressions and maintain truthful user/developer documentation. Each task completion commit contains only its verified result, evidence and initial owning checkbox; push/read back before issue closure or another task. Commands and browser provisioning are established through the actual isolated implementation environment, not assumed validated by this document.

A milestone boundary includes capability-wide code review, focused/regression checks, blocker repairs, a report with TODO disposition and HANDOFF in its own completion commit. A phase review waits for every delivery milestone to complete/close, not its own review milestone. It prepares release-ready source/notes/package evidence; integration, release commit/tag/publication and downloaded-byte verification follow as coordinator operations before the successor begins. See PLAN for their required gates.

## Phase 1 — Classic playable baseline

- [x] Phase 1 — Classic playable baseline
    - [x] Milestone 1.1 — Playable core
        - [x] T-001 — Establish the board geometry and startable Canvas game
            Scope: tetris.html core/markup/controller; tests/test_core.py and tests/test_browser.py; development harness/dependencies.
            Depends on: none. Contracts: G1, G2, U1, A1.
            Evidence: Start creates a correctly colored board/piece; masks, legal spawn and actual Canvas rasterization agree. Establish isolated Chromium/Firefox runner capability through repeated contexts and teardown before dependent browser checks.
        - [x] T-002 — Implement keyboard movement rotation and gravity
            Scope: tetris.html C1/C3/C7/C8; focused core/browser checks.
            Depends on: T-001. Contracts: G1 basic rotation, G3 failed policy, U2.
            Evidence: Left/right/down/rotation and chronological gravity respect wall/floor/stack bounds; handled keys do not scroll the game. Keep baseline rotation without kicks and independent uniform piece selection.
        - [x] T-003 — Complete locking line clearing scoring and game over
            Scope: tetris.html C1-C3; tests/test_core.py; relevant browser checks.
            Depends on: T-001, T-002. Contracts: G2, G3 failed policy, A1.
            Evidence: Observe single/multiple clears, score/level progression, spawn/above-top loss and exactly one game completion; demonstrate a complete playable run.
            Milestone exit: perform the complete 1.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/1/1.1.md`.
    - [x] Milestone 1.2 — Usable browser delivery
        - [x] T-004 — Implement pause resume restart and page focus lifecycle
            Scope: tetris.html C3/C7/C8; core/browser checks.
            Depends on: T-003. Contracts: G2-G3 baseline, U2, A1.
            Evidence: Pause freezes gravity; start/restart state is correct; document hiding/browser-window blur pause without automatic resume or elapsed-time catch-up. Form controls retain native keys.
        - [x] T-005 — Finish information controls help and readable resizing
            Scope: tetris.html markup/style/C7; tests/test_browser.py; README.md.
            Depends on: T-004. Contracts: U1 baseline information/two buttons, U2, A1.
            Evidence: Score/lines/level/status and exact bottom gameplay buttons render and work; keyboard help/focus/Canvas scale are readable. Optional panels/toggles remain deferred.
        - [x] T-006 — Package and verify the single HTML baseline
            Scope: tools/package.py, tests/test_artifacts.py, .github/workflows/verify.yml and release.yml, VERSION, README.md, docs/INSTALL.md.
            Depends on: T-004, T-005. Contracts: U3, scoped A8.
            Evidence: Build a clean version-consistent single-HTML browser ZIP and stable named/checksummed assets; exercise packaged HTML in both browsers and establish direct/CI artifact-name checks. Do not publish the phase release before review/integration.
            Milestone exit: perform the complete 1.2 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/1/1.2.md`.
    - [x] Milestone 1.3 — Phase review
        - [x] T-007 — Review test and report phase 1
            Scope: all phase 1 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF.
            Depends on: T-003, T-006 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/1/PHASE-REPORT.md`; update HANDOFF in this completion commit.

## Phase 2 — Modern rules

- [x] Phase 2 — Modern rules
    - [x] Milestone 2.1 — Bag hold and preview
        - [x] T-008 — Implement seven-bag generation and the shared queue
            Scope: tetris.html C2/C3; tests/test_core.py.
            Depends on: T-007. Contracts: G4, A2.
            Evidence: Deterministic shuffles contain every type once per bag; consume complete bags and reset correctly without a second RNG path.
        - [x] T-009 — Implement one-hold-per-piece and spawn transitions
            Scope: tetris.html C3/C7/C8; core/browser checks.
            Depends on: T-008. Contracts: G4, A2.
            Evidence: Empty/swap hold, used restriction, fresh spawn timing, reset and hold-induced spawn loss agree with G4; expose hold through keyboard only.
        - [x] T-010 — Render next and held piece previews from queue state
            Scope: tetris.html C3/C7; core/browser checks; README.md.
            Depends on: T-008, T-009. Contracts: G4, U1, A2.
            Evidence: Next reflects the next spawn without consumption; held type/orientation is correct; integrated bag/hold/preview remains deterministic and visibly readable.
            Milestone exit: perform the complete 2.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/2/2.1.md`.
    - [x] Milestone 2.2 — Landing and grounded timing
        - [x] T-011 — Implement the documented ordered wall kicks
            Scope: tetris.html C1; tests/test_core.py; browser checks.
            Depends on: T-010. Contracts: G1 kicks, A2.
            Evidence: Clockwise/counterclockwise, I/O behavior and fixed offset ordering pass wall/floor/stack fixtures; failed rotations preserve the original piece.
        - [x] T-012 — Share ordinary landing calculation with ghost rendering
            Scope: tetris.html C1/C3/C7; core/browser checks.
            Depends on: T-011. Contracts: G5 ordinary landing/ghost, A2.
            Evidence: Ghost is the last consecutively reachable valid row and never changes locked cells; omit coincident ghost and verify actual Canvas projection.
        - [x] T-013 — Implement keyboard hard drop and drop scoring
            Scope: tetris.html C1/C3/C8; core/browser checks.
            Depends on: T-012. Contracts: G2 hard-drop points, G5, A2.
            Evidence: Enter reaches the shared landing, awards distance once and handles zero distance; domain checks cover general/immediate policy paths while the UI uses fixed defaults.
        - [x] T-014 — Implement full grounded interval and event ordering
            Scope: tetris.html C3; tests/test_core.py; browser integration checks.
            Depends on: T-013. Contracts: G3, G5 locking, A2.
            Evidence: Check before/at deadline, nonreset grounded moves, lift/re-ground, pause, policy changes and coincident gravity/lock; modern default is general interval locking, with no old event applied to a successor.
        - [x] T-015 — Review landing and timing integration
            Scope: all 2.2 implementation, relevant queue/core consumers, tests and documentation.
            Depends on: T-011, T-012, T-013, T-014. Contracts: G1/G3/G5, A2 and PLAN 2.2 exits.
            Evidence: capability-wide code review separate from test execution, deterministic timing/landing regressions, blocker repairs and retained TODO disposition; include milestone report and HANDOFF with completion.
            Report: `docs/dev/reports/phases/2/2.2.md`.
    - [x] Milestone 2.3 — Phase review
        - [x] T-016 — Review test and report phase 2
            Scope: all phase 2 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF.
            Depends on: T-010, T-015 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/2/PHASE-REPORT.md`; update HANDOFF in this completion commit.

## Phase 3 — Configurable penetrator gameplay

- [x] Phase 3 — Configurable penetrator gameplay
    - [x] Milestone 3.1 — Session configuration
        - [x] T-017 — Add the six canonical session settings and controls
            Scope: tetris.html C4/C7/C8; tests/test_settings.py.
            Depends on: T-016. Contracts: CFG1 session-only, U1.
            Evidence: Exactly six typed keys/defaults and labeled controls exist; ordinary visibility/enablement flags apply, and invalid programmatic values are rejected without coercion.
        - [x] T-018 — Implement dynamic ghost visibility at the midline
            Scope: tetris.html C3/C7; core/browser checks.
            Depends on: T-017. Contracts: G5 dynamic mode, CFG4, A2.
            Evidence: All-above hides, any cell at/below row ten shows, and mode/movement/rotation changes re-evaluate visibility without changing landing or board.
        - [x] T-019 — Integrate live policy changes and session-only reload behavior
            Scope: tetris.html C3/C4/C8; tests/test_settings.py and browser checks; README.md.
            Depends on: T-017, T-018. Contracts: G3-G5, CFG1/CFG4, A4 session subset.
            Evidence: Exercise all six controls, hold retention, disabled actions and grounded policy timing; prove this increment neither reads nor writes configuration cookies/query parameters and reload restores defaults.
            Milestone exit: perform the complete 3.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/3/3.1.md`.
    - [x] Milestone 3.2 — Earned penetration
        - [x] T-020 — Award capped bonuses and render penetrator status
            Scope: tetris.html C3/C7; core/browser checks.
            Depends on: T-019. Contracts: G6 earning/cap/white display, U1, A3.
            Evidence: Four-line clear earns one, other clears earn none, cap is three and indicator updates; white is reserved for penetrator active/locked cells and ghost.
        - [x] T-021 — Implement activation and viable penetrating movement
            Scope: tetris.html C1/C3/C8; tests/test_core.py.
            Depends on: T-020. Contracts: G6 activation, G7 travel, A3.
            Evidence: One activation spends one bonus, repeated/empty activation is a no-op, barriers are traversed without erasure and proposed moves retain at least one legal eventual landing.
        - [x] T-022 — Integrate penetrator ghost drop hold and legal locking
            Scope: tetris.html C1/C3/C7; core/settings/browser checks; README.md.
            Depends on: T-020, T-021. Contracts: G3-G7, CFG4, A2-A3.
            Evidence: Ghost/drop/gravity agree on the lowest valid cavity, hold is excluded while active, all policy paths lock legally and successors are regular; demonstrate barrier traversal and bonus spending.
            Milestone exit: perform the complete 3.2 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/3/3.2.md`.
    - [x] Milestone 3.3 — Phase review
        - [x] T-023 — Review test and report phase 3
            Scope: all phase 3 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF.
            Depends on: T-019, T-022 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/3/PHASE-REPORT.md`; update HANDOFF in this completion commit.

## Phase 4 — Persistent configuration

- [x] Phase 4 — Persistent configuration
    - [x] Milestone 4.1 — URL and cookie settings
        - [x] T-024 — Resolve settings independently from URL cookies and defaults
            Scope: tetris.html C4/C9; tests/test_settings.py.
            Depends on: T-023. Contracts: CFG2, A4.
            Evidence: Mixed valid sources, omissions, explicit defaults, empty/repeated/invalid query values and invalid/duplicate cookies resolve per key with visible diagnostics and no saved-value loss.
        - [x] T-025 — Persist setting changes with browser write verification
            Scope: tetris.html C8/C9; tests/test_settings.py.
            Depends on: T-024. Contracts: CFG3-CFG4, A4.
            Evidence: Write canonical cookie/query encodings, preserve unrelated URL/cookies/fragment, verify writes and roll back recoverable failures without changing live state.
        - [x] T-026 — Verify reloads live integration and persistence limitations
            Scope: tetris.html diagnostics/C9; browser settings checks; README.md and docs/INSTALL.md.
            Depends on: T-024, T-025. Contracts: CFG1-CFG4, A4 persistent subset.
            Evidence: Real HTTP(S) reloads retain every setting including explicit defaults; invalid sources fall back correctly, live timing/hold behavior survives, and blocked-cookie/direct-file limitations are accurately shown/documented.
            Milestone exit: perform the complete 4.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/4/4.1.md`.
    - [x] Milestone 4.2 — Phase review
        - [x] T-027 — Review test and report phase 4
            Scope: all phase 4 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF.
            Depends on: T-026 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/4/PHASE-REPORT.md`; update HANDOFF in this completion commit.

## Phase 5 — Portable session results

- [x] Phase 5 — Portable session results
    - [x] Milestone 5.1 — Session leaderboard
        - [x] T-028 — Create stable completed-game records exactly once
            Scope: tetris.html C3/C6/C8; tests/test_core.py and test_persistence.py.
            Depends on: T-027. Contracts: G2 completion, F1, A5.
            Evidence: Generate canonical UUID/UTC/safe score records at game over only; repeated events and unfinished restarts do not add results.
        - [x] T-029 — Rank and retain the session top ten deterministically
            Scope: tetris.html C5/C6; tests/test_persistence.py.
            Depends on: T-028. Contracts: F1, A5.
            Evidence: Score/time/ID tie ordering, zero-score entries, truncation, stable identity and empty replacement are correct; no result history uses cookies/local storage.
        - [x] T-030 — Render and integrate the session leaderboard
            Scope: tetris.html C6-C8/markup; browser checks; README.md.
            Depends on: T-028, T-029. Contracts: F1, U1 leaderboard subset, A5.
            Evidence: Displayed ranks match records after several games/restarts; page reload empties results while configured settings remain; use text-only result rendering.
            Milestone exit: perform the complete 5.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/5/5.1.md`.
    - [x] Milestone 5.2 — JSON snapshot transfer
        - [x] T-031 — Define strict snapshot validation and the JSON Schema
            Scope: tetris.html C4/C5/embedded schema, tools/export_schema.py, schemas/tetris-save.schema.json, tests/test_persistence.py.
            Depends on: T-030. Contracts: F1-F2, CFG1, A5-A6.
            Evidence: Validate exact root/record/settings keys, version, UUIDs, duplicate IDs/JSON keys, safe integers and real canonical UTC timestamps; schema companion parity and structural/semantic rejection cases pass.
        - [x] T-032 — Download one complete JSON snapshot through Save
            Scope: tetris.html C10/C11/C7; browser persistence checks.
            Depends on: T-031. Contracts: F2/F4 JSON save, U1 Save location, A5.
            Evidence: Save captures current top ten/all settings, downloads exactly one tetris-save.json and changes no results/settings/cookies/URL; pause/cancellation/resource handling is correct.
        - [x] T-033 — Restore JSON atomically with complete failure handling
            Scope: tetris.html C5/C8-C11; persistence/settings/browser/artifact checks; README.md and docs/INSTALL.md.
            Depends on: T-031, T-032. Contracts: F2/F4-F5 JSON restore, CFG3, U1, A5-A6.
            Evidence: Complete candidate validation precedes replacement/browser writes; size/corruption/unknown fields/values and recoverable commit failures preserve state; busy/cancel paths clean up, actual downloads round trip, and schema enters the release package.
            Milestone exit: perform the complete 5.2 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/5/5.2.md`.
    - [x] Milestone 5.3 — Phase review
        - [x] T-034 — Review test and report phase 5
            Scope: all phase 5 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF.
            Depends on: T-030, T-033 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/5/PHASE-REPORT.md`; update HANDOFF in this completion commit.

## Phase 6 — SQLite snapshots

- [x] Phase 6 — SQLite snapshots
    - [x] Milestone 6.1 — SQLite snapshot transfer
        - [x] T-035 — Establish the pinned isolated SQLite worker runtime
            Scope: tetris.html embedded worker/C10/C11; tests/test_persistence.py and test_artifacts.py.
            Depends on: T-034. Contracts: U3 external boundary, F4 worker limits.
            Evidence: Verify pinned sql.js 1.13.0 asm.js CDN bytes/integrity and worker initialization; keep all app bootstrap inline, enforce operation ownership/deadline/termination and show optional-library failure without breaking JSON/gameplay.
        - [x] T-036 — Export versioned SQLite snapshots and the format choice
            Scope: tetris.html C10/C11/C7; persistence/browser checks.
            Depends on: T-035. Contracts: F3 export, F4 Save, CFG1 encodings, A5.
            Compatibility amendment: use pinned production sql.js1.14.2 JavaScript loader plus its embedded binary; the T035 asm initialization prototype failed Chromium SQL execution. See DOCS_PREPARATION and ARCHITECTURE.
            Evidence: Create exact tables/types/metadata and all six unique textual settings rows, preserve record IDs/UTC/scores and download one actual tetris-save.sqlite; expose both Save formats.
        - [x] T-037 — Validate SQLite imports through the shared restore transaction
            Scope: tetris.html C5/C8/C10; persistence/browser checks.
            Depends on: T-036. Contracts: F3 decode, F4 restore, CFG3, A5-A6.
            Evidence: Detect bytes rather than extension; inspect schema/integrity/storage types/metadata/limits without file SQL execution, decode exact scores and reject invalid rows before applying the shared candidate.
        - [x] T-038 — Complete cross-format fault coverage and resource cleanup
            Scope: tetris.html C10/C11 integration as needed; tests/test_persistence.py and test_artifacts.py; README.md and docs/INSTALL.md.
            Depends on: T-035, T-036, T-037. Contracts: F1-F5 complete, A5-A6/A8 scoped.
            Evidence: Independently inspect exports with Python sqlite3, cross-restore both formats, exercise corrupt/extra-schema/missing/duplicate/CDN/timeout/cancel/busy cases in both browsers, verify unchanged-state failures and worker/URL/database cleanup, and update install/package limits.
            Milestone exit: perform the complete 6.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/6/6.1.md`.
    - [x] Milestone 6.2 — Phase review
        - [x] T-039 — Review test and report phase 6
            Scope: all phase 6 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF.
            Depends on: T-038 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/6/PHASE-REPORT.md`; update HANDOFF in this completion commit.

## Phase 7 — Centered panel layout

- [x] Phase 7 — Centered panel layout
    - [x] Milestone 7.1 — Centered optional panels
        - [x] T-040 — Arrange five panels around a fixed board center
            Scope: tetris.html markup/style/C7; tests/test_browser.py.
            Depends on: T-039. Contracts: U1 panel order/geometry, A7.
            Evidence: Left-to-right order and symmetric side regions keep board centered with mandatory information visible; optional overflow never covers those mandatory regions.
        - [x] T-041 — Add individual panel toggles and preserve input focus
            Scope: tetris.html C7/C8; browser checks.
            Depends on: T-040. Contracts: U1 toggles/file buttons, U2 focus, A7.
            Evidence: Three toggles sit above the exact gameplay row; all eight combinations preserve state/centering, Settings hides its only Save/Restore pair, and focus/keyboard remain usable after hiding a focused panel.
        - [x] T-042 — Verify responsive accessible layout and final packaging
            Scope: tetris.html C7 as needed; tests/test_browser.py and test_artifacts.py; README.md and docs/INSTALL.md.
            Depends on: T-040, T-041. Contracts: U1-U3, A7/A8.
            Evidence: Inspect screenshots/Canvas/labels/focus and geometry at all specified widths/device pixel ratios and visibility combinations; package actual final HTML/schema and show accurate full-scope installation/help.
            Milestone exit: perform the complete 7.1 code review/testing/repair/report and update HANDOFF before this task closes; include all milestone exit evidence from PLAN.
            Report: `docs/dev/reports/phases/7/7.1.md`.
    - [x] Milestone 7.2 — Phase review
        - [x] T-043 — Review test and report phase 7
            Scope: all phase 7 implementation/milestone exits, release-ready notes/version/package, reports and HANDOFF, plus final complete-project report and aggregated unresolved/deferred TODOs.
            Depends on: T-042 and verified completion/closure of every delivery milestone in this phase.
            Evidence: independent code review of cross-milestone behavior, applicable PLAN/SPEC acceptance and packaged-HTML regressions, resolved blockers, explicit browser/evidence limits and release-ready source. Do not claim the later merge or hosted release already occurred.
            Report: `docs/dev/reports/phases/7/PHASE-REPORT.md`; update HANDOFF in this completion commit.
            Final report: `docs/dev/reports/IMPLEMENTATION-REPORT.md`, with A1-A8 coverage and complete TODO aggregation/provenance.

## Completion boundary

A partial task range ends at its selected boundary with published verified work; it does not integrate an incomplete phase. The complete list ends after phase 7 review, final report, verified integration and final release/download checks, with evidence limits stated. No further feature or revision campaign is implied.
