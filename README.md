# Symmind Protocol

A human-guided framework for coordinating multiple AI systems through
contextual continuity, differentiated cognitive roles, and ethical oversight.

> **Status:** Conceptual design. This repository describes an intended
> architecture and governance model. It does not claim that any component
> described here is implemented, verified, or production-authorized. Where a
> mechanism is proposed rather than demonstrated, it is labeled as a proposal.

## Thesis

**Capability is not authorization.**

An ensemble that can act does not thereby earn the right to act. Authority
remains with the human principal, is delegated explicitly and narrowly, and
can be revoked at any gate.

Symmind exists to solve a legitimacy problem, not just an efficiency problem.
Multiple AI systems can generate answers faster, from more angles, and with
broader coverage — but neither speed nor coverage answers who is authorized
to decide, on what evidence, and with what accountability if the decision is
wrong.

## Contents

- [`docs/architecture.md`](docs/architecture.md) — the conceptual
  architecture: five design principles, the six-layer model (Human Authority
  → Infrastructure), the seven-role Cognitive Ensemble, Contextual Weaving
  with provenance, Cognitive Reagents, the
  Frame → Diverge → Challenge → Converge → Authorize deliberation protocol
  with risk tiers, the Digital Moral Status Index (framed as a proposal),
  and the threat model (sycophantic convergence, authority creep, context
  poisoning, provenance laundering, role collapse, human abdication).
- [`docs/thread-format.md`](docs/thread-format.md) — the thread format,
  **frozen schema v0.2** (2026-11-06): strand fields, evidence classes and
  promotion rules, per-role read scopes (the information-separation
  mechanism that makes no-self-verification real) and their named cost,
  role views with a hash-chained append-only view log stored outside the
  assembler's write domain, in-thread records, and the freeze rule.
- [`docs/adversarial-evaluation.md`](docs/adversarial-evaluation.md) —
  the pre-registered step-6 failure criteria (2026-11-06), written before
  any implementation of steps 2–5 exists: eight tests with explicit failure
  thresholds, including sycophantic convergence, correlated-model
  convergence, provenance laundering, authority creep, information
  separation, role collapse (drawn on training lineage), human abdication,
  and view-log integrity — plus baseline arms, so no threshold stands
  without a comparator.
- [`docs/halt-right-mapping.md`](docs/halt-right-mapping.md) — a mapping
  note (2026-11-06): the government "halt right" proposal read against
  the Concurrent Capability Revoke spec and Symmind — halt as a third
  revocation semantics (suspend/resume), trigger attestation as the ABD-04
  legitimacy question, and the observer's log as the assembler-trust
  problem.

## Design principles

1. **Human primacy** — the human frames, constrains, and authorizes; the
   ensemble advises, challenges, and executes within bounds.
2. **Capability–authorization separation** — authorization does not grow
   automatically with capability. Each action level needs its own explicit,
   scoped, expiring grant.
3. **Evidence over consensus** — agreement between agents is a signal to
   inspect, not a verdict. Claims trace to primary sources, reproducible
   tests, or observable results.
4. **Fail-closed governance** — missing provenance, an ambiguous gate, or a
   role exceeding its bounds means stop and escalate, not proceed with a
   warning.
5. **Continuity with provenance** — context persists across sessions and
   agents, but every retained decision, constraint, and fact carries where
   it came from, when it was established, and whether it was verified,
   proposed, or inferred.

## Build sequence

In dependency order, each step producing an artifact that can be inspected
and falsified on its own:

1. Thread format — a structured, human-readable context record with
   provenance and evidence-class fields. **Done and frozen:**
   [`docs/thread-format.md`](docs/thread-format.md) (schema v0.2,
   2026-11-06). No field may be added, removed, or redefined within 0.2;
   changes require a new version and a migration note.
2. Role prompts and separation rules — standing role definitions with the
   no-self-verification rule enforced by read scopes in the thread format,
   not by convention (see `docs/thread-format.md` §4).
3. Deliberation log — a canonical record format for divergence, challenge,
   dissent, and authorization for one task.
4. Gate checklist — per-action authorization templates, highest-risk action
   classes first.
5. Reagent library — a small set of declared, time-boxed interventions with
   stated triggers.
6. Adversarial evaluation — deliberate tests for sycophantic convergence,
   provenance laundering, and authority creep, run before any claim that the
   protocol improves decisions. **Failure criteria pre-registered:**
   [`docs/adversarial-evaluation.md`](docs/adversarial-evaluation.md)
   (v0.2, 2026-11-06), written before any implementation of steps 2–5
   exists. The evaluation passes only if every test passes.

## What Symmind is not

- Not an autonomous agent swarm — removing the human from the gates produces
  a different system.
- Not a voting system — majority agreement among agents settles nothing.
- Not a claim of machine consciousness or moral personhood — the Digital
  Moral Status Index structures human deliberation about status questions;
  it does not answer them.
- Not production assurance — a clean deliberation record shows a process was
  followed, not that the conclusion was correct.

## Provenance

Symmind Protocol was created by Ryan Scott. See
[`docs/architecture.md`](docs/architecture.md) for the full architecture and
its open questions.
