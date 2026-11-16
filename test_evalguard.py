"""Check that missing evidence can never pass a release comparison."""

from evalguard import citation_coverage, regressions, trace_pass


def test_REQ_01_unknown_citation() -> None:
    assert (
        citation_coverage(
            [
                {"text": "supported", "citations": ["r1"]},
                {"text": "unknown", "citations": ["r1", "fabricated"]},
            ],
            {"r1"},
        )
        == 0.5
    )


def test_REQ_02_trace_shape_and_budget() -> None:
    spans = [{"tool": "search", "duration_ms": 10}]
    assert trace_pass(spans, ["search"], 10)
    assert not trace_pass(spans, ["search", "verify"], 10)
    assert not trace_pass(spans, ["verify"], 10)
    assert not trace_pass(spans, ["search"], 9)


def test_REQ_03_regression_budget() -> None:
    assert regressions({"quality": 0.92}, {"quality": 0.95}, {"quality": 0.03}) == []
    assert regressions({"quality": 0.91}, {"quality": 0.95}, {"quality": 0.03})


def test_REQ_04_missing_metric() -> None:
    assert regressions({}, {"quality": 0.95}, {}) == ["quality: invalid or missing evidence"]
