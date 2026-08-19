import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from scripts.rag_guards import grounded_or_abstain, valid_relation


def test_empty_retrieval_abstains_instead_of_using_world_knowledge():
    assert grounded_or_abstain("Microsoft invested in OpenAI", "") == (
        "Insufficient evidence in the retrieved context to answer faithfully."
    )


def test_relation_without_evidence_is_rejected():
    assert valid_relation("ACQUIRED", "") is False
    assert valid_relation("ACQUIRED", "Microsoft acquired Activision") is True


if __name__ == "__main__":
    test_empty_retrieval_abstains_instead_of_using_world_knowledge()
    test_relation_without_evidence_is_rejected()
    print("rag guards: PASS")
