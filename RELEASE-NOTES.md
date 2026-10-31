Added the session top-ten leaderboard and manual JSON Save/Restore. Stable IDs, safe integer scores and canonical UTC completion times are preserved. Complete strict validation, duplicate-key detection, a companion JSON Schema and transactional settings updates protect failed restores.

Download tetris.html directly or extract tetris-browser.zip. SHA256SUMS.txt covers the release assets. The JSON Schema is included separately and in the ZIP.

Verified locally with deterministic pytest checks and the actual application/package in Chromium headless shell and managed Firefox on Linux. Firefox uses the documented process-local sandbox override on this execution host. Native OS focus delivery and headed browsers were not tested. Settings persistence requires HTTP(S) and permitted cookies.
