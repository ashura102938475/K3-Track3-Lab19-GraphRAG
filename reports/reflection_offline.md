# Reflection and Action Plan

## Lecture mapping

| Concept | Notebook area | Evidence |
|---|---|---|
| Conservative coreference | Module 1 | Same-chunk antecedent rule and unresolved log |
| Schema guard | Module 2 | Node/relation allowlists |
| Bulk ingestion | Module 2 | `UNWIND $rows AS row` |
| Entity resolution | Module 3 | ANN candidate, lexical guard, audit |
| Super-node mitigation | Module 4 | degree threshold, 50-edge cap, 250 global cap |
| LLM judge | Module 5 | three 1–5 quality dimensions |

## Debugging lesson

The most important operational lesson is to separate deterministic contracts from external services. Offline fixtures can validate shape, caps, provenance fields, exports, and rubric coverage; only a configured run can validate model quality, Neo4j connectivity, and real latency.

## Action plan

For a production project, start with Flat RAG for direct support questions, then add a graph only where multi-hop joins and entity identity are demonstrated by evaluation. Use typed entities, provenance-backed relations, ANN candidate blocking, guard rejections, bounded traversal, and route-level observability. Re-run the golden set after every extraction prompt or threshold change.

## Self-assessment

| Criterion | Score (1–5) |
|---|---:|
| GraphRAG understanding | 4 |
| AI coding-agent control | 4 |
| Knowledge-graph quality discipline | 4 |
| Debugging and evaluation | 4 |
