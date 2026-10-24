# Grok Build × SWE-bench Lite

A reproducible workspace for evaluating Grok Build on [SWE-bench Lite](https://www.swebench.com/). The benchmark contains 300 real GitHub issue tasks. This repository records the workflow, verified results, and failure analysis.

> **Status:** Setup in progress. One smoke task, `astropy__astropy-12907`, has been reported as resolved by the official SWE-bench evaluator. The full 300-task run has **not** started; aggregate benchmark results are not available yet.

## Goals

- Run Grok Build against SWE-bench Lite task descriptions without exposing reference solutions.
- Evaluate generated patches with the official SWE-bench harness.
- Preserve predictions, evaluator reports, run metadata, and sanitized failure analysis.
- Report measured outcomes honestly, including infrastructure failures and unresolved tasks.

## Repository layout

- `docs/methodology.md` — evaluation protocol and integrity rules.
- `docs/setup.md` — local setup and run checklist.
- `scripts/validate_predictions.py` — basic JSONL validation for SWE-bench predictions.
- `scripts/run_evaluation.py` — preflight checks and guarded launch of the official evaluator; it does not generate patches.
- `docs/grok-task-prompt.md` — focused prompt template for each Grok Build task.
- `results/README.md` — expected result artifacts and publication rules.
- `analysis/README.md` — summary and failure-analysis conventions.
- `logs/README.md` — safe logging guidance.

Generated predictions and reports will be added after the benchmark is run and validated. Secrets, credentials, raw private logs, and SWE-bench `gold.patch` / `test.patch` files must never be committed.

## Current verified smoke result

| Field | Value |
|---|---|
| Instance | `astropy__astropy-12907` |
| Reported result | Resolved |
| Evaluator | Official SWE-bench evaluator |
| Completed | 1 |
| Resolved | 1 |
| Unresolved | 0 |
| Infrastructure failures | 0 |

This is a **single-task smoke result**, not a claim about performance on all 300 tasks. The patch fixes nested compound-model separability by preserving the right-hand submodel's matrix in Astropy's `_cstack`, with a regression test.

## Prediction format

The validator expects one JSON object per line with at least:
- `instance_id`
- `model_patch`

The standard SWE-bench format also commonly includes `model_name_or_path`. Empty patches are flagged.

## Reproducibility

Record the dataset/version, SWE-bench package version, model identifier, run ID, date, worker count, task image/environment, and exact evaluation command. Do not publish API tokens or credential-bearing environment variables.

## License

SWE-bench and the evaluated projects have their own licenses. This repository's scripts and documentation are provided under the MIT License; see [LICENSE](LICENSE).
