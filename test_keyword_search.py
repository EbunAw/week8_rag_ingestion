import sqlite3

import keyword_search


def test_keyword_search(tmp_path, monkeypatch):
    # Give this test its own temporary SQLite database.
    test_db = tmp_path / "test_keyword_index.db"
    monkeypatch.setattr(keyword_search, "DB_PATH", str(test_db))

    with sqlite3.connect(test_db) as conn:
        conn.execute("""
            CREATE TABLE chunks (
                chunk_id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                source TEXT,
                chunk_index INTEGER
            )
        """)

        conn.execute("""
            CREATE VIRTUAL TABLE chunks_fts
            USING fts5(text, content='chunks', content_rowid='rowid')
        """)

        conn.execute(
            """
            INSERT INTO chunks (chunk_id, text, source, chunk_index)
            VALUES (?, ?, ?, ?)
            """,
            (
                "sample-1",
                "RAG retrieves relevant documents and uses them to generate answers.",
                "sample.txt",
                0,
            ),
        )

        # Populate FTS from the chunks table.
        conn.execute("""
            INSERT INTO chunks_fts(chunks_fts) VALUES ('rebuild')
        """)

    results = keyword_search.keyword_search("retrieves relevant documents")

    assert results
    assert results[0]["id"] == "sample-1"