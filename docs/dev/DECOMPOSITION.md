# Logical component model

This model refines [ARCHITECTURE](ARCHITECTURE.md). Components are cohesive sections of the single HTML application, not separate runtime files. Interfaces below express responsibility and collaboration; SPEC owns exact values, events, errors and acceptance.

## Components and verification seams

| ID / component | Responsibility and owned state | Provided boundary / consumers | Required inputs and verification seam |
| --- | --- | --- | --- |
| C1 Board rules | Piece geometry, collision, rotation/kick tables, legal locked cells and landing calculation | Position/rotation/landing decisions for C3; projected cells for C7 | Board and piece values; pure fixtures exercise walls, floor, stack and penetration |
| C2 Piece source | Seven-bag queue and random sampling; injectable simpler baseline source | Next piece and read-only preview to C3 | Injected random function; deterministic sequence and bag-membership checks |
| C3 Game session | Board, active/held pieces, lifecycle, gravity accumulator, grounded deadline, score/level, bonuses and per-piece hold/penetrator state | Start, advance-time and gameplay commands; immutable display snapshot and one game-completed event | C1/C2 and validated settings; deterministic state/time fixtures verify event order and boundaries |
| C4 Settings model | Six canonical setting definitions, defaults and strict typed validation | Complete settings values and per-setting parse/serialize functions for C5/C9/C10 | Plain values; table-driven round trips and invalid-value checks |
| C5 Snapshot model | Shared schema definition, full result/settings validation and deterministic top-ten ordering | Validated candidate snapshot for C8/C9/C10; embedded JSON Schema | Plain decoded data; invalid timestamp, ID, score, key, type, version and duplicate fixtures |
| C6 Leaderboard | Session's top-ten completed results and stable IDs/timestamps | Record one completion, replace validated results, read-only result snapshot to C7/C8 | C5 ordering/validation, injected ID and UTC providers; game-over/restart and tie fixtures |
| C7 Presentation and input | Canvas painting, HTML panels/settings/help/errors, panel visibility, keyboard/focus handling | Read-only rendering and semantic commands to C8 | Display models, DOM and Canvas; screenshot/geometry/input checks in isolated browsers |
| C8 Controller | Live state references, command serialization, animation loop and restore operation ownership | Connect inputs, domain results, configuration and file operations; single restore commit boundary | C3–C7/C9–C11; integration checks observe commands and browser side effects |
| C9 Configuration adapter | Independent URL/cookie resolution, cookie/URL write/readback and rollback of owned browser values | Initial complete settings; transactional setting application for C8 | C4 validation plus browser cookie/history adapters; isolated origins exercise precedence, rejection and failure |
| C10 Snapshot codecs | JSON decoding/encoding and isolated SQLite encoding/decoding into C5 candidates | Asynchronous candidate/export bytes to C11; typed decode/validation failure to C8 | C5, pinned SQL library inside worker; cross-format round trips, malformed/schema/resource failures |
| C11 File and worker adapter | File selection/size checks, worker lifecycle/deadline, download URL ownership and busy-operation state | One selected file, one completed download, or explicit failure/cancellation | Browser File/Blob/Worker/URL APIs; download parsing, cancellation/timeout and teardown checks |

## Domain collaboration

C8 passes validated settings and semantic commands to C3. C3 calls C1 for all movement/rotation and landing decisions and C2 for new pieces. Ghost and hard drop consume the same C1 landing result; C7 never calculates a competing landing. C3 changes locked cells only through a valid lock operation, then emits line-clear/score/bonus outcomes and spawns a successor. C8 consumes a completion event once, calling C6 with a newly generated stable ID and UTC completion time.

C3 receives active elapsed time, not a browser clock. It tracks gravity and lock deadlines separately, orders due events deterministically, and exposes a paused snapshot without advancing either timer. C8 owns browser frame scheduling and visibility events. C7 can render held/next shapes, bonus symbols and ghost visibility directly from the snapshot.

Penetrator travel may overlap occupied cells. C1 supplies the lowest valid eventual landing for the proposed column/orientation; C3 admits only moves that preserve an eventual valid landing and grounds the piece at that target. Thus an overlapping intermediate state cannot force an illegal lock at the floor. C3 owns activation spending, per-piece lifetime and hold exclusion; the board representation needs no separate penetrator cell type after lock.

## Configuration and file collaboration

C4 owns settings identity/type knowledge. C9 resolves each field independently and returns a complete settings object plus diagnostics. C8 applies it to C3 and C7. C9 preserves unrelated URL parameters and cookies and never changes leaderboard history.

C10 decodes into temporary data; C5 validates all fields and produces a canonical candidate. C8 commits that candidate only after complete validation and browser-effect preparation. C6 replaces results and C9 applies settings within this controller-owned transaction. Neither codec can reach live game/session objects or write cookies/history.

C11 creates an owned worker for each SQLite operation, passes bounded bytes/data and accepts a single matched response. The worker's embedded bootstrap loads only the pinned SQL library, releases statements/database resources and posts plain results. C11 terminates on timeout/error/completion, revokes Blob URLs, and prevents a stale response or double click from committing twice. Cancellation changes no live data. JSON operations use the same candidate/validation boundary without needing the SQL library.

## Failure and lifecycle boundaries

- C1–C6 reject invalid inputs before mutation; domain rejection of an ordinary gameplay command is a no-op rather than an application error.
- C8 alone decides whether a result changes live state and reports user-facing failures through C7.
- C9 distinguishes invalid source values from browser read/write failure and retains prior relevant values for rollback.
- C10/C11 bound untrusted file work; malformed data, unsupported versions, missing CDN access or worker timeouts never create partial restores.
- C7 uses text rendering for file/result/error values, keeping untrusted content out of HTML interpretation.
- Dependencies are directed from adapters/presentation/controller into domain/model services. No component retrieves controller globals to bypass its interface.

Tests may extract the pure inline core in a development harness and inject time/randomness/IDs. Browser tests still run the actual HTML and its browser adapters. The verification seam must not create a second implementation or a required external runtime asset. No focused children are necessary for this component model.
