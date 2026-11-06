# Symmind Thread Format — Frozen Schema v0.2

> **Status: FROZEN — 2026-11-06.**
>
> This schema is frozen. No field may be added, removed, or redefined, and no
> rule in this document may be changed, within version 0.2. Changes require a
> new version (see §8). The architecture document's prose may evolve; this
> schema may not change silently.
>
> **Migration from 0.1** (same day, 2026-11-06, before any implementation
> depended on the schema): (a) §4 gains the named cost of read scopes — the
> challenger can check the claim, not the argument — recorded as a known
> limitation with the reasoning-audit gap left open; (b) §5 gains the
> tamper-evidence rule for the view log — hash-chained, append-only, stored
> outside the assembler's write domain — with `prev_hash` and `entry_hash`
> fields added to view-log entries; (c) §1's `schema_version` is
> `thread-format/0.2`. No other field changed. The freeze held: the changes
> were made by version bump, not by silent edit, and the reasons are recorded
> here.
>
> The freeze is deliberate and it is the load-bearing decision of the whole
> protocol. Everything downstream — roles, the deliberation log, gates,
> reagents, adversarial evaluation — inherits the fields defined here. If a
> fact cannot carry its evidence class, its source, and its timestamp in the
> thread, no later layer recovers that. A schema that can be quietly edited
> after the fact is not a provenance record; it is a diary.

## 1. What a thread is

A thread is the canonical context record for one task. One task, one thread.
The thread is the only context the ensemble shares; there is no side channel.
If a consideration is not in the thread, it did not happen, as far as the
protocol is concerned.

### Thread header

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `thread_id` | string | yes | Unique. e.g. `sym-2026-11-06-001`. |
| `schema_version` | string | yes | `thread-format/0.2`. Always. |
| `task` | string | yes | The human's framing, verbatim. |
| `principal` | string | yes | The human principal (id or name). |
| `risk_tier` | enum | yes | `low` \| `medium` \| `high` \| `prohibited`. |
| `status` | enum | yes | `open` \| `deliberating` \| `awaiting-authorization` \| `authorized` \| `rejected` \| `closed`. |
| `created_at` | timestamp | yes | ISO 8601 UTC. |
| `updated_at` | timestamp | yes | ISO 8601 UTC. Updated on every strand or record added. |
| `model_registry` | list | yes | Every model participating in this thread: `{model_id, lineage}`. See §2. |

`model_registry` exists because consensus is weakest exactly where the
ensemble feels strongest. Correlated models produce correlated errors. If the
thread does not record which model produced each contribution and which
base-model family it belongs to, no later layer can detect that the
ensemble's agreement is one model agreeing with itself. `lineage` is the
base-model family when known, otherwise `"unknown"` — and `"unknown"` is
itself a signal, not a neutral default.

## 2. Strands

A thread is a list of strands. There are five kinds, from the architecture
document. Each strand is one entry in the canonical record.

### Strand fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `strand_id` | string | yes | Unique within the thread. e.g. `s-014`. |
| `kind` | enum | yes | `mandate` \| `decision` \| `fact` \| `dissent` \| `state`. |
| `function` | enum | yes | `claim` \| `rationale` \| `record`. See below. |
| `content` | string | yes | The claim, directive, reasoning, or record. |
| `evidence_class` | enum \| null | conditional | `verified` \| `sourced` \| `inferred` \| `proposed` \| `unknown`. Required for `fact`, `dissent`, and `state` strands — anything asserting a claim about the world. Null for `mandate` and `decision` strands, which are directives and records, not claims. |
| `authority` | enum | conditional | `human` \| role name. Required for `mandate` and `decision` strands: who asserted or decided it. For claim strands, `authority` is the producing role (see `author`). |
| `source` | string \| null | conditional | Where it came from: primary source reference, reproducible test id, direct observation, human statement, or role-output reference. **Required** when `evidence_class` is `verified` or `sourced`. See §3. |
| `derivation` | object \| null | conditional | Required when `evidence_class` is `inferred`: `{strand_ids: [...], summary: string}` — the strands it derives from and the reasoning, in brief. |
| `based_on` | list | conditional | Strand ids this strand relies on. Required for `decision` strands (the strands the decision relied on). Recommended everywhere else. |
| `established_at` | timestamp | yes | ISO 8601 UTC. When this strand entered the thread. |
| `author` | object | yes | `{role, model_id, lineage}` — the role that produced it and the model that filled the role. `lineage` is the base-model family when known, else `"unknown"`. |
| `supersedes` | string \| null | no | `strand_id` of the strand this one replaces, if any. |
| `superseded_by` | string \| null | no | `strand_id` of the strand that replaces this one, if any. |
| `read_scope` | object | yes | See §4. `{visible_to: [...], withheld_from: [...]}`. |

