from embeddings import generate_embedding
from vector_store import get_collection

collection = get_collection()

query = "How does retrieval-augmented generation combine retrieved knowledge with a language model?"

# Embed the user's query using the same embedding model
query_vector = generate_embedding(query)

# Retrieve the three most similar paper chunks
results = collection.query(
    query_embeddings=[query_vector],
    n_results=3,
    include=["documents", "metadatas", "distances"],
)

for rank, document in enumerate(results["documents"][0], start=1):
    metadata = results["metadatas"][0][rank - 1]
    distance = results["distances"][0][rank - 1]

    print(f"\nResult {rank} | Distance: {distance:.4f}")
    print("Metadata:", metadata)
    print("Passage:", document[:500])