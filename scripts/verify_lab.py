"""Offline contract verification for Lab 19 deliverables."""
from pathlib import Path
import csv
import json
import re
import sys

ROOT = Path(__file__).parents[1]


def main():
    notebook = ROOT / "Day19_GraphRAG_vs_FlatRAG_Production_Lab_Guide.ipynb"
    nb = json.loads(notebook.read_text())
    assert nb["nbformat"] >= 4
    assert any(c["cell_type"] == "code" for c in nb["cells"])

    golden = list(csv.DictReader((ROOT / "data/golden_dataset.csv").open()))
    assert len(golden) >= 5 and {r["group"] for r in golden} >= {"factoid", "multi-hop", "cross-doc"}
    assert all(r["reference_answer"].strip() for r in golden)

    eval_rows = list(csv.DictReader((ROOT / "outputs/graphrag_eval_results.csv").open()))
    summary_rows = list(csv.DictReader((ROOT / "outputs/graphrag_vs_flatrag_summary.csv").open()))
    assert len(eval_rows) == len(golden)
    summary_headers = set(summary_rows[0]) if summary_rows else set()
    if {"architecture", "quality_mean"}.issubset(summary_headers):
        assert {r["architecture"] for r in summary_rows} == {"Flat RAG", "GraphRAG"}
    else:
        assert {"Loại câu hỏi", "Metric", "Flat RAG", "GraphRAG"}.issubset(summary_headers)
        assert {r["Loại câu hỏi"] for r in summary_rows} >= {"factoid", "multi-hop", "cross-doc"}

    source = notebook.read_text()
    assert "UNWIND $rows AS row" in source
    assert "SUPER_NODE_EDGE_CAP = 50" in source
    assert "GLOBAL_EDGE_CAP = 250" in source
    assert not re.search(r"(?:sk-[A-Za-z0-9]{20,}|gsk_[A-Za-z0-9]{20,})", source)
    print(f"verified notebook={len(nb['cells'])} cells golden={len(golden)} eval={len(eval_rows)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise
