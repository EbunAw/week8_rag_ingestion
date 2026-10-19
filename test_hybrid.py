from hybrid_retrieval import hybrid_search


def test_hybrid_search():
    query = "What are the two variants of RAG, and how do they differ?"

    results = hybrid_search(query, n_results=5)

    assert isinstance(results, list)