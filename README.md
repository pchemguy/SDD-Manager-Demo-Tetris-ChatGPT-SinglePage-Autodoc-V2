# Single-page HTML Tetris

A browser Tetris project targeting one HTML file with embedded application HTML, CSS and JavaScript. The intended scope includes modern rules, a penetrator ability, configurable gameplay, a session leaderboard, and manual JSON/SQLite save and restore.

The classic playable baseline is available in `tetris.html`. Modern capabilities are delivered in subsequent bounded releases.

## Project documents

Read the [project brief](docs/dev/PROJECT.md), [architecture](docs/dev/ARCHITECTURE.md), [component model](docs/dev/DECOMPOSITION.md), [specification](docs/dev/SPEC.md), [delivery plan](docs/dev/PLAN.md), [repository layout](docs/dev/layout.md) and [implementation tasks](docs/dev/TASKS.md) for the intended product. See the [preparation record](docs/dev/DOCS_PREPARATION.md) for current decisions and pending approvals. The [handoff](docs/dev/HANDOFF.md) provides workflow continuity.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md).

## Development checks

The classic core implements spawning, keyboard movement/rotation, gravity, legal locking, line clearing, score/level progression, game over and restart. Pause/resume, automatic page/window-event pause and restart are implemented. The information panel shows score, lines and level; keyboard help and high-DPI responsive Canvas sizing are implemented. Releases and later capabilities follow the task plan. Development dependencies are pinned in `requirements-dev.txt` and installed into the ignored `.dev/python` target. Production remains one HTML file.

On this Linux execution host the verified test command is:

```sh
PYTHONPATH="$PWD/.dev/python" PLAYWRIGHT_BROWSERS_PATH="$PWD/.dev/browsers" TETRIS_FIREFOX_SANDBOX=off python -m pytest -q
```

The Firefox override is limited to trusted local tests on this host after its normal content processes failed with `/proc/self/uid_map: EPERM`; it is not a general browser default. Browsers are managed builds matching Playwright 1.56.0, installed in the dedicated project directory. Chromium uses the headless shell. The initial installer returned an invalid first archive, then hit a lock heartbeat failure; verified complete official fallback archives were extracted without changing host restrictions. Browser provenance/digests are retained in the T-001 report. Re-evaluate the override on other hosts and follow the repository browser policy.

## Browser package

Build and inspect the stable browser release assets with:

```sh
python tools/package.py
python tools/package.py --check
```

Both commands and the packaged HTML were verified locally. The ZIP contains `tetris.html`, `LICENSE` and `INSTALL.md`; `dist/SHA256SUMS.txt` covers the standalone HTML and ZIP. See [installation](docs/INSTALL.md). The verify workflow runs tests and the independent naming gate; the manually dispatched release workflow is build-only and checks an existing release tag. SDD Manager owns release publication, followed by exact downloaded-byte/latest-link checks. No hosted release or live CI result is claimed before its observed completion.

Published and verified: [v0.1.0](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/tag/v0.1.0).

Modern increment: a seven-bag queue, once-per-piece keyboard hold (C), and next/held shape previews are implemented.

Phase 2 delivered: Added seven-bag randomization, once-per-piece hold and shape previews, ordered wall kicks, ghost projection, keyboard hard drop and a full gravity interval of grounded lock delay. Keyboard event timing preserves fresh incoming pieces and processes elapsed time chronologically.

Published and verified: [v0.2.0](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/tag/v0.2.0).

Session configuration increment: six settings apply immediately in memory. This phase deliberately does not read or write setting cookies/query parameters; reload restores defaults. Dynamic ghost hides only when every projected cell is above row ten.

Penetrator increment: clearing four rows awards one bonus up to three; B spends one. White pieces cross intact stacks, cannot be held, and use their lowest fully legal landing for gravity, ghost and hard drop. The ordinary lock policy still applies.

Phase 3 delivered: Added six session-only game settings, dynamic midline ghost visibility and earned penetrator bonuses (up to three). White penetrators cross occupied barriers and share the lowest valid landing across gravity, ghost and hard drop; active penetrators cannot be held.

Published and verified: [v0.3.0](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/tag/v0.3.0).

Persistent configuration increment: each of the six settings resolves independently from a valid explicit URL parameter, then a valid saved cookie, then its default. Explicit defaults are saved; omitted parameters retain saved values. Changes update only their parameter and cookie, preserving other raw query text and the fragment. Invalid/repeated values produce diagnostics and fall back. Serve through HTTP(S) with cookies permitted for persistent changes and later restores; direct-file and blocked-cookie environments cannot guarantee persistence. Write failures retain live settings and attempt verified rollback, reporting any browser-blocked recovery. Gameplay remains usable if cookie reads fail.

Phase 4 delivered: Added independent URL/cookie/default configuration resolution for all six settings, explicit-default saving and canonical updates. Invalid or repeated sources report diagnostics; recoverable browser-write failures roll back without applying live changes.

Published and verified: [v0.4.0](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/tag/v0.4.0).

Session leaderboard: completed games receive one cryptographically generated UUIDv4 and UTC completion timestamp. The ten best scores rank by score descending, time ascending and ID ascending. Restarting an unfinished game adds nothing; reloading clears results while retaining configured settings.

JSON snapshots: Save downloads one tetris-save.json with formatVersion1, the current top ten and all six settings. Restore replaces results and settings only after complete structural/semantic validation; stable IDs and canonical UTC timestamps are retained. The supplied tetris-save.schema.json matches the embedded schema. Files over1MiB, malformed UTF-8, duplicate keys/IDs, unsafe or fractional numbers, invalid dates and unknown fields/values are rejected. File operations pause a running game and leave it paused for explicit resume; cancel or failure releases the controls. Restoring does not restore the active game. SQLite is added in the next increment.

Phase 5 delivered: Added the session top-ten leaderboard and manual JSON Save/Restore. Stable IDs, safe integer scores and canonical UTC completion times are preserved. Complete strict validation, duplicate-key detection, a companion JSON Schema and transactional settings updates protect failed restores.

Published and verified: [v0.5.0](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/tag/v0.5.0).

SQLite runtime compatibility: the production sql.js1.14.2 loader is pinned to jsDelivr and verified with Fetch integrity. Its matching binary is embedded in tetris.html; no separate binary request is required. The upstream MIT notice is retained in the HTML. The initial asm prototype was replaced after minimal Chromium SQL execution failed; see the phase6 runtime amendment.
