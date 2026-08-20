"""Benchmark helpers for DSPy program evaluation (accuracy, cost, latency)."""

from __future__ import annotations

import time
from typing import Literal

import dspy
import pandas as pd


def _lm_cost_usd(lm: dspy.LM, start_index: int) -> float:
    """Sum LiteLLM-reported costs for calls made after start_index."""
    history = lm.history[start_index:]
    return sum(entry["cost"] for entry in history if entry.get("cost") is not None)


def benchmark_program(
    program,
    devset,
    metric,
    *,
    phase: str,
    mode: Literal["inference", "train"],
    lm: dspy.LM,
    num_threads: int = 24,
    history_start: int | None = None,
    wall_seconds: float | None = None,
    accuracy: float | None = None,
) -> dict:
    """Collect workload-adjusted metrics for one phase of the pipeline.

    For ``mode="inference"``, runs ``dspy.Evaluate`` on ``devset`` and records
    accuracy, cost, and latency per query.

    For ``mode="train"``, pass pre-measured ``wall_seconds`` and ``history_start``
    from before/after an optimizer ``compile`` call (accuracy is not applicable).
    """
    n = len(devset)
    start = history_start if history_start is not None else len(lm.history)

    if mode == "inference":
        t0 = time.perf_counter()
        evaluator = dspy.Evaluate(
            devset=devset,
            metric=metric,
            num_threads=num_threads,
            display_progress=True,
            display_table=2,
        )
        result = evaluator(program)
        elapsed = time.perf_counter() - t0
        accuracy = float(result.score)
    else:
        elapsed = wall_seconds if wall_seconds is not None else 0.0

    cost_total = _lm_cost_usd(lm, start)

    return {
        "phase": phase,
        "mode": mode,
        "n_queries": n if mode == "inference" else None,
        "accuracy_pct": accuracy,
        "cost_total_usd": cost_total,
        "cost_per_query_usd": cost_total / n if mode == "inference" and n else None,
        "latency_sec_per_query": elapsed / n if mode == "inference" and n else None,
        "wall_seconds": elapsed,
    }


def results_to_frame(rows: list[dict]) -> pd.DataFrame:
    """Build a cumulative results table across phases."""
    return pd.DataFrame(rows)
