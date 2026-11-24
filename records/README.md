# Submitting a Round 2 record

This directory is a **proposal** for how records could be collected, made in
`aaif/wg-identity-and-trust#32`. It becomes binding only if the group adopts it.

## Shape

One file per implementation per case:

```
records/<implementation-slug>/case-<case>.json
```

The file must validate against `schema/case-record.schema.json` and pass
`schema/validate_records.py`. `scripts/check.sh` runs both.

## What a record must state

- **Pins.** Implementation name, release (a tag, or `hosted` when the service runs the revision
  directly), and the exact revision (40-character commit). A hosted service that cannot name a commit
  says so in `served_revision` and is labelled accordingly.
- **Label.** `independently_run` or `author_operated`. A run by the implementation's own operator is
  never labelled independent.
- **Case.** One of `1, 2, 3, 4, 5, 5a, 5b, 6, 7, 8` from the #22 appendix.
- **Start event** for cases 1, 3 and 4: what started the clock, when, and where that time comes from.
- **Decision.** Outcome and reason code. The reason code is the implementation's own, **verbatim in its
  own case** (`DELEGATION_PROOF_DENIED` and `state_unproven` are both fine): a reader matches it against
  that implementation's published vocabulary, so the format does not normalise it.
- **Status fields, case 3.** `status_observed` says whether the decision rested on a status read.
  When it did, `status_version` (a counter, an epoch and height, or an opaque identifier) and
  `status_age_s` are required, with the `declared_bound_s`. When it did not, `status_age_s` is absent
  and `status_source` says the fields came from nowhere. `status_source` otherwise names the source:
  the decision's own record, or the implementation's public status read by the operator at the time.
- **In-flight policy and outcome** where an action was in flight, with a target-side observation or an
  explicit `unknown`.
- **Evidence.** `record_sha256` digests what the record points at; `scope` says whether that is the
  published bundle or a private record that stays with the implementation. `verify` is optional and
  names a signature scheme, key or offline command, so a signed decision can be checked for origin.
- **Residual.** What the design knowingly leaves uncovered; required and non-empty.

## Review

- The maintainer checks shape, completeness, the reason-code rule and the residual rule. The maintainer
  does not judge whether an implementation conforms.
- The maintainer does not check their own implementation's records; a different named participant does,
  or the chairs do, and the pull request states who checked it.
- Disagreement about a check goes to the chairs, not to the maintainer.
