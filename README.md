# RegulatoryLLMEvalGuard

[![CI](https://github.com/jatinmallarapu/RegulatoryLLMEvalGuard/actions/workflows/ci.yml/badge.svg)](https://github.com/jatinmallarapu/RegulatoryLLMEvalGuard/actions/workflows/ci.yml)

Turn citation coverage, tool trace validation, and baseline regression checks into a deterministic CI gate.

## Architecture

```text
Claims and tool spans → metrics → baseline comparison → PASS or BLOCK
```

## Verification

| Scope | What the tests cover |
| --- | --- |
| Local acceptance tests | Citation coverage, tool trace checks, regression tolerance, and missing metric blocking |
| Synthetic release fixture | Passes with one fully cited claim and two tools in the expected order |
| Production benchmark | Pending |

The fixture starts with one known citation and two ordered tool spans. Change the citation to an unknown source ID and rerun to reproduce a blocked gate. The test suite also exercises missing metrics and out-of-order or slow tool calls.

## Quickstart

Python 3.11 or newer.

```sh
python evalguard.py examples/evalguard.json
python -m pip install -e '.[dev]'
make test
```

## Design and data

The fixture contains original synthetic claims and tool timings. Fixture timings exercise thresholds and are not measured latency.

[Requirements](specs/toolkit/requirements.md) · [Design](specs/toolkit/design.md) · [Tasks](specs/toolkit/tasks.md)

[Architecture decision](docs/adr/0001-local-baseline.md)

## Remaining milestones

DeepEval, OpenTelemetry and MLflow ingestion, red-team suites, provider guardrails, reusable Action, and PyPI publication.
