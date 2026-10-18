
from typing import List, Dict


def fixed_size_chunking(
    text: str,
    chunk_size: int = 150,
) -> List[Dict]:
    """
    Split text into fixed-size word chunks without overlap.

    chunk_size: maximum number of words in each chunk.
    """
    words = text.split()
    chunks = []

    for start in range(0, len(words), chunk_size):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])

        chunks.append({
            "chunk_index": len(chunks),
            "text": chunk_text,
            "start_word": start,
            "end_word": end,
        })

    return chunks


def overlapping_chunking(
    text: str,
    chunk_size: int = 150,
    overlap: int = 30,
) -> List[Dict]:
    """
    Split text into fixed-size word chunks with overlap.

    Each chunk shares some words with the preceding chunk
    to help preserve context across boundaries.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])

        chunks.append({
            "chunk_index": len(chunks),
            "text": chunk_text,
            "start_word": start,
            "end_word": end,
        })

        if end == len(words):
            break

    return chunks
