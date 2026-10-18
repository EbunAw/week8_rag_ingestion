from embeddings import generate_embedding

sample_text = "Retrieval-augmented generation combines retrieval with text generation."

vector = generate_embedding(sample_text)

print("Embedding dimensions:", len(vector))
print("First five values:", vector[:5])