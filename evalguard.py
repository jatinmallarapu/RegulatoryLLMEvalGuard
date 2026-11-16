"""Evaluate normalized LLM claims and spans and fail closed on regressions."""

import argparse
import json
import math
from pathlib import Path
from typing import TypedDict


class Claim(TypedDict):
    text: str
    citations: list[str]


class Span(TypedDict):
    tool: str
    duration_ms: float


def citation_coverage(claims: list[Claim], sources: set[str]) -> float:
    # A claim with any unknown reference cannot be fully checked by a reviewer.
    return (
        sum(bool(row["citations"]) and set(row["citations"]) <= sources for row in claims)
        / len(claims)
        if claims
        else 0.0
    )


def trace_pass(spans: list[Span], expected: list[str], budget_ms: float) -> bool:
    return [span["tool"] for span in spans] == expected and all(
        0 <= span["duration_ms"] <= budget_ms for span in spans
    )


def regressions(
    current: dict[str, float], baseline: dict[str, float], tolerance: dict[str, float]
) -> list[str]:
    failures = []
    if not baseline:
        return ["missing baseline"]
    for metric, reference in sorted(baseline.items()):
        value = current.get(metric)
        allowed = tolerance.get(metric, 0)
        if value is None or not all(map(math.isfinite, (reference, value, allowed))) or allowed < 0:
            failures.append(f"{metric}: invalid or missing evidence")
        elif value < reference - allowed:
            failures.append(f"{metric}: {value:.4f} below minimum {reference - allowed:.4f}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    # Keep fixture baselines and measured evidence inspectable in one local demo.
    data = json.loads(args.config.read_text(encoding="utf-8"))
    metrics = {
        "citation_coverage": citation_coverage(data["claims"], set(data["source_ids"])),
        "trace_pass": float(trace_pass(data["spans"], data["expected_tools"], data["budget_ms"])),
    }
    failures = regressions(metrics, data["baseline"], data["tolerance"])
    print(
        json.dumps(
            {"status": "BLOCK" if failures else "PASS", "metrics": metrics, "failures": failures},
            indent=2,
        )
    )
    raise SystemExit(2 if failures else 0)


if __name__ == "__main__":
    main()
