
import hybrid_retrieval


def test_hybrid_search_merges_vector_and_keyword_results(monkeypatch):
    query = "What are the two variants of RAG, and how do they differ?"

    vector_results = [
        {
            "id": "chunk-a",
            "text": "Vector result A",
            "metadata": {"source": "sample.txt", "chunk_index": 0},
        },
        {
            "id": "chunk-b",
            "text": "Vector result B",
            "metadata": {"source": "sample.txt", "chunk_index": 1},
        },
    ]

    keyword_results = [
        {
            "id": "chunk-a",
            "text": "Keyword result A",
            "metadata": {"source": "sample.txt", "chunk_index": 0},
        },
        {
            "id": "chunk-c",
            "text": "Keyword result C",
            "metadata": {"source": "sample.txt", "chunk_index": 2},
        },
    ]

    monkeypatch.setattr(
        hybrid_retrieval,
        "generate_embedding",
        lambda query: [0.1, 0.2, 0.3],
    )
    monkeypatch.setattr(
        hybrid_retrieval,
        "search_chunks",
        lambda **kwargs: vector_results,
    )
    monkeypatch.setattr(
        hybrid_retrieval,
        "keyword_search",
        lambda **kwargs: keyword_results,
    )

    results = hybrid_retrieval.hybrid_search(
        query=query,
        n_results=3,
    )

    result_ids = [item["id"] for item in results]

    assert len(results) == 3
    assert set(result_ids) == {"chunk-a", "chunk-b", "chunk-c"}
    assert result_ids[0] == "chunk-a"
