
from hybrid_retrieval import hybrid_search

query = (
    "How does retrieval-augmented generation combine "
    "retrieved knowledge with a language model?"
)

results = hybrid_search(query, n_results=5)

for rank, result in enumerate(results, start=1):
    print(f"\nHybrid Result {rank}")
    print("Chunk ID:", result["id"])
    print("Metadata:", result["metadata"])
    print("RRF score:", round(result["rrf_score"], 6))
    print("Retrieved by:", result["retrieved_by"])
    print("Passage:", result["text"][:500])
