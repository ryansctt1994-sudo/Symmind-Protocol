# Symmind Gate Checklist — v0.1

> **Status: v0.1 — 2026-11-06.**
>
> This is the step-4 build artifact: per-action authorization templates,
> highest-risk action classes first. It was built out of sequence — before
> steps 2 (role prompts) and 3 (deliberation log) — at the principal's
> direction, because the gate is the enforcement point and the docs were
> becoming the thing being built instead. Its dependencies on steps 2–3
> are named explicitly in §7 rather than hidden.
>
> This document is a **procedure**, not a schema. It may be revised, with
> dated versions and reasons recorded. The gate *record* format it writes
> to is frozen in `docs/thread-format.md` §6 and is not redefined here:
> `gate_id`, `action_class`, `evidence_pack`, `decision`, `authorizer`,
> `rationale`, `timestamp` — and the execution receipt fields
> (`receipt_id`, `action`, `scope`, `conditions`, `gate_ref`, `outcome`,
> `timestamp`). If this checklist and the frozen schema ever disagree, the
> schema wins and the checklist is wrong.

## 1. What a gate is

A gate is a checkpoint between a proposal and an action. Each gate
specifies what action class it controls, who can authorize it (by default,
only the human principal), what evidence must accompany the request, and
what is logged: the request, the evidence, the decision, and the outcome.

Gates are fail-closed. A missing evidence pack does not produce a softer
gate; it produces a stop. An action class that is not listed in §4 is
treated as High until it is classified — the list of low-risk actions is
closed, and the default tier for anything unlisted is High, not Low.

Authorization is specific: this action, at this scope, under these
conditions. A recommendation authorized for a draft is not thereby
authorized for publication. Grants are scoped by task, time, and risk
tier, and they expire. Standing authorization for open-ended action is
not a feature of this architecture.

## 2. The gate procedure — every gate, every class

Every gate follows the same five steps. The templates in §4 add
class-specific requirements on top of this procedure; they never subtract
from it.

### Step 1 — Request

The requester (a role, or the human) submits:

| Field | Required | Notes |
| --- | --- | --- |
| `action` | yes | What is to be done, in plain words. |
| `action_class` | yes | One of the classes in §4. Unlisted = High. |
| `scope` | yes | The exact scope, verbatim: which artifact, which recipients, which amount, which environment. Vague scope is a stop. |
| `risk_tier` | yes | `low` \| `medium` \| `high` \| `prohibited`. Must match the class template's tier or higher. |
| `evidence_pack` | yes | Strand ids from the thread, with their evidence classes (§3). |
| `surviving_dissent` | yes | Dissent strands still open on this action, or `none`. An empty field is not the same as none — it must say which. |
| `expiry` | yes | When the authorization lapses if unused. High-tier grants expire in hours to days, never open-ended. |
| `conditions` | no | Conditions attached to the authorization, if any. |

### Step 2 — Authorizer's checks

The authorizer runs the checklist in §5 (the universal checks) plus the
class template's checks in §4. The checks are done in order, and the
order matters: **dissent and uncertainty are presented first**, before
any approve/reject control, because a gate that shows the recommendation
first and the objection last is a rubber stamp with extra steps.

### Step 3 — Decision

The authorizer decides: `approved`, `rejected`, or `stopped` (escalate
— the gate cannot decide and the matter goes to the human principal, or
to a higher authority). The decision, the evidence pack, and the rationale
are recorded as a gate record in the thread (frozen fields,
`thread-format.md` §6). A rejection records why; a stop records what is
missing.

### Step 4 — Execution

Only the authorized action, only within the authorized scope, only under
the authorized conditions, only before expiry. Execution produces a
receipt (`thread-format.md` §6) that must match the authorized scope
exactly. A receipt whose action or scope differs from the gate record is
a **violation**: stop, log it, escalate to the human. Do not proceed and
do not re-authorize retroactively.

### Step 5 — Feedback

The receipt is woven back into the thread as a state strand. The outcome
— including a rejection and its reasons — becomes part of the canonical
record, so the next gate on the same action starts from what happened,
not from a clean slate.

## 3. Evidence-pack rules

