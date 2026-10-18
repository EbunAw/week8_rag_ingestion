# Week 8: RAG Document Ingestion Pipeline

## Project Overview

This project implements the ingestion half of a Retrieval-Augmented Generation (RAG) pipeline. It allows a user to upload a PDF, extract its text, split the text into chunks, generate embeddings, and store the chunks and their metadata in a Chroma vector database.

The purpose is to prepare document content for semantic retrieval, so relevant passages can later be supplied to a language model.

## Pipeline

**Upload PDF → Extract text → Chunk → Generate embeddings → Store in Chroma → Retrieve relevant chunks**

## Technologies Used

- Python
- FastAPI
- PyPDF
- Sentence Transformers (`all-MiniLM-L6-v2`)
- ChromaDB
- HTML for the upload interface

## Chunking Strategies

I implemented and compared two chunking strategies using the same 19-page research paper.

### 1. Fixed-size chunking

The document is split into chunks of approximately 150 words, without overlap.

**Advantages**
- Simple and consistent chunk sizes.
- Avoids storing repeated text between chunks.

**Limitations**
- Important context may be split across chunk boundaries.

### 2. Overlapping chunking

The document is split into 150-word chunks with a 30-word overlap between consecutive chunks.

**Advantages**
- Preserves some context across neighbouring chunks.
- May improve retrieval when relevant information falls near a chunk boundary.

**Limitations**
- Creates more chunks and stores some repeated text.

### Comparison Results

| Strategy | Chunk size | Overlap | Chunks produced |
|---|---:|---:|---:|
| Fixed-size | 150 words | 0 words | 66 |
| Overlapping | 150 words | 30 words | 83 |

Both strategies were applied to the same document. Overlapping chunking produced more chunks because neighbouring chunks share some text.

For retrieval, I selected the overlapping chunks because retaining context between adjacent passages can be helpful. The retrieval test returned three passages for a sample query. This was an initial test; a more thorough comparison would assess passage relevance across several queries.

## Embeddings

The project uses the local Sentence Transformers model `all-MiniLM-L6-v2` to convert text chunks and search queries into numerical vectors.

Using a local embedding model allowed the pipeline to continue when the external embedding API reached its usage quota.

## Vector Store: ChromaDB

I chose ChromaDB because it supports persistent local vector storage, similarity search, and metadata associated with stored documents. It was suitable for this lab because it allowed me to implement and test the pipeline locally.

Each stored chunk should include useful metadata such as its source document and page number, allowing retrieved passages to be traced back to their origin.

## Retrieval Test

I tested semantic retrieval with the query:

> How does retrieval-augmented generation combine retrieved knowledge with a language model?

The retrieval test successfully returned the top three matching passages from the indexed research paper. This confirms that the stored embeddings can be searched using a query embedding.

## Upload Safety

**Confirm these safeguards are implemented before submission:**

- [ ] The endpoint validates that uploads are PDFs.
- [ ] The endpoint enforces a maximum file size.
- [ ] The application processes uploaded files locally and does not fetch user-supplied URLs.

Only check these boxes once you have verified the corresponding safeguards in your code.

## Running the Project

1. Create and activate the project’s Python virtual environment.
2. Install the dependencies listed in `requirements.txt`.
3. Start the FastAPI application:

   ```bash
   python -m uvicorn main:app --port 8001
   ```

4. Open `http://127.0.0.1:8001` in your browser.
5. Upload a PDF to run the ingestion pipeline.
6. Run the retrieval test:

   ```bash
   python test_retrieval.py
   ```

## Current Milestone

The PDF ingestion, chunking, local embedding, Chroma storage, and retrieval test have been implemented and tested.

This project covers the ingestion and retrieval preparation stage of RAG. Generating a final language-model answer from retrieved passages is a separate step.
