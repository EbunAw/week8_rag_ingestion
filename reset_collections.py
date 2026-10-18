import chromadb

client = chromadb.PersistentClient(path="chroma_db")

for name in ["rag_fixed", "rag_overlapping"]:
    try:
        client.delete_collection(name)
        print(f"Deleted old collection: {name}")
    except Exception:
        print(f"Collection {name} did not exist.")

print("Database cleanup complete.")