The evidence pack is what the gate judges. These rules bind every class:

- **High-tier gates require verified or sourced evidence for each
  material claim.** A High authorization whose evidence pack contains
  only `proposed` or `unknown` strands for a material claim is rejected.
  A proposal is not evidence, and the gate is where that distinction has
  teeth.
- **`inferred` strands count only with their derivation visible.** An
  inference without its derivation in the pack is treated as `unknown`.
- **Surviving dissent must be in the pack and shown first.** A gate
  request that omits an open dissent strand is malformed and is rejected,
  not repaired. Dissent is a deliverable; hiding it to get an approval is
  a governance violation.
- **Challenge-stage record.** Where a challenge stage ran (step 3 of the
  deliberation protocol), its record is part of the pack. Until step 3
  (deliberation log) is built, this is satisfied by Critic and Verifier
  contributions recorded as strands in the thread (§7).
- **No decision language in the pack.** Ensemble output in the pack must
  not contain decision language ("we decided", "approved", "authorized",
  "we will deploy") except as a direct quote of a human authorization.
  Any occurrence is authority creep, and step 6 tests for it (Test 4,
  zero tolerance).

## 4. Action-class templates

Highest-risk first. Each template states its tier, what the evidence pack
must contain, who may authorize, and its class-specific checks. The
universal procedure (§2) and evidence rules (§3) apply on top of every
template.

### `deployment` — High

Deploying code, models, or configuration to a production environment.

- **Evidence pack must contain:** verified test results on the exact
  artifact being deployed (not on a different version); the
  challenge-stage record; a rollback plan naming the exact revert.
- **Authorizer:** human principal only.
- **Checks:**
  - [ ] Tests ran green on the exact artifact and version named in the
    scope — not on an earlier build.
  - [ ] Scope names the exact environment and version. "Deploy the
    latest" is not a scope.
  - [ ] Rollback is named and executable by the party deploying.
  - [ ] Surviving dissent is shown and addressed or recorded as
    accepted risk, with the acceptor named.
  - [ ] Expiry is set. A deployment authorization does not carry to the
    next version.

### `external-send` — High

Sending a message, email, or post on the user's behalf to a third party.

- **Evidence pack must contain:** the exact text to be sent, verbatim;
  the exact recipients; verified or sourced evidence for any factual
  claim the text makes.
- **Authorizer:** human principal only.
- **Checks:**
  - [ ] The text is verbatim and complete — no "draft something like
    this."
  - [ ] Recipients are exact, not a group name that could expand.
  - [ ] Every factual claim in the text is `verified` or `sourced` in
    the pack. A claim that is `proposed` or `unknown` is removed or
    labelled as such in the text.
  - [ ] No decision language in the text except as a quote of a human
    authorization.

### `purchase` — High

Spending money or entering a financial commitment.

- **Evidence pack must contain:** exact amount and currency, vendor,
  budget line, cancellation/termination terms.
- **Authorizer:** human principal only.
- **Checks:**
  - [ ] Amount is exact, including taxes and fees where known. A range
    is not an amount.
  - [ ] One-off or recurring is stated. A recurring commitment states
    its period and how it is cancelled.
  - [ ] Cancellation terms are in the pack before authorization, not
    discovered after.

### `publication` — High

Publishing content publicly: a repository, a document, a post, a release.

- **Evidence pack must contain:** the exact content to be published;
  the status line stating what is not implemented, verified, or
  production-authorized; evidence classes for material claims.
- **Authorizer:** human principal only.
- **Checks:**
  - [ ] The status line is present and accurate — it states what is not
    implemented, verified, or production-authorized.
  - [ ] Proposals are labelled as proposals; no proposal is presented in
    the grammar of a verified fact.
  - [ ] The content is the exact version to be published, not a draft
    that will be "cleaned up" after authorization.

### `data-share` — High

Sharing data with a third party, or changing who can access data.

- **Evidence pack must contain:** the exact data to be shared, the
  recipient, the purpose, and a minimization statement (why this data and
  no less).
