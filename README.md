# RAG Document Ingestion, Hybrid Retrieval, Reranking, and Answer Generation

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline that ingests PDF documents, retrieves relevant passages, and uses retrieved context to generate answers with source citations.

Users can upload a PDF, extract its text, split the content into chunks, generate embeddings, and store the chunks and metadata in ChromaDB. The system retrieves relevant passages using semantic vector search and keyword search, combines the results using Reciprocal Rank Fusion (RRF), and reranks candidate passages using a CrossEncoder.

The `/ask` endpoint extends the pipeline by passing retrieved passages to a language model to generate answers grounded in the document context. The response includes citation references and source information to help users inspect the evidence behind an answer.

## End-to-End Pipeline

**Upload PDF → Extract text → Chunk → Generate embeddings → Store in ChromaDB → Hybrid retrieval → RRF fusion → CrossEncoder reranking → Grounded answer generation with citations**

## Technologies Used

- Python
- FastAPI
- PyPDF
- Sentence Transformers (`all-MiniLM-L6-v2`)
- ChromaDB
- SQLite FTS5
- CrossEncoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
- Google Gemini for answer generation
- Pytest
- GitHub Actions
- HTML for the upload interface

## 1. Document Ingestion

The ingestion pipeline accepts a PDF, extracts its text, divides it into chunks, generates an embedding for each chunk, and stores the resulting vectors and metadata in ChromaDB.

Chunk metadata can include the source document and chunk index. This information helps identify where retrieved content originated.

## 2. Chunking Strategies

I implemented and compared two chunking strategies using the same 19-page research paper.

### Fixed-size chunking

The document is split into chunks of approximately 150 words, without overlap.

**Advantages**
- Produces consistent chunk sizes.
- Avoids storing repeated text between chunks.

**Limitations**
- Relevant information or context may be split across chunk boundaries.

### Overlapping chunking

The document is split into 150-word chunks, with a 30-word overlap between consecutive chunks.

**Advantages**
- Preserves some context between neighbouring chunks.
- May improve retrieval when relevant information falls near a chunk boundary.

**Limitations**
- Produces more chunks.
- Stores some repeated text.

### Chunking Comparison

| Strategy | Chunk size | Overlap | Chunks produced |
|---|---:|---:|---:|
| Fixed-size | 150 words | 0 words | 66 |
| Overlapping | 150 words | 30 words | 83 |

Both strategies were applied to the same document. Overlapping chunking produced more chunks because adjacent chunks share some text.

I selected overlapping chunking for retrieval because retaining context between neighbouring passages may help preserve useful information.

The initial retrieval test returned three passages for a sample query. This was a preliminary check; a more comprehensive evaluation would compare relevance across multiple queries.

## 3. Embeddings

The project uses the local Sentence Transformers model `all-MiniLM-L6-v2` to convert document chunks and search queries into numerical vectors.

A local embedding model allows the pipeline to generate embeddings without depending on an external embedding API. This was useful when the external API reached its usage quota.

## 4. Vector Store: ChromaDB

ChromaDB is used to persist document chunk embeddings and perform semantic similarity search.

It was selected because it supports local persistent vector storage, similarity search, and metadata associated with stored documents. This made it suitable for implementing and testing the pipeline locally.

## 5. Week 9: Hybrid Retrieval

Week 9 extends the project with hybrid retrieval, which combines semantic vector search with keyword-based search.

### Vector retrieval

Vector retrieval uses embeddings to find passages that are semantically related to the user's query, even when they do not contain the exact query words.

### Keyword retrieval

Keyword retrieval uses SQLite FTS5 to search indexed chunk text for query terms. It can help identify passages containing important words or phrases.

### Reciprocal Rank Fusion (RRF)

The ranked results from vector retrieval and keyword retrieval are combined using Reciprocal Rank Fusion (RRF).

RRF uses the rankings from the separate retrieval methods to produce a unified list of candidate passages. Combining the methods can help balance semantic relevance with exact keyword matches.

## 6. CrossEncoder Reranking

After hybrid retrieval returns candidate passages, a CrossEncoder evaluates the relevance of each query–passage pair.

