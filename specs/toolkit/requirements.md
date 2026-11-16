# LLM evidence regression gates

An application team needs a deterministic CI check for missing citations, invalid execution traces, and quality regressions.

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| REQ-01 | Citation coverage | GIVEN claims with citations WHEN scored THEN count a claim only if it cites known evidence. |
| REQ-02 | Trace contract | GIVEN ordered tool spans WHEN scored THEN reject unknown steps, missing calls, and slow spans. |
| REQ-03 | Regression threshold | GIVEN a baseline and tolerance WHEN a metric drops beyond tolerance THEN block. |
| REQ-04 | Incomplete evidence | GIVEN a missing metric WHEN comparing against baseline THEN block. |
