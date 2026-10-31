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
