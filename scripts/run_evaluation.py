#!/usr/bin/env python3
"""Preflight and run official SWE-bench Lite evaluation on a predictions JSONL.

This script evaluates existing model predictions; it does not invoke Grok Build
or generate patches. It writes a small run-metadata JSON beside the requested
run ID and leaves the official evaluator responsible for scoring.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--task-repo", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--expected-count", type=int, default=300)
    parser.add_argument("--dataset", default="princeton-nlp/SWE-bench_Lite")
    parser.add_argument("--output-dir", type=Path, default=Path("results/runs"))
    parser.add_argument("--allow-partial", action="store_true",
                        help="Allow fewer than expected unique instances (not recommended for final run).")
    return parser.parse_args()


def read_predictions(path: Path) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    errors: list[str] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as stream:
        for line_no, raw in enumerate(stream, 1):
            if not raw.strip():
                errors.append(f"line {line_no}: blank line")
                continue
            try:
                item = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON ({exc.msg})")
                continue
            if not isinstance(item, dict):
                errors.append(f"line {line_no}: record must be a JSON object")
                continue
            missing = [k for k in ("instance_id", "model_patch") if k not in item]
            if missing:
                errors.append(f"line {line_no}: missing {', '.join(missing)}")
                continue
            instance_id = item["instance_id"]
            if not isinstance(instance_id, str) or not instance_id.strip():
                errors.append(f"line {line_no}: instance_id must be a non-empty string")
                continue
            if instance_id in seen:
                errors.append(f"line {line_no}: duplicate instance_id {instance_id}")
                continue
            seen.add(instance_id)
            if not isinstance(item["model_patch"], str):
                errors.append(f"line {line_no}: model_patch must be a string")
                continue
            rows.append(item)
    return rows, errors


def main() -> int:
    args = parse_args()
    if args.workers < 1:
        print("ERROR: --workers must be at least 1", file=sys.stderr)
        return 2
    if not args.predictions.is_file():
        print(f"ERROR: predictions file not found: {args.predictions}", file=sys.stderr)
        return 2
    if not args.task_repo.is_dir():
        print(f"ERROR: task repository directory not found: {args.task_repo}", file=sys.stderr)
        return 2
    if not args.run_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in args.run_id):
        print("ERROR: --run-id may contain only letters, numbers, dot, underscore, and hyphen", file=sys.stderr)
        return 2

    rows, errors = read_predictions(args.predictions)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"ERROR: {len(errors)} prediction file issue(s); evaluation not started.", file=sys.stderr)
        return 2
    count = len(rows)
    if count != args.expected_count and not (args.allow_partial and count < args.expected_count):
        print(f"ERROR: found {count} unique predictions; expected {args.expected_count}.", file=sys.stderr)
        print("Use --allow-partial only for an explicitly partial/pilot run.", file=sys.stderr)
        return 2
    if count == 0:
        print("ERROR: no predictions found.", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = args.output_dir / f"{args.run_id}.metadata.json"
    if metadata_path.exists():
        print(f"ERROR: refusing to overwrite existing metadata: {metadata_path}", file=sys.stderr)
        return 2

    command = [
        "swebench", "eval", args.dataset,
        "--predictions", str(args.predictions.resolve()),
        "--workers", str(args.workers),
        "--run-id", args.run_id,
        "--task-repo", str(args.task_repo.resolve()),
    ]
    metadata = {
        "run_id": args.run_id,
        "dataset": args.dataset,
        "expected_count": args.expected_count,
        "prediction_count": count,
        "workers": args.workers,
        "predictions_path": str(args.predictions.resolve()),
        "task_repo_path": str(args.task_repo.resolve()),
        "command": command,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "started",
        "exit_code": None,
        "note": "Evaluation of existing predictions only; this script does not generate model patches.",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Preflight passed: {count} unique prediction(s).")
    print(f"Run metadata: {metadata_path}")
    print("Starting official SWE-bench evaluation...")

    try:
        result = subprocess.run(command, check=False)
        code = result.returncode
    except FileNotFoundError:
        code = 127
        print("ERROR: 'swebench' executable not found on PATH. Activate the SWE-bench environment.", file=sys.stderr)

    metadata["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    metadata["exit_code"] = code
    metadata["status"] = "completed" if code == 0 else "failed"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
