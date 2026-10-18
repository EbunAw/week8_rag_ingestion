from pathlib import Path

from chunking import fixed_size_chunking, overlapping_chunking
from embeddings import generate_embeddings
from vector_store import store_chunks

TEXT_PATH = Path("uploads/rag_research_paper_extracted.txt")
SOURCE_NAME = "rag_research_paper.pdf"


def ingest_paper() -> None:
    if not TEXT_PATH.exists():
        raise FileNotFoundError(f"Extracted text not found: {TEXT_PATH}")

    text = TEXT_PATH.read_text(encoding="utf-8")
    print(f"Text loaded: {len(text.split())} words")

    # Prepare both chunking strategies
    strategies = {
        "rag_fixed": fixed_size_chunking(text, chunk_size=150),
        "rag_overlapping": overlapping_chunking(
            text,
            chunk_size=150,
            overlap=30,
        ),
    }

    for collection_name, chunks in strategies.items():
        print(f"\n{collection_name}: {len(chunks)} chunks")

        # Generate vectors for this strategy's chunks
        embeddings = generate_embeddings(
            [chunk["text"] for chunk in chunks]
        )
        print(f"Embeddings generated: {len(embeddings)}")

        # Store in the strategy-specific Chroma collection
        store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            source=SOURCE_NAME,
            collection_name=collection_name,
        )

        print(f"Stored in Chroma collection: {collection_name}")


if __name__ == "__main__":
    ingest_paper()