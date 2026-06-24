"""Persistent evidence store for GEO Agent runs."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .engine_sampling import EngineRun


SCHEMA = """
CREATE TABLE IF NOT EXISTS engine_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    engine TEXT NOT NULL,
    query TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    region TEXT NOT NULL,
    language TEXT NOT NULL,
    raw_answer TEXT NOT NULL,
    citations_json TEXT NOT NULL,
    mentions_json TEXT NOT NULL,
    recommendations_json TEXT NOT NULL,
    source_domains_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_engine_runs_query ON engine_runs(query);
CREATE INDEX IF NOT EXISTS idx_engine_runs_engine ON engine_runs(engine);
"""


class EvidenceStore:
    """SQLite-backed store for raw query-answer-citation evidence."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self._connection = sqlite3.connect(self.path)
        self._connection.row_factory = sqlite3.Row
        self._connection.executescript(SCHEMA)
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def save_run(self, run: EngineRun) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO engine_runs (
                engine, query, timestamp, region, language, raw_answer,
                citations_json, mentions_json, recommendations_json, source_domains_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run.engine,
                run.query,
                run.timestamp,
                run.region,
                run.language,
                run.raw_answer,
                _dump(run.citations),
                _dump(run.mentions),
                _dump(run.recommendations),
                _dump(run.source_domains),
            ),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def save_runs(self, runs: Iterable[EngineRun]) -> list[int]:
        return [self.save_run(run) for run in runs]

    def list_runs(self, *, query: str | None = None, engine: str | None = None) -> list[EngineRun]:
        sql = "SELECT * FROM engine_runs"
        filters: list[str] = []
        params: list[str] = []
        if query is not None:
            filters.append("query = ?")
            params.append(query)
        if engine is not None:
            filters.append("engine = ?")
            params.append(engine)
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY id ASC"
        rows = self._connection.execute(sql, params).fetchall()
        return [_row_to_run(row) for row in rows]

    def count_runs(self) -> int:
        return int(self._connection.execute("SELECT COUNT(*) FROM engine_runs").fetchone()[0])

    def __enter__(self) -> "EvidenceStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def _dump(values: tuple[str, ...]) -> str:
    return json.dumps(list(values), sort_keys=True)


def _load(value: str) -> tuple[str, ...]:
    return tuple(str(item) for item in json.loads(value))


def _row_to_run(row: sqlite3.Row) -> EngineRun:
    return EngineRun(
        engine=row["engine"],
        query=row["query"],
        timestamp=row["timestamp"],
        region=row["region"],
        language=row["language"],
        raw_answer=row["raw_answer"],
        citations=_load(row["citations_json"]),
        mentions=_load(row["mentions_json"]),
        recommendations=_load(row["recommendations_json"]),
        source_domains=_load(row["source_domains_json"]),
    )
