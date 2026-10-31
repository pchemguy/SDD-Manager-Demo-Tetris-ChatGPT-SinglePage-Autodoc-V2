# Single-page HTML Tetris

## Purpose and outcome

Provide a keyboard-controlled Tetris game for individual players in a desktop web browser. The application is delivered as one well-organized HTML file with its application markup, styling and JavaScript embedded. Players can play immediately, configure the rules, inspect the session leaderboard, and manually transfer results and configuration between sessions.

## Principal scope

The classic playable baseline provides a falling-piece board, movement, rotation, line clearing, scoring, levels, game over, restart and pause/resume. A Game info and controls panel displays standard game information. Its bottom row contains only two clickable gameplay controls: Start/Restart on the left and Pause/Start on the right. All other gameplay actions use the keyboard.

Modern rules add hold, next-piece preview, ghost projection, seven-bag randomization, wall kicks and hard drop. The general locking policy supports either a failed downward attempt or one full gravity interval after becoming grounded. Hard drop follows that policy unless immediate locking is selected. Grounded movement and rotation do not restart the delay; lifting off clears it, and pausing freezes its remaining time.

A conditional ghost mode hides the projection only when all its cells are above the board's midline. A projection straddling the midline remains visible.

Clearing four lines awards one penetrator bonus, with at most three accumulated. A keyboard activation spends one bonus to make the current piece entirely white until it locks. Regular pieces never use white. The penetrator passes through occupied cells without destroying them, but its final locked position must be entirely within the board and free of overlap. Its ghost and hard drop share the same lowest valid landing. Repeated activation has no effect, and hold is disabled while the penetrator is active. The information panel shows one symbol per available bonus and updates when bonuses are earned or spent.

The settings panel controls six settings: ghost visibility, hard-drop enablement, next-preview enablement, hard-drop locking policy, general locking policy and hold enablement. Settings apply immediately; changing the locking policy while grounded starts timing afresh. Delivery includes a session-only configuration increment before persistence is added.

Persist each setting independently using explicit URL value, then saved cookie, then default. Setting changes update the corresponding cookie and URL parameter. Explicit valid URL values are saved to cookies even when equal to defaults; omitted parameters retain cookie values. Invalid URL values produce a clear message and fall back independently to a valid cookie or default.

The leaderboard contains the ten highest completed-game scores for the current page session. Game over completes a run; restarting an unfinished game discards it. Results retain stable IDs, non-negative integer scores and UTC completion timestamps.

A single Save/Restore button pair sits at the bottom of the settings panel and disappears with that panel. Save offers JSON or SQLite, downloading one file containing the current top ten and all six settings. Restore accepts either format, replaces session results, applies settings, and updates cookies and URL parameters. JSON has a format version, results array, settings object and supplied JSON Schema. SQLite has `high_scores(id, score, timestamp)`, uniquely keyed `settings(key, value)` rows, and metadata versioning. Complete validation, including timestamps and setting values, precedes every restore mutation; failure leaves results, settings, cookies and URL parameters unchanged and displays an error.

## Presentation and delivery constraints

Arrange panels left to right: Leaderboard; Game info and controls; Board; Settings; Controls/help. Keep the board centered when optional panels change visibility, with the board and information panel visible. Place separate show/hide toggles for the three optional panels immediately above the two gameplay buttons.

Use embedded JavaScript/CSS, a Canvas board and ordinary HTML panels. External dependencies are limited to widely used JavaScript libraries from established CDNs. The delivered game requires no application server or separate Node.js installation; static HTTP(S) hosting is the supported environment for cookie/URL persistence verification. Direct file opening may limit cookies under browser policy.

Deliver the simplest sensible playable baseline first, then bounded useful increments until the full scope is complete. Select and maintain semantic versions and publish a new GitHub release with its tag and release notes after each phase is completed, verified and integrated. Each release must make its single HTML application available as a deployable artifact. Include the JSON Schema when the file-persistence capability is delivered.

## Boundaries and design ownership

This project delivers the browser game. It includes no desktop package, extension, account service, multiplayer, online leaderboard or automatic result-file saving. Session leaderboard history survives only through a manual save and later restore.

Detailed defaults, keyboard mappings, scoring progression, rotation/kick tables, data encodings, resource bounds, responsive presentation and acceptance checks belong in the design and specification. They must preserve the interactions and constraints above. No unresolved material decision prevents the project brief from being reviewed.
