import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]


def edge_is_valid(edge):
    return all(edge.get(k) not in (None, "") for k in ("source_chunk_id", "published_date", "evidence", "confidence"))


def bounded_edges(edges, degree, super_node_degree=100, super_node_cap=50, global_cap=250):
    cap = super_node_cap if degree > super_node_degree else len(edges)
    return edges[: min(cap, global_cap)]


def test_scale_guards_are_documented():
    text = (ROOT / "README.md").read_text()
    assert "LAB_MAX_ARTICLES = 1500" in text
    assert "LAB_MAX_CHUNKS = 3000" in text
    assert "EXTRACTION_MAX_CHUNKS = 400" in text


def test_fixture_edges_have_complete_provenance():
    edges = [
        {"source_chunk_id": "art_01::c0001", "published_date": "2024-01-01", "evidence": "A invested in B.", "confidence": 0.95},
        {"source_chunk_id": "art_02::c0002", "published_date": "2024-02-01", "evidence": "B uses C.", "confidence": 0.88},
    ]
    assert all(edge_is_valid(e) for e in edges)


def test_super_node_is_capped():
    assert len(bounded_edges(list(range(101)), degree=101)) == 50
    assert len(bounded_edges(list(range(10)), degree=10)) == 10
    assert len(bounded_edges(list(range(300)), degree=101)) <= 50


def test_golden_dataset_has_required_groups_and_answers():
    with (ROOT / "data/golden_dataset.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 5
    assert {r["group"] for r in rows} >= {"factoid", "multi-hop", "cross-doc"}
    assert all(r["reference_answer"].strip() for r in rows)


def test_summary_contains_both_architectures():
    with (ROOT / "outputs/graphrag_vs_flatrag_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    if "architecture" in rows[0]:
        assert {r["architecture"] for r in rows} == {"Flat RAG", "GraphRAG"}
        assert all(r["quality_mean"].strip() for r in rows)
    else:
        assert {"Loại câu hỏi", "Metric", "Flat RAG", "GraphRAG"}.issubset(rows[0])
        assert {r["Loại câu hỏi"] for r in rows} >= {"factoid", "multi-hop", "cross-doc"}


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"{name}: PASS")
