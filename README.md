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
