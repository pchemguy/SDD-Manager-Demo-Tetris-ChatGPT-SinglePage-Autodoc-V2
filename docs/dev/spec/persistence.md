# Results and file persistence contracts

Canonical owner for F1–F5. [Configuration](configuration.md) owns settings types and textual encodings.

## F1 — Completed results and ranking

A result has exactly `id`, `score`, `timestamp`: id is a canonical lowercase UUID v4 string; score is an integer from zero through 9007199254740991; timestamp is a real Gregorian UTC instant in canonical `YYYY-MM-DDTHH:mm:ss.sssZ` form, years 0001–9999. Reject impossible dates, offsets, missing milliseconds, leap seconds and strings that fail an exact parse/format round trip. IDs are unique within a snapshot and remain unchanged through sorting, truncation, export and restore. New results use browser cryptographic randomness for UUID creation and the completion wall clock; no result is regenerated on save.

Rank by score descending, timestamp ascending, then ID lexicographically ascending. Keep at most ten. Zero-score completions are allowed. The initial page session is empty; reload clears results. A valid restore wholly replaces the current session results (including an empty array) and does not merge them. Do not store leaderboard history in cookies or local storage. Generated scores/timestamps must pass the same model validator as restored ones.

## F2 — JSON representation and schema

UTF-8 JSON has exactly three root properties: `formatVersion` equal to integer 1, `results` an array of zero through ten F1 records, and `settings` an object with exactly the six CFG1 keys and typed values. Every record disallows additional properties. Reject a BOM/encoding error, duplicate property names at any object level, missing/extra fields, invalid types/values/version and duplicate result IDs. Do not coerce numeric strings or booleans. Sorting an otherwise valid results array is allowed; exceeding ten results is invalid rather than silently truncated on restore.

Supply a Draft 2020-12 JSON Schema with the release, matching the embedded schema's parsed content. Encode required fields, limits, enums/types and additionalProperties=false. Enforce real-calendar timestamps, duplicate JSON keys and ID uniqueness with explicit semantic validation in addition to schema structural validation. A schema `format` annotation alone does not satisfy timestamp validation. Validate the complete candidate before application.

## F3 — SQLite representation

Export a real SQLite 3 database with PRAGMA user_version=1 and application_id=0x54545253. Its only user schema objects are these tables; implicit SQLite primary-key indexes are allowed, triggers/views/virtual tables/extra user indexes/tables are rejected. Inspect schema/columns and SQLite integrity before reading candidate rows. Do not execute SQL text from the input or query through views.

```sql
CREATE TABLE high_scores (
    id TEXT PRIMARY KEY NOT NULL,
    score INTEGER NOT NULL CHECK(score >= 0 AND score <= 9007199254740991),
    timestamp TEXT NOT NULL
);
CREATE TABLE settings (
    key TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
);
```

Require exactly the named ordered columns, declared types, non-null attributes and primary-key positions. Inspect row storage types as well as declared types. Accept only zero through ten valid high_scores rows and exactly six distinct settings rows, one per CFG1 key. Setting values use CFG1 textual encodings. Convert integral scores without lossy numeric rounding: inspect their integer storage type and exact decimal text before converting within the safe range. Validate all F1/CFG1 semantic constraints after decoding. Metadata mismatches, corruption, unsupported schema, extra/duplicate/missing settings and invalid rows reject the database. Schema checks need not require identical SQL whitespace or CHECK-expression spelling when column/row validation enforces the same contract.

## F4 — Save/Restore operations

Save captures one valid snapshot at the click, chooses JSON or SQLite from the export selector, and downloads exactly one `tetris-save.json` or `tetris-save.sqlite` file. Saving has no settings, cookie, URL or result side effects. Restore chooses one file, detects SQLite by its `SQLite format 3` header and otherwise attempts strict UTF-8 JSON; filename extensions/MIME are advisory. Restore of either type validates completely into temporary state, canonicalizes ranking, then replaces results and applies all six settings through one controller commit with CFG3 browser updates. Do not restore the active board, hold, bonuses or timers from the file.

Reject files larger than 1048576 bytes before reading/decoding. Bound each SQLite operation, including library startup, to ten seconds; timeout terminates the worker. Do not allow more than one Save/Restore operation concurrently. Disable file buttons, export selector and setting controls while busy; take a stable paused-game snapshot and reject stale operation responses. Cancellation, decode/validation errors, unavailable library, download setup failures and worker failures show understandable status and do not apply a candidate. Error messages identify a useful category/field without injecting file-provided HTML. Reset busy state and release all worker/database/statement/Blob URL resources on every terminal path. The game remains paused until explicit resume.

## F5 — Validation and atomicity acceptance

Exercise successful JSON and SQLite round trips in both directions, including empty/top-ten results, tied scores, all settings and explicit default values. Verify the SQLite bytes independently with Python sqlite3 and JSON against the supplied schema plus semantic cases. Invalid-file cases include truncated/invalid encoding, unknown versions, extra/missing keys, duplicate keys/IDs/settings, false integer types, negative/out-of-range/fractional scores, impossible/non-UTC timestamps, bad settings, malformed SQLite/header/schema/metadata, triggers/views/extra tables, and size/time limits.

For each rejected restore compare the previous leaderboard, six settings, relevant cookies and entire URL; none may change from validation. Recoverable commit-side browser-write failures roll back the same state. Verify a valid restore updates all six browser representations, replaces session results, retains stable IDs/timestamps and survives a settings reload while leaderboard history remains session-only. A successful file parse alone is not a successful restore.
