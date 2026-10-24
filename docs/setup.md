# Local setup and run checklist

This project documents a local workflow; it does not embed credentials or run the benchmark from GitHub.

## Prerequisites
- Linux host with Docker configured for SWE-bench task images.
- Python environment with a compatible `swebench` package.
- Grok Build installed and configured with the desired model endpoint.
- Access to the official SWE-bench Lite dataset and task repository.

## Before a full run
1. Verify the single-task smoke test and inspect its evaluator report.
2. Validate the predictions file with `python scripts/validate_predictions.py predictions.jsonl`.
3. Confirm reference solution files (`gold.patch`, `test.patch`) are not mounted into or readable by the agent workspace.
4. Confirm sufficient disk space and Docker image availability.
5. Choose a unique run ID and record the model, package version, date, and worker count.
6. Run a small pilot before scaling to all 300 tasks.
7. Evaluate predictions with the official SWE-bench harness.
8. Reconcile the number of prediction rows, attempted tasks, and evaluator results before publishing.

## Example evaluation command
Adapt paths and run ID to the actual machine:

```bash
swebench eval princeton-nlp/SWE-bench_Lite \
  --predictions /path/to/predictions.jsonl \
  --workers 1 \
  --run-id grok-lite-run-001 \
  --task-repo /path/to/swe-bench-tasks
```

Use the exact options supported by the installed SWE-bench version (`swebench eval --help`). The command above is a template, not a benchmark already executed by this repository.