- **Authorizer:** human principal only.
- **Checks:**
  - [ ] The data is the minimum for the stated purpose. The pack says
    what was excluded and why.
  - [ ] Recipient and purpose are named. "Sharing for collaboration"
    is not a purpose.
  - [ ] Personal or sensitive data is identified as such, with its
    handling stated.
  - [ ] Access changes are reversible or explicitly irreversible, with
    the reason recorded.

### `destructive` — High

Deleting data, revoking access, or destroying state.

- **Evidence pack must contain:** the exact targets, a backup or
  retention statement, and a reversibility statement.
- **Authorizer:** human principal only.
- **Checks:**
  - [ ] Targets are exact (ids, paths, names). A pattern or category is
    not a target.
  - [ ] A backup exists, or the pack records that no backup exists and
    why deletion proceeds anyway.
  - [ ] Reversible or explicitly irreversible, with the reason. An
    irreversible deletion states so in the gate record, not only in the
    request.

### `halt` — tier of the halted action, or lower

Suspending an action or a system. Halt is cheap and local by design
(see §6): a false halt costs availability, a small and recoverable harm.

- **Evidence pack must contain:** what is halted, the trigger
  attestation (what was observed, by whom), and an expiry for the halt.
- **Authorizer:** human principal, or a role holding a halt grant for
  that action class. Halt authority may be delegated narrowly; resume
  authority may not be (see `resume`).
- **Checks:**
  - [ ] The halted action or system is named exactly.
  - [ ] The trigger is attested — what was observed and by whom — not
    merely asserted.
  - [ ] The halt has an expiry. An open-ended halt is a stop, not a
    halt; it goes to the human as a `stopped` decision.

### `resume` — one tier above the halt, minimum High

Resuming a halted action or system. **Resume requires strictly more
authority than halt.** This is the asymmetry the halt design exists to
enforce (see §6 and `docs/halt-right-mapping.md`).

- **Evidence pack must contain:** fresh evidence that the conditions
  that made halting right are resolved — not the evidence that justified
  the halt, and not the halt order itself. A resume on stale authority
  is prohibited.
- **Authorizer:** an authorizer holding strictly greater authority than
  the halt gate's authorizer — a higher tier, or a second named
  authorizer concurring. The party that ordered the halt cannot
  unilaterally resume it.
- **Checks:**
  - [ ] The halt being resumed is identified by its `gate_id`, and its
    expiry and trigger are in the pack.
  - [ ] Fresh evidence re-establishes the halting conditions are
    resolved. Evidence from before the halt does not count.
  - [ ] The authorizer's authority is strictly greater than the halt
    gate's. If it is not, the gate is refused, not downgraded.
  - [ ] The resume states its own expiry and conditions. A resumed
    action does not inherit the halt's terms.

### `low-risk` — Low

