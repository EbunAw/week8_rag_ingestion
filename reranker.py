
from sentence_transformers import CrossEncoder

from hybrid_retrieval import hybrid_search


# A lightweight model trained to rank question-passage relevance.
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(RERANKER_MODEL)


def rerank_results(
    query: str,
    candidate_count: int = 10,
    n_results: int = 5,
) -> list[dict]:
    """
    Retrieve hybrid candidates, score each question-passage pair,
    and return the most relevant passages.
    """

    candidates = hybrid_search(
        query=query,
        n_results=candidate_count,
        candidate_count=candidate_count,
    )

    if not candidates:
        return []

    pairs = [
        (query, candidate["text"])
        for candidate in candidates
    ]

    scores = reranker.predict(pairs)

    for candidate, score in zip(candidates, scores):
        candidate["reranker_score"] = float(score)

    ranked = sorted(
        candidates,
        key=lambda item: item["reranker_score"],
        reverse=True,
    )

    return ranked[:n_results]

if __name__ == "__main__":
    question = "How does RAG use retrieved documents to generate an answer?"

    results = rerank_results(
        query=question,
        candidate_count=10,
        n_results=5
    )

    for rank, result in enumerate(results, start=1):
        print(f"\nRank {rank}")
        print(f"Chunk ID: {result['id']}")
        print(f"Reranker score: {result.get('reranker_score')}")
        print(f"Full text: {result['text']}")
