# Local setup and run checklist

This repository contains benchmark documentation and evaluation helpers. It does not embed credentials, and GitHub cannot run the Grok Build agent against your local Docker task images.

## Prerequisites
- Linux host with Docker configured for SWE-bench task images.
- Python environment with a compatible `swebench` package.
- Grok Build installed and configured with the desired model endpoint.
- Official SWE-bench Lite task dataset and task repository.
- Enough disk space for Docker images, workspaces, logs, and evaluation outputs.

## Important separation
1. **Generation:** Grok Build works on each task and produces one prediction record per instance in standard SWE-bench JSONL format.
2. **Evaluation:** the official SWE-bench evaluator tests those patches. The included `scripts/run_evaluation.py` handles preflight checks and launches evaluation, but does not generate patches or operate Grok Build.

Do not give the agent access to benchmark `gold.patch` or `test.patch` files.

## Pilot first
1. Re-check the already resolved Astropy smoke task and its evaluator report.
2. Use `docs/grok-task-prompt.md` as the task prompt template.
3. Run a small pilot before generating all 300 predictions.
4. Keep one JSON object per line with `instance_id`, `model_patch`, and preferably `model_name_or_path`.
5. Confirm no duplicate IDs, no accidental reference patches, and no credentials in the artifacts.

## Validate predictions

```bash
python scripts/validate_predictions.py predictions.jsonl
```

The validator checks JSONL syntax, required keys, and duplicate instance IDs. It does not prove patch correctness.

## Run evaluation

```bash
python scripts/run_evaluation.py \
  --predictions /absolute/path/to/predictions.jsonl \
  --task-repo /absolute/path/to/swe-bench-tasks \
  --run-id grok-lite-run-001 \
  --workers 1
```

By default the runner expects 300 unique predictions. For a deliberately partial pilot only, add `--expected-count N --allow-partial`. It writes run metadata under `results/runs/` and invokes the official SWE-bench evaluator.

If the installed version differs, check `swebench eval --help` and update the runner only after confirming the supported options.

## Before publishing results
- Compare prediction count, attempted task count, and evaluator report counts.
- Separate resolved, unresolved, and infrastructure-failed tasks.
- Preserve raw logs locally; publish only sanitized summaries.
- Never commit API keys, cookies, environment dumps, `gold.patch`, or `test.patch`.
- Update the README only with actual measured results and the exact denominator.
