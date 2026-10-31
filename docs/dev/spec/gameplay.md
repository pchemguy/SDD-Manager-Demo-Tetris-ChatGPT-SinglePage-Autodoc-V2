# Gameplay contracts

Canonical owner for G1–G7; see [SPEC](../SPEC.md) for system acceptance and [configuration](configuration.md) for setting values.

## G1 — Board, geometry and movement

The visible board has ten columns (x=0–9) and twenty rows (y=0–19). Two hidden spawn rows y=-2,-1 admit an active piece but never locked cells. Seven tetrominoes each contain four cells. Store ordinary piece identity after locking; use distinct non-white colors (I cyan, J blue, L orange, O yellow, S green, T purple, Z red). Penetrator cells retain a white appearance when locked, without overwriting existing cells.

Spawn at x=3,y=-1 using these four-column masks; dots are empty. I rotates in a 4×4 square; J/L/S/T/Z rotate in their upper-left 3×3 square; O is invariant.

| Piece | Four rows, separated by `/` |
| --- | --- |
| I | `..../IIII/..../....` |
| J | `J.../JJJ./..../....` |
| L | `..L./LLL./..../....` |
| O | `.OO./.OO./..../....` |
| S | `.SS./SS../..../....` |
| T | `.T../TTT./..../....` |
| Z | `ZZ../.ZZ./..../....` |

Clockwise rotation maps local (x,y) to (n-1-y,x), with inverse for counterclockwise. For a rotated non-O piece try offsets, in order: (0,0), (-1,0), (1,0), (-2,0), (2,0), (0,-1), (0,-2), with positive y downward. Accept the first legal candidate; if none succeeds, retain the original piece. Kicks cannot move cells outside x=0–9, y=-2–19. Ordinary travel rejects overlap with locked cells. A downward command moves at most one row; rejected side/rotation commands are no-ops.

## G2 — Start, lock, clear, score and completion

Start/restart clears board, hold, score, lines, bonus count and timers; settings, panel visibility and session results remain. The first level is 1. A legal lock writes exactly four visible, non-overlapping cells; if locking would leave a cell above y=0, end the game without writing that piece or awarding a clear. Spawn collision ends the game. End a run once; subsequent frames/inputs cannot produce duplicate results.

Remove all complete rows simultaneously, shift rows above downward, and fill the top with empty rows. Award 100/300/500/800 points for 1/2/3/4 cleared lines, multiplied by the level before the clear. Successful soft-drop rows award one point each and hard-drop distance awards two points per row, without repeated awards for a zero-distance drop. Score saturates at Number.MAX_SAFE_INTEGER. Total lines increments by cleared rows; level=1+floor(lines/10). Gravity interval in active milliseconds is max(80,1000×0.85^(level-1)). Keep integer score/line totals. No combo, T-spin or back-to-back bonus is required.

Only game over creates a completed result. Restart discards an unfinished run; idle, pause and file operations create no result. A completed result captures score, one fresh stable ID and current UTC completion time.

## G3 — Time and locking policies

Maintain separate gravity scheduling and grounded lock delay. Ordinary grounded means the next row is blocked. Penetrator grounded means it is at its lowest valid eventual landing under G7. Determine grounded state after spawn, movement, rotation, activation, hard drop and each downward step.

Under `failed`, a gravity or soft-drop attempt that cannot move downward locks a grounded, legally positioned piece. Under `interval`, grounding starts a deadline one full current gravity interval later. A newly grounded piece receives the full interval regardless of the gravity accumulator. Failed downward attempts do not shorten it. Lateral motion/rotation while continuously grounded does not restart it. Lifting off clears it; becoming grounded again starts a full interval. Pause freezes the remainder. Changing the selected general policy, or the hard-drop policy while grounded, discards the old deadline and starts timing afresh under the applicable policy; unrelated setting changes leave timing intact.

When a lock deadline and a gravity event coincide, process the lock first; never apply the expired event to the newly spawned piece. A newly spawned piece starts fresh gravity timing. Active elapsed time is processed by chronological domain events rather than one move per rendered frame. Exact deadline is inclusive: one millisecond before does not lock, at the deadline does. No lock-delay reset cap is needed because grounded motion does not reset timing.

## G4 — Bag, queue and hold

Shuffle one copy of each of the seven types into a bag using the injected random source. Consume complete bags before generating the next; preview reads the next queued type without consuming it. Restart resets the queue. Next-preview off hides only presentation.

With hold on, C stores the current regular piece and spawns from the queue when the slot is empty; otherwise swap with the held type. Incoming pieces use default spawn orientation/location and fresh gravity/lock timing. Only one successful hold is allowed until the active piece locks. A blocked spawn after hold ends the game. Hold off rejects the action without changing queue/slot; retain a stored type for re-enabling. Active penetrators reject hold without spending/returning bonuses or changing the slot.

## G5 — Landing, ghost and hard drop

For ordinary pieces the landing is the last legal position reachable by consecutive downward rows before the first obstruction. Ghost displays the shape at that landing without changing board/state. Omit it when it coincides with the active piece; its color/outline must distinguish it from locked and active cells.

Ghost mode `hidden` always suppresses it. `visible` shows it where meaningful. `dynamic` suppresses it only when every projected occupied cell has y<10; any projected cell at y≥10 permits visibility. Re-evaluate after every relevant board/piece/mode change, including penetrator activation.

Hard drop off rejects Enter. Hard drop on positions the piece at its computed landing and awards distance points. With `immediate`, lock in that command. With `general`, apply G3; the positioning command itself does not constitute a failed downward attempt under `failed`, even at zero distance. Repeated hard drop does not reset an existing grounded interval. A landing at the current row yields zero points.

## G6 — Bonus and activation

A four-row clear earns exactly one bonus, capped at three. Other clears earn none. B with zero bonuses or an already active penetrator is a no-op. A valid activation spends exactly one bonus, marks that active piece a penetrator, recomputes landing/grounded state and updates the symbol indicator. White is reserved for active/locked penetrator pieces and their ghost outline. The ability ends only when that piece locks or the run ends/restarts; it is never transferred into hold. Newly spawned pieces are regular.

## G7 — Penetrator travel and legal termination

Penetrator travel ignores occupied cells but preserves board bounds. For a proposed column/orientation and current y, enumerate all in-board non-overlapping placements at that y or lower, ignoring intervening obstructions; the greatest y is its terminal landing. Ordinary movement limits still apply, but a penetrator move/rotation is admitted only if at least one such eventual landing exists. Activation starts from an ordinary legal piece and must also find a landing before spending the bonus.

Gravity/soft drop advance through occupied intermediate rows toward that terminal landing and stop there. They do not descend past the last valid landing into an un-lockable floor overlap. Hard drop and visible ghost use exactly that target. A penetrator can cross several occupied barriers and reach a lower cavity; none of those board cells is destroyed. Lock uses the ordinary full-position validation, then ordinary row clearing/scoring. The locking policy cannot bypass that validation.
