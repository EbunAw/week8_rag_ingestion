
from keyword_search import keyword_search

query = (
    "How does retrieval augmented generation "
    "combine retrieved knowledge with a language model?"
)

results = keyword_search(query, n_results=3)

for rank, result in enumerate(results, start=1):
    print(f"\nResult {rank}")
    print("Metadata:", result["metadata"])
    print("Keyword score:", result["keyword_score"])
    print("Passage:", result["text"][:500])
