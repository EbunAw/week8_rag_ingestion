from vector_store import get_collection

collection = get_collection()

print("Chunks stored:", collection.count())

results = collection.get(
    limit=2,
    include=["documents", "metadatas"],
)

for i, document in enumerate(results["documents"]):
    print(f"\nRecord {i + 1}")
    print("Metadata:", results["metadatas"][i])
    print("Text preview:", document[:300])