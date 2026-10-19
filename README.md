# Week 8: RAG Document Ingestion Pipeline

## Project Overview

This project implements the document ingestion and retrieval-preparation stages of a Retrieval-Augmented Generation (RAG) pipeline.

It allows a user to upload a PDF, extract its text, split the text into chunks, generate embeddings, and store the chunks and their metadata in a Chroma vector database. The stored vectors can then be searched to retrieve passages relevant to a user’s query.

The goal is to prepare document content for use by a language model. Generating a final answer with an LLM is outside the scope of this project.

## Pipeline

**Upload PDF → Extract text → Chunk → Generate embeddings → Store in Chroma → Retrieve relevant chunks**

## Technologies Used

- Python
- FastAPI
- PyPDF
- Sentence Transformers (`all-MiniLM-L6-v2`)
- ChromaDB
- HTML for the upload interface
- pytest for automated tests
- GitHub Actions for continuous integration (CI)

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

For retrieval, I used the overlapping chunks because retaining context between adjacent passages can be helpful. The initial retrieval test returned relevant passages from the indexed research paper. A more thorough comparison would evaluate passage relevance across several queries.

## Embeddings

The project uses the local Sentence Transformers model `all-MiniLM-L6-v2` to convert text chunks and search queries into numerical vectors.

Using a local embedding model allowed the pipeline to continue when the external embedding API reached its usage quota.

## Vector Store: ChromaDB

I chose ChromaDB because it supports persistent local vector storage, similarity search, and metadata associated with stored documents. It was suitable for this lab because it allowed me to implement and test the pipeline locally.

The ingestion pipeline stores the two chunking strategies in separate Chroma collections, allowing them to be compared independently.

Chunks include source-related metadata so retrieved passages can be traced back to the indexed document.

## Retrieval Test

I tested semantic retrieval using a question about the research paper:

> What is retrieval-augmented generation (RAG), and how does retrieving relevant document chunks help a language model answer questions?

The retrieval workflow returned passages from the indexed PDF and used them to produce a response. This demonstrates that the stored embeddings can be searched using a query embedding and that retrieved passages can be used as context for an answer.

The test is an initial functional check, not