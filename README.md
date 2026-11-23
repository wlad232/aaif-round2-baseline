# AAIF I&T Round 2 — baseline replay and mapping (Alakris / Radiolaria)

Contribution to `aaif/wg-identity-and-trust#13`, in the shape the Round 2 terms ask for
(draft 0.2, 22 November 2026): a published baseline, mapped before the round is agreed, with the
cases it can and cannot supply.

Everything here is **author-operated**. The operator reviewed the pinned revision and ran the replay;
this is not an independent measurement, and it is not a conformance claim.

## Provenance

- Implementation: **Radiolaria OS**, release `radiolaria-os-reference-g6b6f-v01`
- Revision: `800f38c3407b3f4ec93dc943c977ffeecb614881`
- Source: <https://gitlab.com/radiolaria/radiolaria-os> (public)
- Operator: Vlad Kostitsyn / Alakris — source and test review of the pinned revision, replay runner
- Run date: 2026-11-23T14:33:03Z
- Environment: macOS 27.2.1 (Build 26B131), arm64, Apple M4, Python 3.14.7

## What was run

```bash
python3 -m venv .venv && .venv/bin/python -m pip install -e . && .venv/bin/python -m pip check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m demo.run_action_commit_packet_lifecycle_g2_a_v01
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m demo.run_action_packet_portability_v01
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m demo.run_audit_hash_chain
```

| Command | Exit | Bytes | SHA-256 of output |
|---|---|---|---|
| `.venv/bin/python -m demo.run_action_commit_packet_lifecycle_g2_a_v01` | 0 | 14644 | `8bbb8203a9bb7819c3370d95ac68c9bddd6a1f48036caa850f47bcdc19c6e4f2` |
| `.venv/bin/python -m demo.run_action_packet_portability_v01` | 0 | 2904644 | `8f387991ab1b2abdb9bac212d6491b2eee65fbe95240822bf5f5f969958a5647` |
| `.venv/bin/python -m demo.run_audit_hash_chain` | 0 | 9480 | `b97bd760d19dc3a35fbcb3911935d937fe70eeb2ee64bb90f7b21dd57602e102` |

`run/manifest.json` carries the same digests, the environment and the counts the kernel itself reports
(zero real-world effects, zero network calls, zero provider calls, immutable history proven).

The full deterministic gauntlet (`demo.run_kernel_conformance_v01`) was attempted and aborted after about
28 minutes: CPU-bound on this host with no incremental output. It is recorded as an incomplete attempt in
the manifest, not as a pass.

## Contents

- `mapping.md` — the ten appendix cases (1-8, 5a, 5b) mapped to the baseline: what it supplies, the file
  path that shows it, what it does not supply, and the residual.
- `run/` — replay outputs and the manifest with their digests.
- `schema/` — a proposed machine-readable record shape for Round 2 (`case-record.schema.json`), a
  dependency-free validator, and two illustrative examples. The examples are shapes, not measurements.

## What this does not claim

- No conformance to the AAIF Reference Architecture, no certification, no production readiness.
- No independent measurement: the operator reviewed the release, so every result is labelled
  `author_operated`.
- No real-world effect, network call or provider call occurred in any run here.
