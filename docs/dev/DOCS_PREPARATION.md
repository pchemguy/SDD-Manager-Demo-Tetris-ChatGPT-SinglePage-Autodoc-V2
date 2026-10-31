# Main documentation preparation record

Current control and evidence for the full project. [DOCS_TASKS](DOCS_TASKS.md) owns preparation tasks; [HANDOFF](HANDOFF.md) provides checkpoint context.

## Current control

- Mode: autodoc/onepass, selected by the user's project-development request.
- Scope: the complete single-page HTML Tetris target; one documentation pass with bounded implementation phases to be planned later.
- Approval basis: the user's `K` accepted the proposed implementation approach and gameplay decisions below. The user's subsequent `k` approved the published PROJECT proposal at `c52e30a33cac17d1015053a2820f853eeb750e79` on 2026-10-31; subsequent document checkpoints through TASKS are preapproved by autodoc mode.
- Tracking: enabled for documentation and implementation by root AGENTS.md. GitHub milestone 1 (`sdd-docs-main`) and DOCS-001 through DOCS-009 issues #1 through #9 were created and read back with exact bundled content and associations before target writes.
- Publication: every owned commit must be pushed and read back before advancement.
- Next boundary: prepare through DOCS-008; PROJECT approval publication and issue #2 closure/readback are verified and stop before DOCS-009 package QC or implementation.
- Reporting: Standard, with concise progress updates.

## Scope source

The user's complete target comprises the classic playable baseline, modern rules, conditional ghost, penetrator, all six session-only settings followed by cookie/URL persistence, session top-ten leaderboard, JSON/SQLite manual Save/Restore, and the prescribed centered five-panel layout. The accepted PROJECT owns principal product scope; SPEC will own exact contracts. No later documentation passes are selected.

## Accepted clarification decisions

All decisions in this section were proposed in chat and accepted by the user's `K` on 2026-10-31. Exact contracts will be expressed in SPEC; this record preserves their decision basis.

| Concern | Accepted direction |
| --- | --- |
| Application approach | One HTML file with embedded JavaScript/CSS, Canvas board and standard HTML panels. |
| Ghost at the midline | Hide only when every projected cell is above the midline; show when any cell reaches the lower half. |
| Grounded delay | Start when grounded; movement/rotation while still grounded does not reset it. Lifting off clears it; pause freezes remaining time. |
| Penetrator and hold | Activation immediately spends one available bonus; repeat activation does nothing. Hold is disabled for the active penetrator. |
| Penetrator landing | Pass through occupied cells, never lock at an invalid position; ghost and hard drop share the lowest valid landing. |
| Invalid configuration | Report invalid URL values and fall back independently to valid cookie/default values. Reject an invalid restore atomically. |
| Completed games | Game over records a result; restarting an unfinished game discards that run. |
| Live settings | Apply immediately; changing locking policy while grounded starts timing afresh. |
| Cookie verification | Verify cookies and URL persistence over HTTP(S); direct file opening may limit cookies. |

No material product decision is currently unresolved for brief review. Detailed defaults, keys, scoring and file-contract precision remain with the design/specification owners, within the accepted scope.

## Structural design decisions

The design owner selected a pure inline game domain, controller-owned live state, a shared candidate-snapshot validator and an isolated SQLite codec worker. SQLite uses the pinned sql.js 1.13.0 asm.js build from jsDelivr, whose upstream versioned README confirms single-JavaScript distribution. This preserves the one-HTML application constraint and isolates optional CDN failures. Actual CDN bytes/browser integration remain implementation verification, not observed product capability. The decomposition enforces the accepted valid-lock guarantee by sharing the lowest valid landing across penetrator gravity, ghost and hard drop; proposed moves without any valid eventual landing are rejected. This is a design-owner enforcement detail within the accepted penetrator contract.

## Decisions and document evidence

| Task | Evidence / decision basis |
| --- | --- |
| DOCS-001 | All four existing root files retained unchanged against initial commit `89d088c799d0556603bc0c49b3ac0934d9bacbcc`; no copies needed. Task list instantiated from the bundled template with only DOCS-001 checked. This control record and HANDOFF complete initialization metadata. Initialization commit `bca8bec2c7eca063a4daa21a6d5d15de859ead04` was pushed with exact ref readback and confirmed process cleanup. Issue #1 was closed as completed and read back before PROJECT authoring. |
| DOCS-002 | PROJECT proposed at SHA-256 `dfe653c839d9bfde015f9f2b4fce30a01ce386db391fa3141c79c9b68369fe04`. Reviewed against the complete user request and accepted clarification decisions; complete principal scope retained without detailed architecture/specification. README adds truthful preparation status and disclosure links. Human first approval supplied by the subsequent `k`; exact presented bytes retained unchanged. DOCS-002 closes with this approval evidence and its owning checkbox. |
| DOCS-003 | ARCHITECTURE SHA-256 `3a1d73f814f63075beb344e1971699277e72a4479256da74c7a8fe61f0f2cd2e`; accepted under autodoc scoped preapproval after PROJECT approval. Owner reviewed all brief responsibilities, state ownership, dependency direction, shared landing/validation and browser error boundaries. No material design blocker remains; DECOMPOSITION is next. |
| DOCS-004 | DECOMPOSITION SHA-256 `c23cfeac552a33b96349e9d64105becab0c6e1c788830671e92b449abc6962d5`; accepted under autodoc preapproval. Reviewed C1-C11 for single state owners, directed dependencies, reproducible time/randomness seams, legal penetrator locks and controller-only restore commits; consistent with ARCHITECTURE. |
| DOCS-005 | SPEC and its QC not yet authored. |
| DOCS-006 | PLAN and strategy QC not yet authored. |
| DOCS-007 | layout and combined PLAN/layout QC not yet authored. |
| DOCS-008 | TASKS and task-list QC not yet authored. |
| DOCS-009 | Package QC not selected; remains beyond the autodoc stop. |

## Initialization

- Root files originally present and retained: `AI_DISCLOSURE.md`, `SDD-MANAGER.md`, `AGENTS.md`, `SKILL_DISCOVERY_PROTOCOL.md`.
- Copies: none. Byte-for-byte preservation verified against the initial committed blobs.
- Continuation: all four files were present, so no mixed-presence pause applies.
- Manual provenance: default enabled. Two bundled assets copied unchanged to `docs/ai-logs/` on `design-docs/ai-logs`, seeded at `49ae43a07081049d31e01982002c3dced12a7052` from default base `89d088c799d0556603bc0c49b3ac0934d9bacbcc`. Explicit two-parent merge `e75c858e73168c77104e15ee97ce6b5dc3cf583c` into `main` was verified and published before `design-docs/main` was created. No conversation transcript was created.
- Preparation branch: `design-docs/main`, created from `main` at `e75c858e73168c77104e15ee97ce6b5dc3cf583c`; integration target `main`.
- Credentials: accepted repository token stored only in ignored, untracked `gh.tkn`; the owned `*.tkn` exclusion was included with the preliminary scaffold checkpoint.
- Reset: none; onepass.

## Pending transitions

DOCS-001 (#1) was closed as completed and read back after publication. DOCS-002 (#2) is closed as completed and read back. DOCS-003 (#3) is closed as completed and read back. DOCS-004 (#4) closure is pending this decomposition publication; later issues and milestone 1 remain open; reconcile later effects before replay.
