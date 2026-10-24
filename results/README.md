# Results artifacts

This directory will contain validated outputs from actual runs.

Expected artifacts:
- `predictions.jsonl`: model-generated patches, one JSON object per attempted task.
- `evaluation.json`: official SWE-bench evaluator report.
- `summary.json`: aggregate counts and run metadata.
- `smoke-test.md`: notes for single-task verification.

Only add files after verifying they contain no credentials or reference patches. Clearly label partial runs and never substitute estimates for measured results. The full 300-task benchmark has not yet run.
