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

- **Pins.** Implementation name, release, and the exact revision (40-character commit). A hosted service
  that cannot name a commit says so in `served_revision` and is labelled accordingly.
- **Label.** `independently_run` or `author_operated`. A run by the implementation's own operator is never
  labelled independent.
- **Case.** One of `1, 2, 3, 4, 5, 5a, 5b, 6, 7, 8` from the #22 appendix.
- **Start event** for cases 1, 3 and 4: what started the clock, when, and where that time comes from.
- **Decision.** Outcome, reason code, and - for case 3 - the status version, its age at the decision and
  the declared bound. A status that could not be read and a status that aged out must carry **different**
  reason codes.
- **In-flight policy and outcome** where an action was in flight, with a target-side observation or an
  explicit `unknown`.
- **Evidence digest.** SHA-256 of the record bundle the implementation keeps.
- **Residual.** What the design knowingly leaves uncovered; required and non-empty.

## Review

- The maintainer checks shape, completeness and the reason-code rule. The maintainer does not judge
  whether an implementation conforms.
- The maintainer does not check their own implementation's records; a different named participant does,
  or the chairs do, and the pull request states who checked it.
- Disagreement about a check goes to the chairs, not to the maintainer.
