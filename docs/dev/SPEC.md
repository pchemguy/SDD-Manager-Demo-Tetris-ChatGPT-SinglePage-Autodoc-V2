# Tetris system specification

## Scope and contract owners

Deliver the browser application defined in [PROJECT](PROJECT.md), using [ARCHITECTURE](ARCHITECTURE.md) and the C1–C11 boundaries in [DECOMPOSITION](DECOMPOSITION.md). Requirements describe the complete product; PLAN assigns the independently releasable subsets.

| Contract group | Canonical owner | Participating components |
| --- | --- | --- |
| G1–G7: board, game lifecycle, modern rules, timing, penetrator | [Gameplay](spec/gameplay.md) | C1–C3, C6–C8 |
| CFG1–CFG4: six settings, resolution, browser persistence and live application | [Configuration](spec/configuration.md) | C4, C8–C9 |
| F1–F5: session results, JSON/SQLite, validation and file operations | [Persistence](spec/persistence.md) | C5–C6, C8–C11 |
| U1–U3: panels, input/presentation, delivery and supported verification | This root | C7–C8, C11 and release tooling |

No account, backend, desktop package, extension, multiplayer or online leaderboard is included. Neither active-game saves nor automatic file writes are included.

## U1 — Panels and visible controls

The logical left-to-right order is Leaderboard, Game info and controls, Board, Settings, Controls/help. Keep the board's horizontal center at the viewport's horizontal center, within two CSS pixels, regardless of the eight visibility combinations of the three optional panels. Keep the information panel adjacent on the left and the board/information visible. Use symmetric side regions; optional overflow may scroll within its side region without moving the board or covering the mandatory information panel. At viewport widths 480, 640, 800, 1024, 1440 and 1920 CSS pixels, fit the mandatory board/information horizontally without page-level horizontal scrolling; reduce board size as necessary. Vertical scrolling is allowed. Canvas backing resolution follows device pixel ratio without changing board-cell geometry.

Show score, total lines, level, status, enabled hold/next previews and one lightning symbol per available bonus in the information panel. Place separate Leaderboard, Settings and Controls/help visibility toggle buttons immediately above its bottom gameplay row. The bottom row has exactly two gameplay buttons: left Start when idle and Restart otherwise; right Start when idle/paused/game over and Pause while running. Start from idle/game over creates a game; right Start from paused resumes. No mouse/touch buttons control movement, rotation, drop, hold or penetration. Optional-panel visibility is page-session presentation state, initially shown, and is not exported or persisted as a seventh setting.

Settings has six labeled gameplay controls. One export-format selector (JSON/SQLite) and exactly one Save/Restore button pair occupy its bottom; they disappear when Settings is hidden. Before a format's delivery increment, show only supported export choices. Leaderboard and help use readable text; help lists every gameplay key and explains focus. Give Canvas a textual status/description, visible focus, and HTML alternatives for score/status/previews. Do not announce every animation frame to assistive technology. Imported IDs/error text are rendered as text.

## U2 — Input and page lifecycle

With the game region focused, use Left/Right for horizontal motion, Down for soft drop, Up/Space/X for clockwise rotation, Z for counterclockwise rotation, Enter for hard drop, C for hold, B for penetrator, P/Escape for pause/resume and R for start/restart. Hold/rotation/drop/penetrator/pause/restart ignore repeated keydown events; motion/soft drop may use native key repeat. Prevent browser scrolling for handled game keys. Inputs/selects/textareas and other focused controls retain their native keyboard behavior; gameplay shortcuts do not run while they are being edited/activated. Starting/resuming through a gameplay button focuses the game region.

Hide/blur automatically pauses a running game and clears pending held-input state. Returning does not automatically resume. Pause freezes gravity and lock time; frame resumption does not fast-forward hidden time. A file operation pauses a running game and leaves it paused for explicit resume. Invalid/disabled gameplay actions leave the game unchanged.

## U3 — Delivery and verification boundaries

Provide `tetris.html`, containing all project-owned HTML, CSS and JavaScript. No external app module, CSS, worker file, image/font or separate WASM asset is required. Only the pinned sql.js JavaScript library may be loaded from its established CDN for SQLite operations. Gameplay, JSON transfer and settings remain available if that library cannot load. Users need a desktop browser and static hosting for supported cookie behavior, without Node.js or a development server. Explain direct-file cookie limitations.

Verify in isolated Chromium headless shell and managed Firefox using the actual released HTML; test timing deterministically at the domain seam and real browser input/Canvas/download/cookie/URL behavior. Exercise representative fresh browser contexts and teardown. Browser-dependent implementation proactively establishes the policy-compliant runner and capabilities; documentation preparation does not require browser installation. Full/headed browser checks are not required for these web capabilities. Apply repository policy for diagnosed unavailable full-browser behavior; disclose unverified behavior separately. Feasible required checks that fail remain blockers.

Each completed, verified and integrated phase produces a versioned GitHub release. Use stable, version-free asset names `tetris.html`, `tetris-browser.zip` and `SHA256SUMS.txt`; supply `tetris-save.schema.json` with file-persistence releases. The ZIP contains the HTML, applicable schema, license and installation instructions, without source-only tools, credentials or caches. Verify the packaged HTML and downloaded release bytes, archive contents, version, checksums, actual asset names and installation path before claiming delivery.

## End-to-end acceptance

| ID | Observable acceptance |
| --- | --- |
| A1 | Start, play with keyboard, clear lines, progress levels, pause/resume and restart; score and game-over behavior agree with G1–G3. |
| A2 | Deterministic sequences exercise seven-bag, one-hold-per-piece, kicks, hard drop and exact lock boundaries; ghost/hard drop share ordinary and penetrator landings under all relevant settings. |
| A3 | A four-line clear earns one bonus up to three; activation consumes one, white travel crosses a blocking row, hold is unavailable while active, and every lock remains legal. |
| A4 | Session-only settings do not survive reload. Persistent settings resolve independently URL/cookie/default; default-valued explicit parameters, omissions and invalid values behave as CFG2 requires. |
| A5 | Completed games rank deterministically, retain stable IDs/timestamps and truncate to ten; unfinished restarts add no result. JSON and SQLite round trips replace the session leaderboard and all settings equivalently. |
| A6 | Every malformed/unsupported/inconsistent/resource-exceeding restore is rejected before commit; observed results, settings, relevant cookies and full URL remain byte/value equivalent to their pre-restore state. |
| A7 | Every optional-panel combination preserves board centering and mandatory visibility; Save/Restore follows Settings visibility and gameplay controls remain limited to the prescribed two buttons. |
| A8 | The released one-HTML artifact works in both required browsers under the feasible matrix, including actual downloads/reloads, and the release's downloaded artifacts match its verified package/checksums. |
