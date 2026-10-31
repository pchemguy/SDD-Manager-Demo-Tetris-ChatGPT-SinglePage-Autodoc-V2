Completed the five-panel layout with separate visibility toggles, centered board and mandatory game information. Save/Restore follows Settings visibility. The full requested classic/modern/penetrator gameplay, six persistent settings, session leaderboard and JSON/SQLite transfer are delivered.

Download tetris.html directly or extract tetris-browser.zip. SHA256SUMS.txt covers the release assets. The JSON Schema is included separately and in the ZIP.

Verified locally with deterministic pytest checks and the actual application/package in Chromium headless shell and managed Firefox on Linux. Firefox uses the documented process-local sandbox override on this execution host. Native OS focus delivery and headed browsers were not tested. Settings persistence requires HTTP(S) and permitted cookies. SQLite requires access to the pinned CDN library; failure leaves JSON/gameplay usable.
