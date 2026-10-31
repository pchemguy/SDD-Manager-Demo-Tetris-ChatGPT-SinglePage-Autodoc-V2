# Configuration contracts

Canonical owner for CFG1–CFG4. [Gameplay](gameplay.md) defines the behavior selected by these values; [persistence](persistence.md) exports the same typed object.

## CFG1 — Canonical settings

Use exactly these six keys. JSON uses the types shown; URL/cookies/SQLite use the textual encoding column. No aliases, case folding, numeric coercion or whitespace trimming are accepted for source values.

| Key | Type / allowed values | Default | Text encoding |
| --- | --- | --- | --- |
| `ghost` | string: `hidden`, `dynamic`, `visible` | `visible` | Same literal |
| `hardDrop` | boolean | `true` | `1` or `0` |
| `nextPreview` | boolean | `true` | `1` or `0` |
| `hardDropLock` | string: `general`, `immediate` | `general` | Same literal |
| `lockPolicy` | string: `failed`, `interval` | `interval` | Same literal |
| `hold` | boolean | `true` | `1` or `0` |

Unknown query parameters/cookies are unrelated and preserved; unknown settings keys in a restore are invalid. The session-only increment uses defaults, applies settings in memory, and neither reads nor writes configuration URL parameters/cookies. Reload resets its six values. The persistent increment obeys CFG2–CFG4.

## CFG2 — Independent resolution

For each key resolve one valid explicit URL value, else one valid saved cookie, else the default. Parameter names equal the canonical keys. Cookies are named `tetris_<key>`. Decode through standard URL/cookie decoding and then apply strict value validation. Repeated occurrences of a known URL key, malformed decoding, invalid values or ambiguous duplicate cookies invalidate that source for that key, producing a visible diagnostic and allowing the next source. They do not invalidate another setting. Empty parameter values are invalid, not omitted.

Write every valid explicit URL value to its cookie at initialization, including default-valued values. An omitted parameter does not overwrite a valid cookie with the default. Invalid URL values do not overwrite cookies; preserve their URL text until that setting is explicitly changed or a complete valid snapshot is restored. Initial resolution does not populate missing parameters or manufacture saved defaults.

## CFG3 — Changes, encoding and browser effects

A successful user setting change validates the typed value, applies it, writes its cookie and sets exactly one corresponding URL parameter using history.replaceState without navigation. Preserve URL path, fragment, unrelated query pairs and cookies. A full restore does the same for all six, replacing repeated known parameters with one canonical value each. Cookies use Path=/, SameSite=Lax and Max-Age=31536000; add Secure on HTTPS. Read back owned cookie values to detect silent write failure.

Prepare the entire settings object before live application. Retain prior relevant cookie presence/values, complete URL and live settings until commit succeeds. For a write/history failure, restore those owned values and live settings, display a specific error and leave leaderboard replacement uncommitted. A validation failure performs no browser writes. Cookie-blocking environments are reported as unable to provide persistent configuration; the existing session/game remains usable. Browser-controlled failures that also prevent rollback must be reported explicitly rather than reported as a successful restore. Required atomic restore acceptance is exercised in supported HTTP(S) browser contexts and injected recoverable write failures.

## CFG4 — Live interactions

Apply accepted changes immediately. Preview/ghost switches affect presentation without consuming the queue or changing the board. Hard-drop/hold enablement changes affect subsequent commands. Preserve held-piece and hold-used state when hold is off. Apply timing changes as G3 defines; restore compares old/new policy values and changes timing only when those policy values differ. Restore never resets the run or inserts a completed result. Show current effective values in the controls after initialization, change and restore.

Acceptance includes mixed-source precedence, explicit defaults, omissions, empty/repeated/invalid values, invalid cookies, unrelated URL preservation, live toggles, reloads, blocked/recoverable browser writes and all six settings together.
