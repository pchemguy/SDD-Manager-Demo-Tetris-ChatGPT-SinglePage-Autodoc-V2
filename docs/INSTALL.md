# Install and play

Download `tetris-browser.zip`, extract it to a folder, and open `tetris.html` in a desktop Chromium or Firefox browser. You can also download the standalone HTML. No Node.js installation or development server is required to play.

For static HTTP(S) hosting, serve the extracted folder with any static web host. Later cookie/URL configuration features require a browser context that permits cookies; direct-file behavior is browser-dependent. This baseline has no saved settings or leaderboard.

## Baseline controls

- Left/Right: move.
- Down: soft drop.
- Up, Space or X: rotate clockwise; Z: rotate back.
- P or Escape: pause/resume; R: restart.
- Start/Restart starts a fresh game. The right Pause/Start button pauses or resumes.

Click the board or start/resume to focus gameplay. Other form controls retain native keyboard behavior. Document hiding or window blur pauses the game; returning does not resume automatically.

The baseline includes score, lines, level and game over. Hold, next preview, ghost, seven-bag, wall kicks, hard drop, penetrator, settings, results transfer and optional-panel toggles are planned later releases.

## Artifact verification

`SHA256SUMS.txt` lists the exact standalone HTML and browser ZIP hashes. Verify them with any SHA-256 utility before installation. Release filenames remain stable; tags and the embedded application version identify the release. Development tooling and credentials are excluded from the ZIP.

Verification uses isolated Chromium headless shell and Firefox on Linux. Native OS window focus delivery and full/headed browsers are not part of that evidence. Firefox tests on the current restricted host require a diagnosed, process-local content-sandbox override for trusted local pages; ordinary supported hosts use normal browser settings.

Modern controls: C holds once per piece, Enter hard drops, and the dim ghost previews the shared landing. Seven-bag generation and ordered wall kicks are active. A grounded piece receives a full gravity interval before locking; moving along the floor does not restart that delay.

Persistent configuration increment: each of the six settings resolves independently from a valid explicit URL parameter, then a valid saved cookie, then its default. Explicit defaults are saved; omitted parameters retain saved values. Changes update only their parameter and cookie, preserving other raw query text and the fragment. Invalid/repeated values produce diagnostics and fall back. Serve through HTTP(S) with cookies permitted for persistent changes and later restores; direct-file and blocked-cookie environments cannot guarantee persistence. Write failures retain live settings and attempt verified rollback, reporting any browser-blocked recovery. Gameplay remains usable if cookie reads fail.

JSON snapshots: Save downloads one tetris-save.json with formatVersion1, the current top ten and all six settings. Restore replaces results and settings only after complete structural/semantic validation; stable IDs and canonical UTC timestamps are retained. The supplied tetris-save.schema.json matches the embedded schema. Files over1MiB, malformed UTF-8, duplicate keys/IDs, unsafe or fractional numbers, invalid dates and unknown fields/values are rejected. File operations pause a running game and leave it paused for explicit resume; cancel or failure releases the controls. Restoring does not restore the active game. SQLite is added in the next increment.

SQLite snapshots: choose JSON or SQLite in Settings, then Save one file. Restore detects content rather than filename. SQLite uses sql.js1.14.2 with an integrity-checked JavaScript loader from jsDelivr and its matching binary embedded in this HTML. No separate binary asset is needed. Each isolated operation, including startup, has a ten-second deadline and files are limited to1MiB. Database metadata, schema, indexes, storage types and exact integer values are validated before the same atomic settings/results commit as JSON. Optional library/network failure affects only SQLite. The embedded upstream MIT notice is retained; see the runtime amendment for verified bytes and compatibility rationale.
