# Evaluation methodology

## Scope
Evaluate Grok Build-generated patches on the 300 instances in SWE-bench Lite using the official SWE-bench evaluation harness.

## Protocol
1. Use the benchmark's official task descriptions and task environments.
2. Keep reference solution patches and test patches out of the agent's workspace and prompts.
3. Save one prediction record per attempted instance, including `instance_id`, `model_patch`, and `model_name_or_path`.
4. Evaluate generated patches using the official harness and record its full summary.
5. Separate resolved tasks, unresolved tasks, model/tool failures, infrastructure failures, and tasks not attempted.
6. Report the exact denominator. Do not count skipped or failed-to-start tasks as solved.
7. Keep an immutable copy of each run's inputs and evaluator outputs before doing analysis.

## Required run metadata
- SWE-bench dataset and version
- SWE-bench package version
- Model identifier and Grok Build version
- Start/end timestamps and run ID
- Attempted, completed, resolved, unresolved, and infrastructure-failure counts
- Evaluation command and worker count
- Any exclusions or retries, with reasons

## Integrity and privacy
- Never give Grok access to `gold.patch` or `test.patch`.
- Never commit API keys, access tokens, cookies, private credentials, or environment dumps.
- Sanitize logs before publishing; keep raw local logs private if they contain prompts, paths, or sensitive data.
- Publish results only after validating JSON/JSONL and reconciling counts with evaluator reports.
- Label smoke tests separately from the full benchmark.
