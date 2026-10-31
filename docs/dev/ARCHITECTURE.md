# Application architecture

## Context and packaging

Implement the [project brief](PROJECT.md) as one self-contained application HTML document. Its inline CSS, semantic panel markup and inline JavaScript contain all project-owned runtime code. A Canvas displays the board and piece previews; HTML displays information, settings, help, errors and leaderboard entries. Named sections and lexical component boundaries preserve maintainability without requiring a production bundler, application server or module files.

Development-only tests and release tools may be separate files. The JSON Schema is both embedded in the application and supplied as an inspectable release companion; a consistency check prevents the two representations from drifting. Neither the schema companion nor development tooling is required to start the game.

## Blocks and directed dependencies

| Block | Responsibility | Dependencies |
| --- | --- | --- |
| Game domain | Board/piece rules, legal positions, landing, rotation, hold, randomizer, score, bonuses, game lifecycle and logical time | Explicit settings, injected random source and elapsed active time; no DOM, storage, network or wall clock |
| Application controller | Serialize keyboard/button/settings commands, advance active time, own the current game and session results, coordinate restore commits | Game domain, configuration service, snapshot model, rendering and browser adapters |
| Presentation | Paint game snapshots, render accessible HTML information, capture user intent and control panel visibility | Read-only domain/controller snapshots; send commands to controller rather than mutate state |
| Snapshot model and codecs | Define/validate the complete results/settings snapshot and encode/decode JSON or SQLite | Pure shared validation; isolated SQLite library for SQLite operations |
| Browser adapters | Cookie and URL synchronization, download/file selection, clock/events, crypto IDs and bounded codec-worker execution | Browser APIs; report typed outcomes to controller |

Dependency direction points inward toward the domain and shared validation. Rendering does not implement collision rules. A single landing calculation serves gravity targeting, hard drop and ghost projection, including penetrators; adapters cannot define alternate rules. `DECOMPOSITION.md` details logical components and verification seams.

## State ownership and time

The controller owns the live page session and is the only entry point for commands. The game domain owns board, active/held/queued pieces, score, level, bonuses and simulation timing. Configuration owns the six effective settings. The leaderboard owns completed-result records; file persistence transfers results/settings only, never an active game, board, randomizer or elapsed lock delay. Panel visibility is presentation state and is outside the six exported settings.

Inject randomness and active elapsed milliseconds into the domain to make rule boundaries reproducible. Pause and document hiding stop active time. Wall-clock UTC is used only when creating completed-result records. Grounded timing is independent of the ordinary gravity accumulator, so partial gravity periods do not shorten a newly started lock delay.

## Persistence and restore transaction

JSON and SQLite codecs produce the same candidate snapshot. Decode, validate the entire format/schema and every field, normalize result order, and prepare configuration side effects before committing. Workers and codecs never mutate live results, configuration, cookies or URL state.

The controller checks a candidate through the shared snapshot validator, then commits settings/results and their browser representations through the configuration adapter. Preserve prior settings, leaderboard, relevant cookie values and URL until commit succeeds. Roll back owned effects if a browser write fails; report any inability of the browser environment to retain cookies rather than claiming persistence. A validation rejection has no commit side effects. A busy operation token prevents concurrent restores from applying out of order.

SQLite work executes in a disposable Blob worker whose project-owned bootstrap is embedded in the HTML. It imports the pinned `sql.js@1.13.0/dist/sql-asm.js` library from jsDelivr. The [upstream versioned documentation](https://github.com/sql-js/sql.js/blob/v1.13.0/README.md) identifies this as a single-JavaScript compatibility build. This choice favors the one-file deployment constraint over WASM's performance advantage for a snapshot containing at most ten results and six settings. Release verification pins the actual URL and integrity digest. No library version or CDN fallback is selected dynamically.

Enforce input-size and operation-time limits; terminate the owned worker on timeout and release statements/databases after use. Read only the declared SQLite tables after inspecting metadata and schema. Never execute SQL supplied by a file. CDN failure disables only the requested SQLite operation, leaving the game and JSON transfer usable. No network is needed for gameplay, JSON transfer or configuration after loading the HTML.

## Design rationale and invariants

- Vanilla JavaScript, Canvas and HTML fit the accepted delivery constraint; a UI framework/build pipeline would add runtime and packaging complexity without a required capability.
- Pure rule functions and injected time/randomness permit deterministic unit checks, while browser checks exercise the same inline application code.
- Shared snapshot validation makes JSON/SQLite acceptance equivalent; format-specific parsing does not duplicate gameplay settings or leaderboard rules.
- A worker bounds untrusted SQLite parsing and keeps it outside the rendering/input loop. File size and schema restrictions reduce the amount of work admitted.
- Every locked piece has four in-board, non-overlapping cells. Penetration affects travel, never the locked-board representation.
- Rule configuration, landing logic, persistence validation and score ordering each have one authoritative implementation.
- Browser failures have explicit results; catching an exception is not evidence that a save, restore or cookie write succeeded.

The `SPEC.md` will own observable behavior and exact error/data contracts; the delivery plan owns phase ordering and layout owns physical paths. No additional architectural children are needed for this application.
