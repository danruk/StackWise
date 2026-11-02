"""Similarity-based retrieval utilities."""

from typing import List, Tuple


def rank_matches(query: str, candidates: List[str]) -> List[Tuple[str, float]]:
    """Placeholder ranking function for future TF-IDF/embedding integration."""
    if not candidates:
        return []

    query_lower = (query or "").lower()
    ranked = []
    for candidate in candidates:
        score = 0.0
        if query_lower and query_lower in candidate.lower():
            score += 1.0
        score += min(len(candidate), 0.01 * len(candidate))
        ranked.append((candidate, round(score, 4)))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked
