
from pathlib import Path
from pypdf import PdfReader

PDF_PATH = Path("uploads/rag_research_paper.pdf")
OUTPUT_PATH = Path("uploads/rag_research_paper_extracted.txt")


def extract_pdf_text(pdf_path: Path) -> list[dict]:
    """Extract text page by page, preserving page numbers."""
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page_number": page_number,
                "text": text.strip(),
            })

    return pages


if __name__ == "__main__":
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    extracted_pages = extract_pdf_text(PDF_PATH)

    combined_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in extracted_pages
    )

    OUTPUT_PATH.write_text(combined_text, encoding="utf-8")

    total_words = sum(
        len(page["text"].split()) for page in extracted_pages
    )

    print(f"PDF: {PDF_PATH.name}")
    print(f"Pages containing text: {len(extracted_pages)}")
    print(f"Total extracted words: {total_words}")
    print(f"Saved extracted text to: {OUTPUT_PATH}")
    print("\nPreview:")
    print(combined_text[:1000])
