def recall_at_k(relevant: set, retrieved: list, k: int) -> float:
    """
    Recall@K = |relevant ∩ retrieved@K| / |relevant|
    """
    if not relevant:
        return 0.0

    retrieved_k = set(retrieved[:k])
    return len(relevant.intersection(retrieved_k)) / len(relevant)
