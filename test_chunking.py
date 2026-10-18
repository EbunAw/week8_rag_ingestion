from pathlib import Path
from chunking import fixed_size_chunking, overlapping_chunking

# Read the text extracted from the research paper
text_path = Path("uploads/rag_research_paper_extracted.txt")
paper_text = text_path.read_text(encoding="utf-8")

# Apply both chunking strategies
fixed_chunks = fixed_size_chunking(paper_text, chunk_size=150)
overlap_chunks = overlapping_chunking(
    paper_text,
    chunk_size=150,
    overlap=30
)

# Compare the results
print(f"Total words in paper: {len(paper_text.split())}")
print(f"Fixed-size chunks: {len(fixed_chunks)}")
print(f"Overlapping chunks: {len(overlap_chunks)}")

print("\nFirst fixed-size chunk:")
print(fixed_chunks[0]["text"])

print("\nFirst overlapping chunk:")
print(overlap_chunks[0]["text"])
