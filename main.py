from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from extract_pdf import extract_pdf_text
from embeddings import generate_embeddings
from vector_store import store_chunks


app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RAG PDF Ingestion</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 650px;
            margin: 50px auto;
            padding: 20px;
            background: #f4f7fb;
        }
        .container {
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        button {
            background: #34306f;
            color: white;
            padding: 12px 18px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        #status {
            margin-top: 20px;
            white-space: pre-line;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>PDF Ingestion for RAG</h1>
        <p>Upload a PDF to extract text, create chunks and embeddings, and store them in ChromaDB.</p>

        <form id="uploadForm">
            <input type="file" id="pdfFile" accept=".pdf" required>
            <button id="uploadButton" type="submit">Upload and Ingest PDF</button>
        </form>

        <div id="status"></div>
    </div>

    <script>
        const form = document.getElementById("uploadForm");
        const fileInput = document.getElementById("pdfFile");
        const button = document.getElementById("uploadButton");
        const statusBox = document.getElementById("status");

        form.addEventListener("submit", async function(event) {
            event.preventDefault();

            const file = fileInput.files[0];
            if (!file) {
                statusBox.textContent = "Please choose a PDF.";
                return;
            }

            const data = new FormData();
            data.append("file", file);

            button.disabled = true;
            button.textContent = "Processing...";
            statusBox.textContent = "Uploading and processing your PDF. Please wait.";

            try {
                const response = await fetch("/upload", {
                    method: "POST",
                    body: data
                });

const responseText = await response.text();

let result;
try {
    result = JSON.parse(responseText);
} catch {
    throw new Error(responseText || "The server returned an empty response.");
}
                if (!response.ok) {
                    throw new Error(result.detail || "Upload failed.");
                }

                statusBox.textContent =
                    "Ingestion complete!\\n" +
                    "Pages: " + result.pages + "\\n" +
                    "Fixed chunks: " + result.fixed_chunks + "\\n" +
                    "Overlapping chunks: " + result.overlapping_chunks;

            } catch (error) {
                statusBox.textContent = "Error: " + error.message;
            } finally {
                button.disabled = false;
                button.textContent = "Upload and Ingest PDF";
            }
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE


def make_chunks(text, chunk_size=150, overlap=0):
    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks = []

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]

        chunks.append({
            "chunk_index": len(chunks),
            "text": " ".join(chunk_words),
            "start_word": start,
            "end_word": start + len(chunk_words)
        })

        if start + chunk_size >= len(words):
            break

    return chunks


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF.")

    filename = Path(file.filename).name
    pdf_path = UPLOAD_DIR / filename
    pdf_path.write_bytes(await file.read())

    pages = extract_pdf_text(pdf_path)

    document_text = "\n\n".join(
        page.get("text", "") for page in pages
    ).strip()

    if not document_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text was extracted from the PDF."
        )

    fixed_chunks = make_chunks(document_text, 150, 0)
    overlapping_chunks = make_chunks(document_text, 150, 30)

    fixed_embeddings = generate_embeddings(
        [chunk["text"] for chunk in fixed_chunks]
    )

    overlapping_embeddings = generate_embeddings(
        [chunk["text"] for chunk in overlapping_chunks]
    )

    store_chunks(
        fixed_chunks,
        fixed_embeddings,
        filename,
        "rag_fixed"
    )

    store_chunks(
        overlapping_chunks,
        overlapping_embeddings,
        filename,
        "rag_overlapping"
    )

    return JSONResponse({
        "pages": len(pages),
        "fixed_chunks": len(fixed_chunks),
        "overlapping_chunks": len(overlapping_chunks)
    })