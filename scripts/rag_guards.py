"""Deterministic safety guards for grounded GraphRAG answers."""


def grounded_or_abstain(answer, context):
    """Return an answer only when retrieval supplied explicit usable context."""
    if not str(context or "").strip():
        return "Insufficient evidence in the retrieved context to answer faithfully."
    return str(answer or "").strip()


def valid_relation(relation, evidence):
    """Require explicit evidence before accepting an extracted relation."""
    return bool(str(relation or "").strip() and len(str(evidence or "").split()) >= 3)
