# Single-page HTML Tetris

A browser Tetris project targeting one HTML file with embedded application HTML, CSS and JavaScript. The intended scope includes modern rules, a penetrator ability, configurable gameplay, a session leaderboard, and manual JSON/SQLite save and restore.

The project is in documentation preparation. No playable application or release has been delivered yet.

## Project documents

Read the [project brief](docs/dev/PROJECT.md), [architecture](docs/dev/ARCHITECTURE.md), [component model](docs/dev/DECOMPOSITION.md), [specification](docs/dev/SPEC.md), [delivery plan](docs/dev/PLAN.md), [repository layout](docs/dev/layout.md) and [implementation tasks](docs/dev/TASKS.md) for the intended product. See the [preparation record](docs/dev/DOCS_PREPARATION.md) for current decisions and pending approvals. The [handoff](docs/dev/HANDOFF.md) provides workflow continuity.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md).

## Development checks

Board spawning, keyboard movement/rotation and elapsed-time gravity are implemented; locking/clearing and the remaining rules follow the next tasks. Development dependencies are pinned in `requirements-dev.txt` and installed into the ignored `.dev/python` target. Production remains one HTML file.

On this Linux execution host the verified test command is:

```sh
PYTHONPATH="$PWD/.dev/python" PLAYWRIGHT_BROWSERS_PATH="$PWD/.dev/browsers" TETRIS_FIREFOX_SANDBOX=off python -m pytest -q
```

The Firefox override is limited to trusted local tests on this host after its normal content processes failed with `/proc/self/uid_map: EPERM`; it is not a general browser default. Browsers are managed builds matching Playwright 1.56.0, installed in the dedicated project directory. Chromium uses the headless shell. The initial installer returned an invalid first archive, then hit a lock heartbeat failure; verified complete official fallback archives were extracted without changing host restrictions. Browser provenance/digests are retained in the T-001 report. Re-evaluate the override on other hosts and follow the repository browser policy.
