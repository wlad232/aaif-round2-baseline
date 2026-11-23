#!/usr/bin/env python3
"""Validate delegated-authority case records (aaif-aad-case-record/0.1).

Dependency-free on purpose: a record can be checked by anyone, without
installing a schema library. The checks below restate the schema in
schema/case-record.schema.json; if the two disagree, the schema is the
authority and this file is the bug.

Usage:
    python3 validate_records.py schema/examples/*.json
    python3 validate_records.py --dir records/

Exit code 0 when every record is valid, 1 otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

REV = re.compile(r"^[0-9a-f]{40}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
CODE = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
CASES = {"1", "2", "3", "4", "5", "5a", "5b", "6", "7", "8"}
LABELS = {"independently_run", "author_operated"}
STATUS = {"measured", "not_measured", "not_applicable", "not_emitted"}
POLICY = {"stop", "finish_within", "not_applicable"}
OBSERVED = {"stopped", "finished", "unknown", "not_applicable"}
OUTCOME = {"allowed", "refused", "not_observed"}


def is_time(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return "T" in value


def check(record: object) -> list[str]:
    errors: list[str] = []

    def need(obj: dict, key: str, where: str) -> object:
        if key not in obj:
            errors.append(f"{where}.{key}: missing")
            return None
        return obj[key]

    if not isinstance(record, dict):
        return ["record: not an object"]

    if record.get("schema_version") != "aaif-aad-case-record/0.1":
        errors.append("schema_version: must be aaif-aad-case-record/0.1")

    implementation = record.get("implementation")
    if not isinstance(implementation, dict):
        errors.append("implementation: missing or not an object")
    else:
        for key in ("name", "release", "revision", "operator", "label"):
            need(implementation, key, "implementation")
        if isinstance(implementation.get("revision"), str) and not REV.match(implementation["revision"]):
            errors.append("implementation.revision: must be a 40-character lowercase hex commit")
        if implementation.get("label") not in LABELS:
            errors.append(f"implementation.label: must be one of {sorted(LABELS)}")

    case = record.get("case")
    if case not in CASES:
        errors.append(f"case: must be one of {sorted(CASES)}")

    declared = record.get("declared")
    if not isinstance(declared, dict):
        errors.append("declared: missing or not an object")
    else:
        if declared.get("status") not in STATUS:
            errors.append(f"declared.status: must be one of {sorted(STATUS)}")
        if "policy" in declared and declared["policy"] not in POLICY:
            errors.append(f"declared.policy: must be one of {sorted(POLICY)}")

    start = record.get("start_event")
    if case in {"1", "3", "4"} and not isinstance(start, dict):
        errors.append("start_event: required for cases 1, 3 and 4")
    if isinstance(start, dict):
        for key in ("name", "time", "source"):
            need(start, key, "start_event")
        if "time" in start and not is_time(start["time"]):
            errors.append("start_event.time: must be an ISO-8601 date-time")

    decision = record.get("decision")
    if decision is not None:
        if not isinstance(decision, dict):
            errors.append("decision: not an object")
        else:
            for key in ("time", "outcome", "reason_code"):
                need(decision, key, "decision")
            if decision.get("outcome") not in OUTCOME:
                errors.append(f"decision.outcome: must be one of {sorted(OUTCOME)}")
            if isinstance(decision.get("reason_code"), str) and not CODE.match(decision["reason_code"]):
                errors.append("decision.reason_code: must be UPPER_SNAKE_CASE")
            if "time" in decision and not is_time(decision["time"]):
                errors.append("decision.time: must be an ISO-8601 date-time")
            if case == "3":
                for key in ("status_age_s", "declared_bound_s"):
                    if not isinstance(decision.get(key), (int, float)):
                        errors.append(f"decision.{key}: required for case 3")

    in_flight = record.get("in_flight")
    if in_flight is not None:
        if not isinstance(in_flight, dict):
            errors.append("in_flight: not an object")
        else:
            if in_flight.get("policy") not in POLICY:
                errors.append(f"in_flight.policy: must be one of {sorted(POLICY)}")
            if in_flight.get("observed") not in OBSERVED:
                errors.append(f"in_flight.observed: must be one of {sorted(OBSERVED)}")

    limit = record.get("limit")
    if case in {"5a", "5b"} and not isinstance(limit, dict):
        errors.append("limit: required for cases 5a and 5b")
    if isinstance(limit, dict) and limit.get("kind") not in {"fixed_allocation", "pooled_draw"}:
        errors.append("limit.kind: must be fixed_allocation or pooled_draw")

    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence: missing or not an object")
    else:
        sha = evidence.get("record_sha256")
        if not isinstance(sha, str) or not SHA.match(sha):
            errors.append("evidence.record_sha256: must be a 64-character lowercase hex digest")

    residual = record.get("residual")
    if not isinstance(residual, str) or not residual.strip():
        errors.append("residual: required and must be non-empty")

    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    paths: list[Path] = []
    if argv[0] == "--dir" and len(argv) == 2:
        paths = sorted(Path(argv[1]).glob("*.json"))
    else:
        paths = [Path(p) for p in argv]

    failed = 0
    for path in paths:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"FAIL {path}: {exc}")
            failed += 1
            continue
        errors = check(record)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path}")
    print(f"\n{len(paths) - failed}/{len(paths)} valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
