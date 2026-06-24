"""Persistent evidence store for GEO Agent evidence."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .engine_sampling import EngineRun
from .failure_debugger import FailureDiagnosis
from .optimization_tasks import OptimizationTaskBrief
from .page_inventory import PageInventoryRecord
from .query_space import QueryRecord


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

CREATE TABLE IF NOT EXISTS query_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    intent_type TEXT NOT NULL,
    funnel_stage TEXT NOT NULL,
    language TEXT NOT NULL,
    region TEXT NOT NULL,
    target_engine TEXT NOT NULL,
    competitor_entities_json TEXT NOT NULL,
    expected_answer_format TEXT NOT NULL,
    priority_score REAL NOT NULL,
    cluster TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_query_records_cluster ON query_records(cluster);

CREATE TABLE IF NOT EXISTS page_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    title TEXT,
    h1 TEXT,
    schema_types_json TEXT NOT NULL,
    last_modified TEXT,
    canonical_url TEXT NOT NULL,
    content_chunks_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_page_inventory_canonical ON page_inventory(canonical_url);

CREATE TABLE IF NOT EXISTS failure_diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    failure_types_json TEXT NOT NULL,
    explanation TEXT NOT NULL,
    next_step TEXT NOT NULL,
    evidence_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS optimization_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    target_page TEXT NOT NULL,
    query_cluster TEXT NOT NULL,
    expected_impact TEXT NOT NULL,
    confidence REAL NOT NULL,
    risk TEXT NOT NULL,
    draft_content TEXT NOT NULL,
    retest_plan TEXT NOT NULL,
    failure_type TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_optimization_tasks_action ON optimization_tasks(action_type);

CREATE TABLE IF NOT EXISTS report_artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    format TEXT NOT NULL,
    content TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_report_artifacts_format ON report_artifacts(format);
"""


@dataclass(frozen=True)
class ReportArtifact:
    name: str
    format: str
    content: str


