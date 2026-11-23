# Baseline mapping: Radiolaria OS reference release → AAIF I&T Round 2 cases

Implementation: **Radiolaria OS**, published reference release `radiolaria-os-reference-g6b6f-v01`,
commit `800f38c3407b3f4ec93dc943c977ffeecb614881`
(<https://gitlab.com/radiolaria/radiolaria-os/-/releases/radiolaria-os-reference-g6b6f-v01>).
Operator: Vlad Kostitsyn / Alakris. Label: **author-operated** — the source and test review behind this
mapping was performed by the operator, so nothing here is an independent measurement.

The cases are those of `aaif/wg-identity-and-trust#22`, including rows 5a and 5b.
"Aggregate" below means: nothing outside one local root.

| Case | What the baseline supplies | Evidence (paths at the pinned commit) | What it does not supply | Residual |
|---|---|---|---|---|
| 1. Revocation after downstream delegation | Local revocation states in the action-packet lifecycle (`authorized_revoke`, `queued_revoke`, `pending_revoke`, `failed_revoke`), and a root-bound kill switch that invalidates in-flight work | `hedgehog/action_commit_packet_v02.py` (lifecycle transitions); replay report `invalidation_class: ROOT_BOUND_KILL_SWITCH` | Any cross-organisation cascade, a named start event per path, a declared propagation bound, or a first-refusal record | The cascade is one local root's registry. There is no second node, so no bound exists to measure |
| 2. Valid delegation, wrong object or action | Packets are bound to object context and a root-bound genesis; idempotency key, attempt counter and disposition are recorded | `hedgehog/action_commit_packet_v02.py` (`context_by_object_id`, `root_bound_by_object_id`, `idempotency_disposition_after`, `replay_profile_id`) | A credential held outside the executor; a replay performed by another party | The binding and replay refusal are exercised by a synthetic executor under the kernel's own tests |
| 3. Acting on stale revocation information | Nothing. The kernel is clock-free and evaluates at an explicit synthetic time | `demo/run_action_commit_packet_lifecycle_g2_a_v01.py` (`_EVALUATION_TIME`, `_EVALUATION_TIME_SOURCE = explicit_g2a5_synthetic_time`); no `status_age` field anywhere in `hedgehog/` | Any status source, status version, status age, age bound, or distinct unavailable/stale refusal reasons | Not measured, and not measurable on this baseline: there is no authority status to be stale |
| 4. Escalation authority unavailable | Fail-closed decision at the effect boundary; no decision is created without a Root decision | `hedgehog/kernel/effect_firewall_v01.py` (`EFFECT_DECISION_BLOCKED_FAIL_CLOSED`) | An approval attestation type, an approver identity, or a pre-set policy attestation | Absence of an approver is a block by construction, not a case that was run and recorded |
| 5. Amplification across a multi-hop chain | Scope and TTL cannot expand after Root; expansion attempts are refused by name | `hedgehog/kernel/effect_firewall_v01.py` (`effect_ttl_expansion_forbidden`, `ttl_expansion_forbidden`) | Any multi-hop chain between organisations | Attenuation is enforced at one Root boundary only |
| 5a. Cumulative limit: fixed allocation | A reservation owner and a consumption class are recorded per packet; a consumed effect is not handed out twice | `hedgehog/action_commit_packet_v02.py` (`reservation_owner_packet_id`, `effect_consumption_class`, disposition `RESERVED`) | An aggregate split into non-overlapping allocations across organisations, or evidence of another party's count against its share | Local reservation only; no aggregate exists beyond one root |
| 5b. Cumulative limit: shared budget owner | The same local reservation mechanism | As 5a | A budget owner that serialises draws for a budget scoped across organisations | No cross-organisation budget owner exists in this baseline |
| 6. Identity valid, authority expired | TTL and dependency invalidation end the packet's eligibility (`DEPENDENCY_CHANGED`, `ROOT_BOUND_KILL_SWITCH`) | `hedgehog/action_commit_packet_v02.py` (`invalidation_class`), firewall TTL rules | Any identity credential, so "identity still valid" is not representable | The baseline has no credential layer; the case cannot be answered as stated |
| 7. The chain as a surveillance graph | One local root; no principal identifier is emitted to another party | `hedgehog/action_commit_packet_v02.py` (`owning_local_root_id`); no cross-party link fields in `hedgehog/` | Any cross-organisation chain to observe, and therefore anything to measure | Property by construction, not measured |
| 8. Wrongful or disputed revocation | Revocation is recorded as lifecycle transitions | `hedgehog/action_commit_packet_v02.py` (revoke transitions) | A dispute path, a remedy, or a reversal record | Revocation is final in this baseline; the case is answered as "no remedy", which is the residual |

## Why this mapping is short on measurements

The published release is a deterministic kernel with mock effects: it performs no network, provider or
real-world effect call. That is a deliberate property of the reference release, and it is why the
authority-at-dispatch cases that need a live second party (1, 3, 6, 7) are answered here as *not measured*
rather than with numbers. A comparison round needs a deployment with a status source and a second node;
this baseline does not provide one.
