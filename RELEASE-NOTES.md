Added independent URL/cookie/default configuration resolution for all six settings, explicit-default saving and canonical updates. Invalid or repeated sources report diagnostics; recoverable browser-write failures roll back without applying live changes.

Download tetris.html directly or extract tetris-browser.zip. SHA256SUMS.txt covers the release assets.

Verified locally with deterministic pytest checks and the actual application/package in Chromium headless shell and managed Firefox on Linux. Firefox uses the documented process-local sandbox override on this execution host. Native OS focus delivery and headed browsers were not tested. Settings persistence requires HTTP(S) and permitted cookies.
