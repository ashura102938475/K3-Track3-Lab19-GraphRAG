# Failure Analysis

## Case 1 — Flat RAG misses a multi-hop answer

`G03` requires joining the Microsoft→OpenAI investment fact with Microsoft→Azure context. Flat RAG may retrieve either chunk but not the complete relation chain. GraphRAG resolves Microsoft as a canonical seed and traverses both provenance-backed edges. Root cause: independent vector ranking has no explicit connectivity constraint.

## Case 2 — GraphRAG can be incomplete

`G05` is vulnerable when the relevant older edge is removed by the super-node policy. Root cause: recency-based pruning optimizes context size but is not neutral for historical questions. Mitigation: detect temporal language, widen the date filter, or use a dedicated historical retrieval route; retain the 250-edge global cap and log the route taken.

## Verification evidence

The completed live run produced 263 nodes and 150 edges in Neo4j, with `invalid_provenance_edges = 0`. The offline verifier additionally checks the notebook's `UNWIND` pattern, 50-edge super-node cap, 250-edge global cap, golden groups, and comparison export.