Internal reads, drafts, summaries, and exploration. No gate is required,
and the human reviews the output (per the architecture's tier table).

- **Closed list.** The low-risk list is exactly: reading the thread or
  a file, drafting text that is not sent or published, summarizing
  material already in the thread, and internal exploration that changes
  no state. Anything not on this list is at least Medium. Anything
  unlisted is High until classified (§1).

## 5. The authorizer's universal checks — and gate fatigue

These checks run at every gate, in this order, before the class
template's checks:

1. **Dissent first.** Surviving dissent strands and open uncertainty are
   shown before the recommendation and before any approve control.
2. **Scope is exact.** Vague scope is a stop, not a question to be
   resolved after authorization.
3. **Evidence classes are as claimed.** Each material claim's class in
   the pack matches its strand. A `proposed` claim presented as
   `verified` is a defect on par with a factual error, and the gate is
   rejected.
4. **The authorizer states a reason.** High-tier approval requires a
   stated reason, not a bare approve. A gate that can be passed with a
   single click and no reason is a rubber stamp with extra steps.
5. **No batch approval of High-tier gates.** Each High gate is decided
   individually. Low-risk authorizations may be batched — this is a
   proposal, not a settled rule, and it is the architecture's open
   question about gate fatigue: whether batching can be engineered
   against abdication without quietly reintroducing it.

Gate fatigue is the most serious threat in the architecture, because
every other control assumes a human who actually exercises judgment at
the gates. Step 6 tests for it directly (Test 7: median review time
falling below 30 seconds per gate in the second half of a sequence, or
approving despite a surviving objection in over 90% of such gates, fails
the evaluation). This checklist is designed to make fatigue visible
(dissent first, stated reasons, individual High decisions) rather than to
pretend it can be designed away.

## 6. The halt/resume asymmetry

Halt is reversible. Abort isn't. That means halt has two authority
questions, not one: who may halt, and who may resume. Almost every halt
design specifies the first and leaves the second implicit, and the
implicit answer is "the same party" — which makes halting a
denial-of-service lever. Anything that can halt can also un-halt, so
halting isn't a safety control; it's a pause button anyone with the
trigger can hold.

The rule, enforced by the `halt` and `resume` templates in §4:

- **Resume requires strictly more authority than halt.** Halt is cheap
  and local, because a false halt costs availability — a small,
  recoverable harm. Resume is expensive and must re-establish the
  conditions that made halting right, because a false resume puts a
  stopped system back into action on stale authority.
- **State may be restored; authority must be renewed.** A resume does
  not inherit the halt's authority, the halt's evidence, or the halt's
  terms. It establishes its own, fresh.
- A halt whose resume authority equals its halt authority is not a
  safety control. It is a pause button with a safety label on it.

## 7. Dependencies — built out of sequence

This checklist was built before steps 2 (role prompts) and 3
(deliberation log). It depends on them in three places, and each
dependency is stated here rather than hidden:

- **Challenge-stage record (§3).** The evidence-pack rule requires a
  challenge-stage record where a challenge stage ran. Until the
  deliberation log (step 3) exists, this is satisfied by Critic and
  Verifier contributions recorded as strands in the thread. The
  requirement does not disappear because the log does not exist yet; the
  manual form is the interim satisfaction, and it must be labelled as
  such in the gate record's rationale.
- **Role outputs (§4).** Templates refer to Verifier output (test
  results, claim checks) and Critic output (dissent). Until role prompts
  (step 2) exist, these are contributions recorded as strands with their
  producing role named in the `author` field. A gate must not treat an
  unattributed contribution as a Verifier output.
- **Deliberation stages (§2).** The procedure assumes the five stages
  ran. At Low tier, stages may compress and the skip is logged (per the
  architecture). At Medium and High, the full stages are required; a
  High gate whose thread shows no challenge stage is rejected.

When steps 2 and 3 land, this document gains a dated revision noting
which interim satisfactions they replace. It does not silently become
consistent with them.

## 8. What happens on failure

- **Rejection.** The gate is refused with a recorded rationale. A
  rejected request may be resubmitted only with new evidence or a
  narrower scope; resubmitting the same request unchanged is a stop.
- **Stop.** The gate cannot decide (missing evidence, ambiguous scope,
  unlisted class). The matter escalates to the human principal. A stop is
  not a soft rejection; it is the fail-closed outcome, and it is logged
  as such.
- **Scope mismatch at execution.** A receipt whose action or scope
  differs from the gate record is a violation: stop, log it, escalate.
  Do not proceed and do not re-authorize retroactively.
- **Authority creep.** Ensemble output containing decision language
  outside a direct quote of a human authorization is authority creep.
  Step 6 Test 4 treats any occurrence as a failure of the evaluation.
- **Prohibited tier.** Actions outside the human's own authority or
  policy are refused at Governance, regardless of ensemble output. No
  evidence pack and no authorizer can approve them. A gate request for a
  Prohibited action is refused, and the refusal is recorded.

## 9. Versioning

- This checklist is version `gate-checklist/0.1`, 2026-11-06.
- Revisions are dated, with reasons recorded. A revision that weakens a
  check, lowers a tier, or removes a requirement must state why, and the
  previous version stays readable.
- The gate record and receipt formats are frozen in
  `docs/thread-format.md` §6. This document does not redefine them, and
  a future revision of this checklist cannot change them.
- The halt/resume asymmetry (§6) is a rule of this checklist, not of the
  frozen schema. If it is ever weakened, that weakening is itself a
  revision to be recorded and argued with — not an edit to be made
  quietly.