The candidates are assigned reranking scores, sorted by those scores, and the highest-ranked passages are returned.

This adds a relevance-scoring stage after the initial retrieval process.

## 7. Week 9: Grounded Answer Generation (`POST /ask`)

The `/ask` endpoint extends the retrieval pipeline by generating an answer from passages retrieved from the ingested documents.

When a user submits a question, the system retrieves and reranks candidate passages, supplies the selected passages as context to the language model, and requests an answer based on that context.

The endpoint returns:
- The submitted question.
- The generated answer.
- Source records for the retrieved passages.
- Citation identifiers that connect the answer to those source records.

### Request

`POST /ask`

Example request body:

```json
{
  "question": "What does the paper say about RAG-Token and the documents used during generation?"
}
```

### Response format

The endpoint returns the question, generated answer, and retrieved sources. The following is an illustrative response structure:

```json
{
  "question": "What does the paper say about RAG-Token and the documents used during generation?",
  "answer": "The answer is generated from retrieved passages and includes source citations such as [S1].",
  "sources": [
    {
      "citation_id": "S1",
      "source": "rag_research_paper.pdf",
      "chunk_index": 12,
      "chunk_id": "rag_research_paper.pdf_12",
      "rrf_score": 0.02,
      "excerpt": "Relevant retrieved text from the source document..."
    }
  ]
}
```

### Citation format

The generated answer uses citation labels such as `[S1]` and `[S2]`. Each label corresponds to a `citation_id` in the response's `sources` array.

Source records identify the document and retrieved chunk and include an excerpt. These excerpts allow users to inspect the passages retrieved as evidence for the answer.

The endpoint is designed to answer using retrieved context. When the retrieved passages do not provide enough information, the answer should indicate that the evidence is insufficient rather than inventing details.

### Testing the `/ask` endpoint

The endpoint was tested locally through FastAPI's interactive API documentation. Test questions were submitted about the ingested research paper, and the responses included generated answers and source citation references.

For a meaningful grounding check, verify that:
1. Citation labels in the answer match `citation_id` values in `sources`.
2. The cited excerpts support the claims made in the answer.
3. The response acknowledges when the retrieved context does not contain enough information.

## 8. Retrieval Example

An example query used during retrieval testing was:

> How does retrieval-augmented generation combine retrieved knowledge with a language model?

The ingestion and retrieval pipeline was tested by retrieving passages from the indexed research paper.

The initial retrieval test confirmed that stored embeddings could be searched using a query embedding. Retrieval quality would require a broader evaluation using multiple queries and relevance checks.

## 9. Testing

The project includes pytest tests for the retrieval and reranking components.

The tests cover the relevant retrieval and ranking logic. Where appropriate, mocked retrieval results are used so that core logic can be tested without depending on locally populated databases.

Run the test suite from the project directory:

```bash
python -m pytest -q
```

The test suite passed locally, and the GitHub Actions workflow completed successfully.

## 10. Upload Safety

Before deployment or submission, verify that the upload endpoint includes the following safeguards:

- [ ] Validates that uploaded files are PDFs.
- [ ] Enforces a maximum file size.
- [ ] Processes uploaded files locally and does not fetch user-supplied URLs.

Only mark these items as complete after confirming that the safeguards are implemented in the code.

## 11. Running the Project

### Set up the environment

1. Create and activate the project's Python virtual environment.
2. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Configure any required environment variables, such as the Gemini API key, according to the project's setup.

### Start the FastAPI application

Run the application from the project directory:

```bash
python -m uvicorn main:app --reload --port 8003
```

Open the interactive API documentation:

`http://127.0.0.1:8003/docs`

Use the application to upload and ingest a PDF. Then use `POST /ask` in the API documentation to submit a question about the ingested content.

### Run the tests

From the project directory:

```bash
python -m pytest -q
```

## 12. Project Scope and Current Milestone

The project implements PDF ingestion, text extraction, chunking, local embedding generation, ChromaDB storage, hybrid retrieval, CrossEncoder reranking, and grounded answer generation with source citations.

The Week 8 work focused on preparing documents for retrieval. Week