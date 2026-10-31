# Single-page Tetris

A complete keyboard Tetris game in one HTML file. It includes seven-bag randomization, hold and next previews, ordered wall kicks, ghost projection, hard drop, configurable grounded locking, earned white penetrators, six persistent settings, a session top-ten leaderboard and manual JSON/SQLite snapshots.

[Download the game](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/latest/download/tetris.html) or [download the ZIP](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/latest/download/tetris-browser.zip). No build or Node.js is needed. See [installation and usage](docs/INSTALL.md). The [JSON Schema](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/latest/download/tetris-save.schema.json) and checksums are release assets; the ZIP also includes the schema, license and installation guide.

## Play

Click Start or the board to focus it. All piece actions use the keyboard.

| Key | Action |
| --- | --- |
| Left / Right | Move |
| Down | Soft drop |
| Up / Space / X | Rotate clockwise |
| Z | Rotate counterclockwise |
| Enter | Hard drop when enabled |
| C | Hold once per piece when enabled |
| B | Spend one penetrator bonus |
| P / Escape | Pause or resume an existing game |
| R | Start/restart |

Clearing four lines earns one bonus, up to three. An activated penetrator is white, crosses occupied cells and lands at its lowest fully legal position. It cannot be held. Ghost and hard drop use that same landing. Ordinary pieces stop at their first obstruction. Default locking waits one full gravity interval after grounding; grounded moves do not restart the delay. Lifting off clears it. Hard drop follows that policy unless immediate locking is selected.

The three panel toggles sit above the two gameplay buttons. The board remains centered and game information stays visible. On narrow screens, optional regions scroll horizontally; focus a side region and use its native arrow keys to pan. Inputs and other controls keep their normal keyboard behavior.

## Settings and snapshots

Each setting resolves independently: valid explicit URL parameter, saved cookie, default. Explicit default values are saved too; omitted parameters retain saved values. Invalid/repeated sources report diagnostics and fall back. Changes update only the selected cookie/query pair, preserving other raw query text and the fragment.

| URL key | Accepted text | Default |
| --- | --- | --- |
| ghost | hidden, dynamic, visible | visible |
| hardDrop | 0, 1 | 1 |
| nextPreview | 0, 1 | 1 |
| hardDropLock | general, immediate | general |
| lockPolicy | failed, interval | interval |
| hold | 0, 1 | 1 |

Dynamic ghost hides only when every projected cell is above row ten; a straddling landing remains visible. Cookies are named tetris_KEY and persist for one year with Path=/, SameSite=Lax and Secure on HTTPS. Full persistent changes/restores require HTTP(S) and permitted cookies; failures report clearly and attempt rollback.

Only completed games enter the leaderboard. Rank is score descending, UTC completion time ascending, then stable UUID ascending. Unfinished restarts add nothing. Reload clears results while configured settings persist. Save captures the current top ten and all six settings; Restore replaces them after complete validation and does not restore the active board, hold or bonuses. File operations pause a running game and leave it paused for explicit resume.

JSON and SQLite preserve UUIDv4 IDs, safe non-negative integer scores and canonical UTC timestamps. Files are limited to 1 MiB. JSON rejects duplicate properties, invalid numeric tokens, unknown fields and invalid calendar dates. SQLite checks metadata, schema, indexes, storage types and exact integer text. Both use the same complete candidate validator and browser-state transaction. See [format contracts](docs/dev/spec/persistence.md) and [schema](schemas/tetris-save.schema.json).

SQLite fetches only the pinned sql.js 1.14.2 JavaScript loader from jsDelivr with Fetch integrity. Its matching binary and all worker/application code are embedded in the HTML. There is no separate binary asset. The isolated codec has a ten-second deadline, including startup. Network/library failure affects only SQLite; JSON and gameplay remain available. The upstream MIT notice is retained in the HTML.

## Development and evidence

Production is tetris.html; development dependencies are pinned in requirements-dev.txt. Local Linux verification uses:

```sh
PYTHONPATH="$PWD/.dev/python" PLAYWRIGHT_BROWSERS_PATH="$PWD/.dev/browsers" TETRIS_FIREFOX_SANDBOX=off python -m pytest -q
python tools/package.py
python tools/package.py --check
```

The Firefox override is limited to this trusted local execution host after normal content processes failed with /proc/self/uid_map: EPERM. CI uses managed Chromium headless shell and Firefox without that host-specific override. Tests exercise the actual inline domain, HTML/Canvas, downloads, cookies, URLs, file failures, package contents and runtime integrity. Native OS focus delivery and headed browsers are outside the required evidence matrix. Controlled SQL tests serve verified upstream loader bytes and reject external binary requests; live CDN availability remains network-dependent.

Release assets have stable version-free names. Each phase is verified and explicitly integrated before its release; publication verifies source/tag/body identity and actual downloaded bytes, checksums and latest links. See [tasks](docs/dev/TASKS.md), [phase reports](docs/dev/reports/phases), [handoff](docs/dev/HANDOFF.md), [specification](docs/dev/SPEC.md) and [architecture](docs/dev/ARCHITECTURE.md).

Development follows [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md).

Published and verified: [v1.0.0](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/tag/v1.0.0).
