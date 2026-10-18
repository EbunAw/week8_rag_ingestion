import chromadb

client = chromadb.PersistentClient(path="chroma_db")


def get_collection(collection_name: str = "rag_overlapping"):
    """Get or create a Chroma collection for a chunking strategy."""
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"description": f"Research paper chunks: {collection_name}"},
    )


def store_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
    source: str,
    collection_name: str = "rag_overlapping",
) -> None:
    """Store chunks, embeddings, and source metadata in Chroma."""
    if len(chunks) != len(embeddings):
        raise ValueError("Each chunk must have a corresponding embedding.")

    collection = get_collection(collection_name)

    collection.upsert(
        ids=[f"{source}_{chunk['chunk_index']}" for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "source": source,
                "chunk_index": chunk["chunk_index"],
                "start_word": chunk["start_word"],
                "end_word": chunk["end_word"],
            }
            for chunk in chunks
        ],
    )

def search_chunks(
    query_embedding: list[float],
    n_results: int = 3,
    collection_name: str = "rag_overlapping",
) -> dict:
    """Retrieve the most relevant stored chunks."""
    collection = get_collection(collection_name)

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )