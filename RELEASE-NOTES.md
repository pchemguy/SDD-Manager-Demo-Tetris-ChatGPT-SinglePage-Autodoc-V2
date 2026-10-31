Added real SQLite Save/Restore alongside JSON using a pinned integrity-checked sql.js runtime in an isolated worker with a ten-second deadline. Database metadata/schema/storage types and complete semantic content are validated before the shared restore transaction. JSON and gameplay remain independent of the optional library.

Download tetris.html directly or extract tetris-browser.zip. SHA256SUMS.txt covers the release assets. The JSON Schema is included separately and in the ZIP.

Verified locally with deterministic pytest checks and the actual application/package in Chromium headless shell and managed Firefox on Linux. Firefox uses the documented process-local sandbox override on this execution host. Native OS focus delivery and headed browsers were not tested. Settings persistence requires HTTP(S) and permitted cookies. SQLite requires access to the pinned CDN library; failure leaves JSON/gameplay usable.
