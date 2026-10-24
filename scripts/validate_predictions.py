#!/usr/bin/env python3
"""Validate basic structure of a SWE-bench predictions JSONL file."""
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} predictions.jsonl", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    seen = set()
    errors = []
    count = 0
    empty_patches = 0

    with path.open(encoding="utf-8") as stream:
        for line_no, raw in enumerate(stream, 1):
            if not raw.strip():
                errors.append(f"line {line_no}: blank lines are not valid JSONL records")
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(row, dict):
                errors.append(f"line {line_no}: expected a JSON object")
                continue

            count += 1
            for key in ("instance_id", "model_patch"):
                if key not in row:
                    errors.append(f"line {line_no}: missing required key {key!r}")
            instance_id = row.get("instance_id")
            if isinstance(instance_id, str):
                if instance_id in seen:
                    errors.append(f"line {line_no}: duplicate instance_id {instance_id!r}")
                seen.add(instance_id)
            patch = row.get("model_patch")
            if isinstance(patch, str) and not patch.strip():
                empty_patches += 1

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"INVALID: {len(errors)} issue(s); parsed {count} record(s).", file=sys.stderr)
        return 1

    print(f"Valid JSONL structure: {count} record(s), {len(seen)} unique instance ID(s).")
    if empty_patches:
        print(f"WARNING: {empty_patches} record(s) have empty model_patch values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