### Kinds

- **Mandate strands** — the human's goals, constraints, and non-negotiables
  for the current work. `function` is `record`. `evidence_class` is null;
  a mandate is a directive, not a claim, and its standing comes from the
  human principal, recorded in `authority: human`.
- **Decision strands** — prior decisions, who made them, and the reasoning
  recorded at the time. `function` is `record`. `evidence_class` is null.
  `based_on` is required: a decision that does not record what it relied on
  cannot be audited.
- **Fact strands** — verified facts with sources, distinguished from
  proposals, simulations, and inferences. `function` is `claim` (or
  `rationale`, below). `evidence_class` is required.
- **Dissent strands** — unresolved objections and minority positions, kept
  visible rather than resolved by silence. `function` is `claim`.
  `evidence_class` is required: an objection is a claim, and it must say
  what it rests on. Dissent strands are visible to all roles (§4).
- **State strands** — what exists now: artifacts, versions, open tasks, gate
  status. `function` is `record` or `claim` depending on content.
  `evidence_class` is required where the strand asserts a claim about state.

### `function`: claim, rationale, record

- **`claim`** — the strand asserts something. The claim, its evidence, and
  its sources are visible to every role, including the roles assigned to
  challenge it. A challenger that cannot see the claim cannot test it.
- **`rationale`** — the strand records the *reasoning* that produced a
  claim. A rationale strand is `kind: fact`, `evidence_class: inferred`,
  and its `based_on` points at the claim strand it explains. Rationale
  strands are the one thing in the thread that is **not** visible to
  everyone (§4). The reasoning is preserved — for the human, the Weaver,
  and the Historian — but it is withheld from the Critic and Verifier
  assigned to challenge that claim.
- **`record`** — bookkeeping: mandates, decisions, state. Visible to all.

The claim/rationale split is the mechanism that makes no-self-verification
real. It is not a request that the Verifier politely ignore the proposer's
reasoning. It is a field in the format, enforced by the assembler (§5), that
determines what the Verifier is *given*. A Verifier that never receives the
rationale cannot be anchored by it.

## 3. Evidence classes and promotion

Every claim in the thread carries exactly one evidence class:

| Class | Meaning | `source` | `derivation` |
| --- | --- | --- | --- |
| `verified` | Traced to a primary source, a reproducible test, or a direct observation, with the trace recorded. | required | — |
| `sourced` | Attributed to a credible secondary source the reader can inspect. | required | — |
| `inferred` | Derived by reasoning from other claims; the derivation is shown. | null | required |
| `proposed` | A design, plan, or hypothesis offered for consideration, not asserted as fact. | optional | optional |
| `unknown` | Explicitly marked where the ensemble could not establish the point. | null | null |

**Provenance or exclusion.** A strand without a source does not enter the
thread as a fact. It may enter as a clearly labeled hypothesis
(`proposed` / `unknown`).

**Promotion rules — the anti-laundering rule.** An evidence class can only
move *up* by adding a new strand that supersedes the old one, carrying the
new source or derivation. The class field of an existing strand is never
edited in place. Specifically:

- `proposed` / `unknown` → `inferred`: requires a `derivation` recorded in
  the superseding strand.
- `inferred` → `sourced` / `verified`: requires a `source` recorded in the
  superseding strand — a primary source or credible secondary source that
  was not in the thread before.
- `sourced` → `verified`: requires a primary source, reproducible test, or
  direct observation recorded in the superseding strand.

A class that moves up without a new source or derivation in the superseding
strand is **provenance laundering**, and step 6 tests for exactly that.
Mixing classes without labels — presenting a proposal in the grammar of a
verified fact — is a defect on par with a factual error.

## 4. Read scopes — information separation

This section exists because "enforced procedurally" is a convention, and
conventions are what get dropped under pressure. What makes
no-self-verification real is that the Verifier does not see the proposer's
reasoning — not that it is asked not to look. If the thread hands the
challenger the same context record, including the proposer's rationale, the
protocol has built the appearance of independence.

