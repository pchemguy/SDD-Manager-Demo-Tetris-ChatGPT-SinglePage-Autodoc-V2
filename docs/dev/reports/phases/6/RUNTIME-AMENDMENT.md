# SQLite runtime compatibility amendment

Scope: T036, no product/file-contract change. Initial T035 asm initialization evidence remains historical. Minimal SQL execution independently reproduced native Chromium stack overflow in both asm1.13.0 and asm1.14.2; Firefox succeeded. Browser flags and unverified fallbacks were not selected.

Use official production sql.js1.14.2 loader from jsDelivr with its matching binary embedded in the HTML and passed as wasmBinary to the disposable worker. No separate binary request or release asset is required. Upstream: https://github.com/sql-js/sql.js/blob/v1.14.2/README.md .

| Component | Bytes | SHA-256 |
| --- | --- | --- |
| sql-wasm.js | 46535 | f1c84000dbc856c9d87f4f3aabc4d3654bd436165db4be3da13751db3a9c20d7 |
| Embedded sql-wasm.wasm | 658410 | 38c14f6e379210bc942bdc4ebca44e7bfdb4318ecc1c72ca666a28fdce96670a |

Both were downloaded from the exact versioned jsDelivr package and their bytes verified before integration. Browser Fetch SRI verifies the loader; the embedded bytes are part of source/package checksums. Tests route the verified upstream JavaScript through controlled browser transport and reject external .wasm requests. Native startup/decode deadline remains ten seconds, including loading. Six SQLite checks passed in7.18s, including both browsers and independent sqlite3 inspection of real exports.

QC: active architecture and risk strategy now match implementation; TASKS gains a T036 compatibility note with no completion-checkbox change. SPEC product contracts, dependencies, phase/milestone hierarchy, result/settings schemas and filenames are unchanged. Full implementation/QC/autodoc authorization covers this bounded technical repair.
