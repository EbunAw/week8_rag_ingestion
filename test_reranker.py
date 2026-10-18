
from reranker import rerank_results

query = (
    "How does retrieval-augmented generation combine "
    "retrieved knowledge with a language model?"
)

results = rerank_results(
    query=query,
    candidate_count=10,
    n_results=5,
)

for rank, result in enumerate(results, start=1):
    print(f"\nReranked Result {rank}")
    print("Chunk ID:", result["id"])
    print("Source:", result["metadata"]["source"])
    print("Chunk index:", result["metadata"]["chunk_index"])
    print("Reranker score:", round(result["reranker_score"], 4))
    print("Retrieved by:", result["retrieved_by"])
    print("Passage:", result["text"][:500])