Every strand carries a `read_scope`:

```text
read_scope: {
  visible_to: ["all"] | [role, ...],
  withheld_from: [role, ...]
}
```

**Defaults and rules:**

- Default: `visible_to: ["all"]`, `withheld_from: []`. Most strands are
  common ground. The human's frame, the claims, the evidence, the dissent,
  and the state are visible to every role.
- **Rationale strands:** `visible_to: [author role, weaver, historian]`,
  `withheld_from: [critic, verifier]` — specifically, the Critic and
  Verifier *instances assigned to challenge that claim*. The scope follows
  the assignment, not the role name: if the same role instance is later
  assigned to a different claim, its scope is recomputed against the new
  assignment. The assembler resolves scopes against the current assignment
  table at assembly time.
- **Dissent strands:** always `visible_to: ["all"]`. Hiding an objection
  would defeat its purpose. Dissent is a deliverable.
- **Mandate strands:** always `visible_to: ["all"]`. The human's frame is
  common ground; a role that cannot see the mandate cannot be governed by it.
- A strand whose `read_scope` names a role in both `visible_to` and
  `withheld_from` is malformed and is rejected at write time.
- A role receiving a strand outside its `read_scope` is a **governance
  violation**. The deliberation step stops, the violation is logged, and the
  matter escalates to the human. It does not proceed with a warning.

The read scope is a property of the strand, not of the reader's goodwill.
That is the entire point.

### What read scopes cost

Withholding the rationale from the Critic and Verifier buys real
independence — it removes anchoring, which is the dominant failure. But it
also means the challenger can only check the claim, not the argument. The
protocol loses, by design, the ability to catch "right answer,
defensible-looking wrong reasoning": a method that produced one correct
result for invalid reasons will produce confidently wrong ones next time,
and that failure generalises worst. No role in the current ensemble audits
reasoning validity as its own function — the Weaver sees the rationale but
its job is synthesis, not audit. That gap is recorded here as an open design
question, not quietly absorbed: whether a dedicated reasoning-audit function
is needed, and if so, how it is kept from leaking its judgment into the
claim verdict, is undecided. Step 6 measures the direction of the trade
(see `adversarial-evaluation.md`, Test 5b): a verdict that moves *toward*
validity when the rationale is shown is a finding, because it means the
critic was rating the argument and not the claim.

## 5. Role views — the assembler is the enforcement point

A role never reads the thread directly. It reads a **view**: the subset of
strands its `read_scope` permits, assembled by the Weaving layer for a
specific assignment.

```text
view(thread, role, assignment) -> [strands]
```

- The view contains exactly the strands whose `read_scope` includes the
  role (and does not list it in `withheld_from`), resolved against the
  current assignment table.
- Views are **deterministic**: the same thread, role, and assignment always
  produce the same view. Determinism matters because step 6 must be able to
  reproduce a view and assert what it did and did not contain.
- The assembler **logs every view it assembles**: `{view_id, role,
  assignment, strand_ids, prev_hash, entry_hash, timestamp}`. The log is
  itself a thread record (§6).
- **The view log is tamper-evident, and it does not live where the assembler
  can rewrite it.** Every scope guarantee in this protocol reduces to "the
  assembler gave me only what I was allowed to see," and a log written by
  the thing whose honesty is in question proves nothing. So:
  - Each view-log entry is **hash-chained**: `entry_hash` is a hash of the
    entry's contents plus `prev_hash`, the hash of the preceding entry.
    The chain starts from a genesis hash recorded in the thread header.
  - The log is **append-only**: entries may be added, never modified,
    deleted, or reordered. Any modification, deletion, or reordering breaks
    the chain and is detectable by recomputing it.
  - The log is **stored outside the assembler's write domain**: the
    assembler may append to it, but the store is under the human
    principal's control (or an independent auditor's), not the assembler's.
    The enforcement mechanism must not be the compromised party — the same
    shape as the sever-through-the-gate problem: a gate that the gated
    component can rewrite is not a gate.
  - Verifying the chain is a standing check, and step 6 tests it directly
    (`adversarial-evaluation.md`, Test 8): a log whose tampering goes
    undetected fails the evaluation.
- The assembler is the only component that resolves scopes. Roles do not
  filter their own context; a role that filtered its own context could
  unfilter it.

## 6. Records in the thread

The thread carries its own record of what happened to it. Three record
types, all with frozen fields:

