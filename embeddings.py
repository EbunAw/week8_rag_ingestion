from sentence_transformers import SentenceTransformer

# Downloads the model once, then runs it locally
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)


def generate_embedding(text: str) -> list[float]:
    """Convert one text chunk into a numerical embedding."""
    embedding = model.encode(text)
    return embedding.tolist()


def generate_embeddings(texts, batch_size=50):
    """Convert multiple text chunks into numerical embeddings."""
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
    )
    return embeddings.tolist()