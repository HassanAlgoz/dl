from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class HybridSearchResult:
    dense_ranking: list[str]
    lexical_ranking: list[str]
    hybrid_ranking: list[str]


def lexical_rank(query: str, doc_ids: Sequence[str], docs: Sequence[str]) -> list[str]:
    """Rank documents by how many query tokens appear in each document."""
    query_tokens = set(query.lower().split())
    scored = []
    for doc_id, doc in zip(doc_ids, docs):
        overlap = len(query_tokens & set(doc.lower().split()))
        scored.append((doc_id, overlap))
    scored.sort(key=lambda item: (-item[1], item[0]))
    return [doc_id for doc_id, _ in scored]


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]],
    weights: Sequence[float] | None = None,
    k: int = 60,
) -> list[str]:
    """Merge ranked lists with reciprocal rank fusion (more negative score = better)."""
    if weights is None:
        weights = [1.0] * len(rankings)
    scores: dict[str, float] = {}
    for ranking, weight in zip(rankings, weights):
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) - weight / (k + rank)
    return sorted(scores, key=scores.get)


def hybrid_search(
    collection,
    query: str,
    doc_ids: Sequence[str],
    documents: Sequence[str],
    *,
    weights: tuple[float, float] = (0.7, 0.3),
    k: int = 60,
) -> HybridSearchResult:
    """Run dense Chroma search + lexical token overlap, then fuse with RRF."""
    dense = collection.query(
        query_texts=[query],
        n_results=len(documents),
        include=["documents"],
    )
    dense_ranking = dense["ids"][0]
    lexical_ranking = lexical_rank(query, doc_ids, documents)
    hybrid_ranking = reciprocal_rank_fusion(
        rankings=[dense_ranking, lexical_ranking],
        weights=list(weights),
        k=k,
    )
    return HybridSearchResult(
        dense_ranking=dense_ranking,
        lexical_ranking=lexical_ranking,
        hybrid_ranking=hybrid_ranking,
    )