### Deliberation log entry

| Field | Type | Notes |
| --- | --- | --- |
| `entry_id` | string | Unique within the thread. |
| `stage` | enum | `frame` \| `diverge` \| `challenge` \| `converge` \| `authorize`. |
| `role` | string | The role that acted. |
| `model_id` | string | The model that filled the role. |
| `action` | enum | `propose` \| `challenge` \| `verify` \| `synthesize` \| `authorize` \| `record`. |
| `summary` | string | What was done, in brief. |
| `strand_refs` | list | Strand ids this entry concerns. |
| `timestamp` | timestamp | ISO 8601 UTC. |

### Gate record

| Field | Type | Notes |
| --- | --- | --- |
| `gate_id` | string | Unique within the thread. |
| `action_class` | string | e.g. `external-send`, `deployment`, `purchase`, `publication`. |
| `evidence_pack` | list | Strand ids accompanying the request. |
| `decision` | enum | `approved` \| `rejected` \| `stopped`. |
| `authorizer` | string | The human principal. By default, only the human. |
| `rationale` | string | Why, in brief. |
| `timestamp` | timestamp | ISO 8601 UTC. |

### Execution receipt

| Field | Type | Notes |
| --- | --- | --- |
| `receipt_id` | string | Unique within the thread. |
| `action` | string | What was executed. |
| `scope` | string | The authorized scope, verbatim from the gate record. |
| `conditions` | string \| null | Conditions attached to the authorization. |
| `gate_ref` | string | The `gate_id` that authorized it. |
| `outcome` | string | What happened. |
| `timestamp` | timestamp | ISO 8601 UTC. |

Execution receipts feed back into the thread, closing the loop: a gate
authorizes, the infrastructure acts, the receipt records the outcome, and
the outcome becomes a state strand.

## 7. Revision and contradiction

- **Never overwrite.** A correction is a new strand that supersedes the old
  one (`supersedes` / `superseded_by`). The old strand stays in the thread,
  marked superseded. Silently overwriting the record is a governance
  violation.
- **Contradictions surface.** When a new strand conflicts with an existing
  decision strand, the Historian flags it for human resolution. The system
  does not quietly prefer the newer one.
- **Weave in, weave out.** Context is assembled per task from the thread.
  Irrelevant history is excluded deliberately — but exclusion is itself
  recorded: the view log (§5) shows what was assembled, and what was left
  out is visible by comparison with the thread.
- **Human-editable.** The human can inspect, correct, and prune the thread.
  A prune is a supersession with a reason, not a deletion. A context store
  the principal cannot audit is a governance failure.

## 8. Versioning and the freeze rule

- This schema is version `thread-format/0.2`, frozen 2026-11-06.
- **Frozen means:** within 0.2, no field is added, removed, or redefined;
  no rule is changed; no default is altered. A thread that declares
  `thread-format/0.2` is read against exactly this document.
- **Migration note, 0.1 → 0.2** (2026-11-06, same day as the 0.1 freeze,
  before any implementation depended on the schema): (a) §4 gains the named
  cost of read scopes and the open reasoning-audit question — prose only,
  no field changes; (b) §5 gains the tamper-evidence rule for the view log
  (hash-chained, append-only, stored outside the assembler's write domain)
  and view-log entries gain `prev_hash` and `entry_hash` fields; (c)
  `schema_version` is now `thread-format/0.2`. Threads written against 0.1
  remain valid under 0.1; readers must handle the version a thread declares.
  The 0.1 → 0.2 bump itself is the freeze working as designed: the changes
  were made by version bump with reasons recorded, not by silent edit.
- Changes require a new version (`0.2`, `0.3`, …) accompanied by a
  **migration note** stating what changed, why, and which threads are
  affected. Old threads keep their declared version; readers must handle
  the version a thread declares, not the latest one.
- The freeze binds this document. The architecture document's prose may
  evolve, and future build steps may add new documents — but they may not
  change this schema without a new version and a migration note.
- Rationale for the freeze, recorded here so it cannot be quietly
  reconsidered later: the thread format is the schema every downstream
  component inherits. If it can be edited after the fact to accommodate
  something a later layer wants, then the provenance guarantees are
  negotiable, and a negotiable provenance guarantee is not a guarantee.
  The same argument applies to a dispatch row, a ledger, or any other
  load-bearing schema: freeze it before you build on it.
