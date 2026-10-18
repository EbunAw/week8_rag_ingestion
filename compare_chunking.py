from embeddings import generate_embedding
from vector_store import get_collection

queries = [
    "What is the difference between parametric and non-parametric memory in RAG?",
    "How do RAG-Sequence and RAG-Token differ?",
    "What benefits did the authors observe when using RAG compared with a parametric-only model?",
]

collections = {
    "Fixed-size (no overlap)": get_collection("rag_fixed"),
    "Overlapping (30-word overlap)": get_collection("rag_overlapping"),
}

for query in queries:
    print(f"\n\nQUESTION: {query}")

    # Use the same query vector to search both collections
    query_vector = generate_embedding(query)

    for strategy, collection in collections.items():
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=3,
            include=["documents", "metadatas", "distances"],
        )

        print(f"\n--- {strategy} ---")

        for rank, document in enumerate(results["documents"][0], start=1):
            metadata = results["metadatas"][0][rank - 1]
            distance = results["distances"][0][rank - 1]

            print(
                f"\n{rank}. Distance: {distance:.4f} | "
                f"Chunk: {metadata['chunk_index']} | "
                f"Words: {metadata['start_word']}–{metadata['end_word']}"
            )
            print("Passage:", document[:450])