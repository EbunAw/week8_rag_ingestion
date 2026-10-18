
import re
import sqlite3

from vector_store import get_collection


DB_PATH = "keyword_index.db"


def rebuild_keyword_index(
    collection_name: str = "rag_overlapping",
) -> None:
    """Build a keyword index from chunks already stored in Chroma."""

    collection = get_collection(collection_name)

    stored = collection.get(
        include=["documents", "metadatas"]
    )

    with sqlite3.connect(DB_PATH) as conn:
        # Store chunk information alongside the searchable text.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                source TEXT,
                chunk_index INTEGER
            )
        """)

        # FTS5 provides full-text keyword search.
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
            USING fts5(
                text,
                content='chunks',
                content_rowid='rowid'
            )
        """)

        # Clear old entries before rebuilding.
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM chunks_fts")

        for chunk_id, document, metadata in zip(
            stored["ids"],
            stored["documents"],
            stored["metadatas"],
        ):
            conn.execute(
                """
                INSERT INTO chunks (
                    chunk_id, text, source, chunk_index
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    chunk_id,
                    document,
                    metadata.get("source", ""),
                    metadata.get("chunk_index", -1),
                ),
            )

        # Populate the full-text index from the stored chunks.
        conn.execute("""
            INSERT INTO chunks_fts(chunks_fts)
            VALUES ('rebuild')
        """)

    print(f"Indexed {len(stored['ids'])} chunks.")


def keyword_search(
    query: str,
    n_results: int = 5,
) -> list[dict]:
    """Retrieve chunks using keyword matching."""

    # Extract words and construct a safe FTS query.
    terms = re.findall(r"\w+", query.lower())

    if not terms:
        return []

    fts_query = " OR ".join(
        f'"{term}"' for term in terms
    )

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT
                chunks.chunk_id,
                chunks.text,
                chunks.source,
                chunks.chunk_index,
                bm25(chunks_fts) AS score
            FROM chunks_fts
            JOIN chunks
                ON chunks.rowid = chunks_fts.rowid
            WHERE chunks_fts MATCH ?
            ORDER BY score ASC
            LIMIT ?
            """,
            (fts_query, n_results),
        ).fetchall()

    return [
        {
            "id": row[0],
            "text": row[1],
            "metadata": {
                "source": row[2],
                "chunk_index": row[3],
            },
            "keyword_score": row[4],
        }
        for row in rows
    ]
