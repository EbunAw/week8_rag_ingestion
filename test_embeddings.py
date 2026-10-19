from unittest.mock import patch
from unittest.mock import MagicMock

from embeddings import generate_embedding


def test_generate_embedding_returns_vector():
    sample_text = "RAG combines retrieval with text generation."

    fake_embedding = MagicMock()
    fake_embedding.tolist.return_value = [0.1, 0.2, 0.3]

    with patch("embeddings.model.encode", return_value=fake_embedding):
        result = generate_embedding(sample_text)

    assert isinstance(result, list)
    assert result == [0.1, 0.2, 0.3]