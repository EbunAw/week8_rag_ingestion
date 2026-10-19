import reranker


def test_reranker_sorts_candidates_by_score(monkeypatch):
    # Mock hybrid retrieval so this test doesn't need local databases.
    candidates = [
        {
            "id": "chunk-a",
            "text": "Passage A",
            "metadata": {"source": "sample.txt", "chunk_index": 0},
        },
        {
            "id": "chunk-b",
            "text": "Passage B",
            "metadata": {"source": "sample.txt", "chunk_index": 1},
        },
    ]

    monkeypatch.setattr(
        reranker,
        "hybrid_search",
        lambda **kwargs: candidates,
    )

    # Mock CrossEncoder scores: passage B should rank above A.
    monkeypatch.setattr(
        reranker.reranker,
        "predict",
        lambda pairs: [0.2, 0.9],
    )

    results = reranker.rerank_results(
        query="sample question",
        candidate_count=2,
        n_results=2,
    )

    assert [item["id"] for item in results] == ["chunk-b", "chunk-a"]
    assert results[0]["reranker_score"] == 0.9