class EvidenceStore:
    """SQLite-backed store for raw and derived GEO evidence."""

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
        rows = self._select(sql, filters, params)
        return [_row_to_run(row) for row in rows]

    def count_runs(self) -> int:
        return int(self._connection.execute("SELECT COUNT(*) FROM engine_runs").fetchone()[0])

    def save_query_record(self, record: QueryRecord) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO query_records (
                query, intent_type, funnel_stage, language, region, target_engine,
                competitor_entities_json, expected_answer_format, priority_score, cluster
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.query,
                record.intent_type,
                record.funnel_stage,
                record.language,
                record.region,
                record.target_engine,
                _dump(record.competitor_entities),
                record.expected_answer_format,
                record.priority_score,
                record.cluster,
            ),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def save_query_records(self, records: Iterable[QueryRecord]) -> list[int]:
        return [self.save_query_record(record) for record in records]

    def list_query_records(self, *, cluster: str | None = None) -> list[QueryRecord]:
        filters: list[str] = []
        params: list[str] = []
        if cluster is not None:
            filters.append("cluster = ?")
            params.append(cluster)
        return [_row_to_query(row) for row in self._select("SELECT * FROM query_records", filters, params)]

    def save_page_record(self, record: PageInventoryRecord) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO page_inventory (
                url, title, h1, schema_types_json, last_modified, canonical_url, content_chunks_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.url,
                record.title,
                record.h1,
                _dump(record.schema_types),
                record.last_modified,
                record.canonical_url,
                _dump(record.content_chunks),
            ),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def save_page_records(self, records: Iterable[PageInventoryRecord]) -> list[int]:
        return [self.save_page_record(record) for record in records]

    def list_page_records(self, *, canonical_url: str | None = None) -> list[PageInventoryRecord]:
        filters: list[str] = []
        params: list[str] = []
        if canonical_url is not None:
            filters.append("canonical_url = ?")
            params.append(canonical_url)
        return [_row_to_page(row) for row in self._select("SELECT * FROM page_inventory", filters, params)]

    def save_diagnosis(self, diagnosis: FailureDiagnosis) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO failure_diagnoses (failure_types_json, explanation, next_step, evidence_json)
            VALUES (?, ?, ?, ?)
            """,
            (_dump(diagnosis.failure_types), diagnosis.explanation, diagnosis.next_step, _dump(diagnosis.evidence)),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def save_diagnoses(self, diagnoses: Iterable[FailureDiagnosis]) -> list[int]:
        return [self.save_diagnosis(diagnosis) for diagnosis in diagnoses]

    def list_diagnoses(self, *, failure_type: str | None = None) -> list[FailureDiagnosis]:
        diagnoses = [_row_to_diagnosis(row) for row in self._select("SELECT * FROM failure_diagnoses", [], [])]
        if failure_type is not None:
            diagnoses = [diagnosis for diagnosis in diagnoses if failure_type in diagnosis.failure_types]
        return diagnoses

    def save_task(self, task: OptimizationTaskBrief) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO optimization_tasks (
                action_type, target_page, query_cluster, expected_impact, confidence,
                risk, draft_content, retest_plan, failure_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.action_type,
                task.target_page,
                task.query_cluster,
                task.expected_impact,
                task.confidence,
                task.risk,
                task.draft_content,
                task.retest_plan,
                task.failure_type,
            ),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def save_tasks(self, tasks: Iterable[OptimizationTaskBrief]) -> list[int]:
        return [self.save_task(task) for task in tasks]

    def list_tasks(self, *, action_type: str | None = None) -> list[OptimizationTaskBrief]:
        filters: list[str] = []
        params: list[str] = []
        if action_type is not None:
            filters.append("action_type = ?")
            params.append(action_type)
        return [_row_to_task(row) for row in self._select("SELECT * FROM optimization_tasks", filters, params)]

    def save_report_artifact(self, artifact: ReportArtifact) -> int:
        cursor = self._connection.execute(
            "INSERT INTO report_artifacts (name, format, content) VALUES (?, ?, ?)",
            (artifact.name, artifact.format, artifact.content),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def list_report_artifacts(self, *, format: str | None = None) -> list[ReportArtifact]:
        filters: list[str] = []
        params: list[str] = []
        if format is not None:
            filters.append("format = ?")
            params.append(format)
        return [_row_to_report(row) for row in self._select("SELECT * FROM report_artifacts", filters, params)]

    def _select(self, sql: str, filters: list[str], params: list[str]) -> list[sqlite3.Row]:
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY id ASC"
        return list(self._connection.execute(sql, params).fetchall())

    def __enter__(self) -> "EvidenceStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def _dump(values: tuple[str, ...]) -> str:
    return json.dumps(list(values), sort_keys=True)


def _load(value: str) -> tuple[str, ...]:
    return tuple(str(item) for item in json.loads(value))


def _row_to_run(row: sqlite3.Row) -> EngineRun:
    return EngineRun(row["engine"], row["query"], row["timestamp"], row["region"], row["language"], row["raw_answer"], _load(row["citations_json"]), _load(row["mentions_json"]), _load(row["recommendations_json"]), _load(row["source_domains_json"]))


def _row_to_query(row: sqlite3.Row) -> QueryRecord:
    return QueryRecord(row["query"], row["intent_type"], row["funnel_stage"], row["language"], row["region"], row["target_engine"], _load(row["competitor_entities_json"]), row["expected_answer_format"], float(row["priority_score"]), row["cluster"])


def _row_to_page(row: sqlite3.Row) -> PageInventoryRecord:
    return PageInventoryRecord(row["url"], row["title"], row["h1"], _load(row["schema_types_json"]), row["last_modified"], row["canonical_url"], _load(row["content_chunks_json"]))


def _row_to_diagnosis(row: sqlite3.Row) -> FailureDiagnosis:
    return FailureDiagnosis(_load(row["failure_types_json"]), row["explanation"], row["next_step"], _load(row["evidence_json"]))


def _row_to_task(row: sqlite3.Row) -> OptimizationTaskBrief:
    return OptimizationTaskBrief(row["action_type"], row["target_page"], row["query_cluster"], row["expected_impact"], float(row["confidence"]), row["risk"], row["draft_content"], row["retest_plan"], row["failure_type"])


def _row_to_report(row: sqlite3.Row) -> ReportArtifact:
    return ReportArtifact(row["name"], row["format"], row["content"])
