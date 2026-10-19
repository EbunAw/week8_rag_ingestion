from chunking import fixed_size_chunking, overlapping_chunking


def test_fixed_size_chunking_returns_chunks():
    text = " ".join(f"word{i}" for i in range(350))

    chunks = fixed_size_chunking(text, chunk_size=150)

    assert len(chunks) == 3
    assert chunks[0]["text"].split() == [
        f"word{i}" for i in range(150)
    ]


def test_overlapping_chunking_returns_chunks():
    text = " ".join(f"word{i}" for i in range(350))

    chunks = overlapping_chunking(
        text,
        chunk_size=150,
        overlap=30
    )

    assert len(chunks) == 3

    # The last 30 words of chunk 1 should appear
    # as the first 30 words of chunk 2.
    first_chunk_words = chunks[0]["text"].split()
    second_chunk_words = chunks[1]["text"].split()

    assert first_chunk_words[-30:] == second_chunk_words[:30]