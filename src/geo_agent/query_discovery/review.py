"""Review operations for discovered query spaces."""

from __future__ import annotations

from dataclasses import replace

from .ranker import RankedQuery, rank_queries


def delete_query(queries: tuple[RankedQuery, ...], query_text: str) -> tuple[RankedQuery, ...]:
    remaining = tuple(query.discovered_query for query in queries if query.discovered_query.query.query != query_text)
    return rank_queries(remaining)


def add_query(queries: tuple[RankedQuery, ...], query: RankedQuery) -> tuple[RankedQuery, ...]:
    return rank_queries(tuple(item.discovered_query for item in queries) + (query.discovered_query,))


def reprioritize_query(queries: tuple[RankedQuery, ...], query_text: str, priority_score: float) -> tuple[RankedQuery, ...]:
    updated = []
    for item in queries:
        discovered = item.discovered_query
        if discovered.query.query == query_text:
            record = replace(discovered.query, priority_score=round(max(0.0, min(priority_score, 1.0)), 3))
            discovered = replace(discovered, query=record, priority_score=record.priority_score)
        updated.append(discovered)
    return rank_queries(tuple(updated))
