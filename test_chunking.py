from chunking import fixed_size_chunking, overlapping_chunking


def test_chunking_strategies():
    # Small sample text so GitHub Actions doesn't need your research paper
    sample_text = (
        "Retrieval augmented generation combines document retrieval "
        "with language generation. Documents are split into chunks "
        "so relevant information can be retrieved efficiently. "
        "Overlapping chunks help preserve context between sections. "
    ) * 30

    fixed_chunks = fixed_size_chunking(sample_text, chunk_size=150)
    overlap_chunks = overlapping_chunking(
        sample_text,
        chunk_size=150,
        overlap=30
    )

    # Confirm both strategies produce chunks
    assert len(fixed_chunks) > 0
    assert len(overlap_chunks) > 0

    # Confirm each chunk contains text
    assert all(chunk["text"].strip() for chunk in fixed_chunks)
    assert all(chunk["text"].strip() for chunk in overlap_chunks)