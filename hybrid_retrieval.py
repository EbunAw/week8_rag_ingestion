
from embeddings import generate_embedding
from vector_store import search_chunks
from keyword_search import keyword_search


def hybrid_search(
    query: str,
    n_results: int = 5,
    candidate_count: int = 10,
    collection_name: str = "rag_overlapping",
) -> list[dict]:
    """
    Combine vector and keyword retrieval using
    Reciprocal Rank Fusion (RRF).
    """

    # 1. Vector retrieval
    query_embedding = generate_embedding(query)

    vector_results = search_chunks(
        query_embedding=query_embedding,
        n_results=candidate_count,
        collection_name=collection_name,
    )

    # 2. Keyword retrieval
    keyword_results = keyword_search(
        query=query,
        n_results=candidate_count,
    )

    # Store each unique chunk and its fusion score.
    fused = {}

    def add_result(
        chunk_id: str,
        text: str,
        metadata: dict,
        rank: int,
        retrieval_type: str,
    ):
        if chunk_id not in fused:
            fused[chunk_id] = {
                "id": chunk_id,
                "text": text,
                "metadata": metadata,
                "rrf_score": 0.0,
                "retrieved_by": [],
            }

        fused[chunk_id]["rrf_score"] += 1 / (60 + rank)
        fused[chunk_id]["retrieved_by"].append(retrieval_type)

    # Chroma returns results grouped by query.
    for rank, chunk_id in enumerate(
        vector_results["ids"][0], start=1
    ):
        index = rank - 1

        add_result(
            chunk_id=chunk_id,
            text=vector_results["documents"][0][index],
            metadata=vector_results["metadatas"][0][index],
            rank=rank,
            retrieval_type="vector",
        )

    for rank, result in enumerate(
        keyword_results, start=1
    ):
        add_result(
            chunk_id=result["id"],
            text=result["text"],
            metadata=result["metadata"],
            rank=rank,
            retrieval_type="keyword",
        )

    # 3. Rank by the combined RRF score.
    ranked = sorted(
        fused.values(),
        key=lambda item: item["rrf_score"],
        reverse=True,
    )

    return ranked[:n_results]


if __name__ == "__main__":
    question = "How does RAG use retrieved documents to generate an answer?"

    results = hybrid_search(
        query=question,
        n_results=5,
        candidate_count=10,
    )

    for rank, result in enumerate(results, start=1):
        print(f"\n{'=' * 80}")
        print(f"Rank: {rank}")
        print(f"Chunk ID: {result['id']}")
        print(f"Retrieved by: {result.get('retrieved_by')}")
        print("Full chunk text:")
        print(result["text"])
        print("=" * 80)
