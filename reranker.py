from sentence_transformers import CrossEncoder

from hybrid_retrieval import hybrid_search


# CrossEncoder model used to score query-passage relevance.
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(RERANKER_MODEL)


def rerank_results(
    query: str,
    candidate_count: int = 10,
    n_results: int = 5,
):
    """
    Retrieve candidate chunks with hybrid search, then rerank them
    using CrossEncoder relevance scores.
    """
    candidates = hybrid_search(
        query=query,
        n_results=candidate_count,
    )

    if not candidates:
        return []

    pairs = [(query, item["text"]) for item in candidates]
    scores = reranker.predict(pairs)

    ranked_results = []

    for item, score in zip(candidates, scores):
        result = item.copy()
        result["reranker_score"] = float(score)
        ranked_results.append(result)

    ranked_results.sort(
        key=lambda item: item["reranker_score"],
        reverse=True,
    )

    return ranked_results[:n_results]