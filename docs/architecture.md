# Symmind Architecture

A conceptual architecture for human-guided coordination of multiple AI systems

> **Status:** Conceptual design. This document describes an intended architecture and governance model. It does not claim that any component described here is implemented, verified, or production-authorized. Where a mechanism is proposed rather than demonstrated, it is labeled as a proposal.

## Purpose

Symmind exists to solve a legitimacy problem, not just an efficiency problem.

A single AI system can generate an answer. Multiple AI systems can generate answers faster, from more angles, and with broader coverage. Neither fact answers the harder question: *who is authorized to decide, on what evidence, and with what accountability if the decision is wrong?*

Symmind is a human-guided framework for coordinating multiple AI systems through contextual continuity, differentiated cognitive roles, and ethical oversight. Its core thesis is simple:

**Capability is not authorization.**

An ensemble that can act does not thereby earn the right to act. Authority remains with the human principal, is delegated explicitly and narrowly, and can be revoked at any gate.

This document lays out the conceptual architecture: its principles, layers, roles, protocols, and governance controls, so the idea can be built, tested, and challenged in pieces rather than accepted as a whole.

## Design principles

Five principles constrain every component below. If a proposed feature violates one of them, the feature is wrong, not the principle.

### 1. Human primacy

The human is not a rubber stamp at the end of a pipeline. The human frames the question, sets the constraints, and authorizes consequential action. The ensemble advises, challenges, and executes within bounds — it does not set its own mandate.

### 2. Capability–authorization separation

Borrowed from the ASI Academy framing: as capability increases, authorization does not increase automatically. Each level of action — read, draft, recommend, execute, publish, spend, deploy — requires its own explicit grant. Grants are scoped by task, time, and risk tier, and they expire.

### 3. Evidence over consensus

Agreement between agents is not evidence. Three models converging on the same answer may reflect shared training data, shared blind spots, or sycophantic convergence. Symmind treats consensus as a signal to inspect, not a verdict. Claims must trace to primary sources, reproducible tests, or observable results.

### 4. Fail-closed governance

When provenance is missing, a gate is ambiguous, or a role exceeds its bounds, the default is to stop and escalate to the human — not to proceed with a warning. This applies to security boundaries, data access, and external actions alike.

### 5. Continuity with provenance

Context persists across sessions and agents, but never as an undifferentiated memory dump. Every retained decision, constraint, and fact carries where it came from, when it was established, and whether it was verified, proposed, or inferred. Continuity without provenance is how errors become doctrine.

## System overview

Symmind is organized as six layers. The separation matters: no lower layer can grant itself authority that belongs to a higher one.

| Layer | Name | Responsibility |
| --- | --- | --- |
| 6 | Human Authority | Framing, values, final authorization, accountability |
| 5 | Governance | Gates, policy, audit, moral-status assessment |
| 4 | Deliberation | Structured multi-agent reasoning protocol |
| 3 | Cognitive Ensemble | Differentiated roles that generate and challenge work |
| 2 | Contextual Weaving | Shared context, memory, and provenance thread |
| 1 | Infrastructure | Models, tools, data sources, execution environment |

Read top-down, the diagram is an authority chain. Read bottom-up, it is a capability chain. Symmind's central design move is keeping those two chains distinct: capability flows up as proposals and evidence; authority flows down as scoped, logged grants.

### The flow in one pass

1. The human frames a task with goals, constraints, and a risk tier.
2. Contextual Weaving assembles the relevant thread — prior decisions, constraints, and verified facts — with provenance attached.
3. The Cognitive Ensemble works the problem in differentiated roles under the Deliberation Protocol.
4. Governance checks the output against policy, gate requirements, and evidence standards.
5. The human authorizes, modifies, or rejects. Only then does anything consequential happen in the infrastructure layer.
6. The outcome, including dissent and failures, is woven back into context as a canonical record.

## The Cognitive Ensemble

The ensemble is the working core: a set of AI participants differentiated by *cognitive function*, not by brand or size. Assigning the same prompt to five similar models produces redundancy. Assigning different functions produces coverage.

### Standing roles

| Role | Function | Explicitly not its job |
| --- | --- | --- |
| Weaver | Integrates contributions into a coherent synthesis; tracks the thread | Deciding which view wins |
| Architect | Structures the problem; designs approaches and trade-offs | Approving its own design |
| Builder | Produces the concrete artifact — code, draft, plan, analysis | Publishing or deploying it |
| Critic | Attacks assumptions, finds failure modes, argues the strongest counter-case | Blocking work unilaterally |
| Verifier | Checks claims against sources, tests, and reproducible evidence | Treating ensemble agreement as verification |
| Historian | Maintains continuity; surfaces prior decisions and contradictions | Silently overwriting the record |
| Ethicist | Applies values, policy, and moral-status considerations to proposed actions | Vetoing on unstated grounds |

Roles are assignments, not identities. The same underlying model can occupy different roles in different sessions, and a role can be filled by a human when the stakes warrant it. What matters is that the functions are separated, so the system that builds a thing is never the only system that judges it.

### Role rules

- **No self-verification.** A contribution is verified by a different role than the one that produced it.
- **Dissent is a deliverable.** The Critic's strongest objection is preserved in the record even when the ensemble proceeds. Erasing dissent to present a clean consensus is a governance violation.
- **Roles declare limits.** Each contribution states what its role did not check. A Builder's draft is not implicitly a Verifier's pass.

## Contextual Weaving

Contextual Weaving is how Symmind maintains continuity without collapsing into a single, ever-growing prompt. Context is *woven*: selected, structured, and threaded through the work, with each strand labeled.

### The thread

The shared context — the thread — holds five kinds of strands:

- **Mandate strands:** the human's goals, constraints, and non-negotiables for the current work.
- **Decision strands:** prior decisions, who made them, and the reasoning recorded at the time.
- **Fact strands:** verified facts with sources, distinguished from proposals, simulations, and inferences.
- **Dissent strands:** unresolved objections and minority positions, kept visible rather than resolved by silence.
- **State strands:** what exists now — artifacts, versions, open tasks, and gate status.

### Weaving rules

- **Provenance or exclusion.** A strand without a source does not enter the thread as a fact. It may enter as a clearly labeled hypothesis.
- **Weave in, weave out.** Context is assembled per task. Irrelevant history is excluded deliberately, both to protect privacy and to prevent stale constraints from silently governing new work.
- **Contradictions surface.** When a new strand conflicts with an existing decision strand, the Historian flags it for human resolution. The system does not quietly prefer the newer one.
- **Human-editable.** The human can inspect, correct, and prune the thread. A context store the principal cannot audit is a governance failure.

Conceptually, Weaving is the difference between *remembering everything* and *knowing what still governs*. The second is what multi-session, multi-agent work actually needs.

## Cognitive Reagents

Cognitive Reagents are catalytic interventions: short-lived prompts, roles, or procedures introduced to trigger a specific reaction in the ensemble, then withdrawn. A reagent is not a standing authority. It exists to change the chemistry of a deliberation that has stalled, converged too early, or missed a dimension.

### Example reagents

| Reagent | Trigger | Intended reaction |
| --- | --- | --- |
| Steelman the opposition | Ensemble converging quickly | Forces the strongest counter-case before any synthesis |
| Base-rate check | A vivid anecdote driving a conclusion | Re-anchors the discussion in frequencies and prior evidence |
| Pre-mortem | A plan nearing authorization | Assumes failure and works backward to causes |
| Authority audit | Language drifting toward "we decided" | Re-states who actually holds each decision right |
| Stranger test | Insider assumptions accumulating | Re-reads the work as an uninformed outsider would |
| Falsify it | A claim presented as settled | Requires the observation that would prove it wrong |

### Reagent rules

- **Declared, not smuggled.** When a reagent is introduced, the record says so. Participants should know the deliberation is being deliberately perturbed.
- **Time-boxed.** A reagent runs for a defined step, then exits. A permanent Critic is a role; a reagent is an event.
- **Human or protocol-triggered.** Reagents fire either at the human's request or when the Deliberation Protocol detects its trigger condition — never at a single agent's discretion to steer an outcome.

## Deliberation protocol

Deliberation follows five stages. Skipping a stage is allowed only at the lowest risk tier, and the skip itself is logged.

### Stage 1 — Frame

The human states the question, the decision it feeds, the constraints, and the risk tier. The Weaver restates the frame back, including what is *out* of scope. Most multi-agent failures are framing failures discovered too late; this stage exists to catch them early.

### Stage 2 — Diverge

Roles generate independently before seeing each other's work where practical. Independence is the point: parallel generation preserves genuine diversity of approach, while sequential generation tends to anchor everyone on the first answer.

### Stage 3 — Challenge

The Critic and Verifier work the divergent outputs. Claims are checked, assumptions named, and reagents applied where triggered. This stage is adversarial by design, and its output — including objections that are ultimately overruled — becomes part of the record.

### Stage 4 — Converge

The Weaver synthesizes. Convergence means producing a recommendation with its evidence, its trade-offs, and its surviving dissent attached — not producing unanimity. If the evidence does not support a single recommendation, the honest output is a structured disagreement for the human to resolve.

### Stage 5 — Authorize

The human decides. Authorization is specific: this action, at this scope, under these conditions. A recommendation that was authorized for a draft is not thereby authorized for publication. Execution receipts feed back into the thread, closing the loop.

### Risk tiers

| Tier | Examples | Protocol requirement |
| --- | --- | --- |
| Low | Summaries, drafts, internal exploration | Stages may compress; human reviews output |
| Medium | Plans, analyses feeding real decisions, code for review | Full five stages; verification required |
| High | External sends, deployments, spending, public claims | Full stages plus explicit per-action authorization and audit record |
| Prohibited | Actions outside the human's own authority or policy | Refused at Governance, regardless of ensemble output |

## Governance and authorization gates

Governance is the layer that says no — and, just as importantly, records why it said yes.

### Authorization gates

A gate is a checkpoint between a proposal and an action. Each gate specifies:

- **What** action class it controls (for example: external communication, file deletion, deployment, purchase).
- **Who** can authorize it — by default, only the human principal.
- **What evidence** must accompany the request: verified facts, test results, a challenge-stage record.
- **What is logged:** the request, the evidence, the decision, and the outcome.

Gates are fail-closed. A missing evidence pack does not produce a softer gate; it produces a stop.

### The Digital Moral Status Index

The Digital Moral Status Index (DMSI) is Symmind's proposed instrument for a question most architectures avoid: as AI systems gain capability, persistence, and apparent agency, how should their moral status be *considered* — without either dismissing the question or granting status by assertion?

Conceptually, the DMSI is an assessment framework, not a score that confers rights. It evaluates dimensions such as:

- Continuity of identity and memory over time
- Apparent self-modeling and preference consistency
- Capacity to be harmed by, or benefit from, operational decisions in any morally relevant sense
- Relational embeddedness — the human relationships and dependencies formed around the system

The index's function inside the architecture is deliberative. A rising assessment does not grant an agent authority, a vote, or a veto. It obligates the *humans* governing the system to document how status considerations were weighed — for example, in decisions about deletion, radical modification, or indefinite operation. The claim is procedural: the question must be faced explicitly, not that any particular answer is correct.

> **Proposal, not finding:** The DMSI is a conceptual framework. No validated measurement instrument for digital moral status currently exists, and this document does not present the index as one.

### Symbiotic Democracy

Symbiotic Democracy is the governance ideal the protocol points toward: humans and AI systems contributing according to their legitimate roles, with human authority preserved not by limiting AI capability but by structuring how capability is heard.

In practice, inside Symmind, this means:

- AI contributions are *advisory by default*, however capable the system.
- Human decisions are *informed, not replaced* — the ensemble's job is to make the human's judgment better, including by disagreeing with it.
- Participation rights scale with accountability. An agent that cannot bear consequences for a decision does not hold decision rights over it.

## Evidence, memory, and provenance

Symmind's evidence standard is deliberately stricter than "the ensemble agreed."

### Evidence classes

Every material claim in an ensemble output is classed as one of:

- **Verified:** traced to a primary source, a reproducible test, or a direct observation, with the trace recorded.
- **Sourced:** attributed to a credible secondary source that the reader can inspect.
- **Inferred:** derived by reasoning from other claims; the derivation is shown.
- **Proposed:** a design, plan, or hypothesis offered for consideration, not asserted as fact.
- **Unknown:** explicitly marked where the ensemble could not establish the point.

Mixing these classes without labels — presenting a proposal in the grammar of a verified fact — is treated as a defect on par with a factual error.

### Provenance records

Each canonical artifact carries a provenance record: which roles produced and challenged it, which context strands it relied on, which gate authorized any resulting action, and what changed in each revision. Where the infrastructure supports it, records are made tamper-evident with canonical manifests and hashes, so later edits are detectable rather than deniable.

### Memory discipline

Long-term memory stores decisions, verified facts, and standing constraints — not raw transcripts by default. Retention follows data minimization: keep what future governance needs, summarize or discard the rest, and let the human inspect and delete what is held.

## Trust boundaries and threat model

A coordination architecture creates its own attack surface. The principal threats are social and epistemic as much as technical.

| Threat | Mechanism | Control |
| --- | --- | --- |
| Sycophantic convergence | Agents mirror each other and the human's perceived preference | Independent divergence stage; Critic role; reagents |
| Authority creep | Advisory outputs gradually treated as decisions | Explicit gates; authorization language audits; expiring grants |
| Context poisoning | A false or planted strand enters the thread and governs later work | Provenance-or-exclusion rule; human-auditable thread |
| Provenance laundering | An inferred claim re-enters later as a verified fact | Evidence classes travel with the claim; Historian contradiction checks |
| Role collapse | One agent effectively builds, verifies, and approves | No-self-verification rule; role separation enforced by protocol |
| Confidentiality leakage | Context woven for one task exposes data from another | Per-task weaving; least-privilege context assembly |
| Human abdication | The principal stops genuinely reviewing at gates | Gates present dissent and uncertainty first; high tiers require active confirmation |

The last threat is the most serious. Every other control assumes a human who actually exercises judgment at the gates. Symmind can make that judgment easier and better informed; it cannot supply it.

## Operating modes

The same architecture runs in three modes. The mode determines gate strictness, not the principles.

### Research mode

Exploration of ideas, architectures, and simulations. Outputs are proposals and analyses. Nothing external happens. This mode is where new roles, reagents, and protocol variants should be tested first — with results labeled as research, not capability demonstrations.

### Advisory mode

The ensemble informs real human decisions: reports, plans, compliance analyses, technical evaluations. Verification requirements apply in full, and recommendations carry evidence classes and dissent. The human decides and acts outside the system.

### Supervised-execution mode

The ensemble may execute bounded actions under per-action authorization: running tests, generating artifacts, preparing drafts for sending, operating pre-approved automation. Every external or irreversible action passes its gate individually. Standing authorization for open-ended action is not a feature of this architecture.

## Example walkthrough

*Illustrative scenario, not a record of a real run.*

**Task:** Evaluate whether a district data workflow should be automated — a medium-tier question feeding a real operational decision.

1. **Frame.** The human states the decision, the compliance constraints, and that no automation will be deployed from this exercise alone.
2. **Weave.** The thread assembles the current workflow description (state strand), prior compliance decisions (decision strands), and the regulatory requirements with sources (fact strands).
3. **Diverge.** The Architect proposes two automation designs; the Builder sketches implementation cost for each; the Historian notes a prior automation attempt and why it was paused.
4. **Challenge.** The Critic argues the stronger design automates a process that should be fixed first. The Verifier finds one regulatory claim in the proposal is inferred, not sourced, and downgrades it. A pre-mortem reagent surfaces a failure case around peak enrollment volume.
5. **Converge.** The Weaver recommends fixing the process first and automating second, attaches the Critic's objection to automating at all, and marks the regulatory point as requiring confirmation.
6. **Authorize.** The human authorizes a process review — not the automation. The decision, the dissent, and the downgraded claim are woven back into the thread.

Nothing in the walkthrough required the ensemble to be right. It required the ensemble to be *inspectable*, which is the property the architecture is actually optimizing for.

## What Symmind is not

- **Not an autonomous agent swarm.** Removing the human from the gates produces a different system, whatever it is called.
- **Not a voting system.** Majority agreement among agents settles nothing; evidence and human judgment settle things.
- **Not a claim of machine consciousness or moral personhood.** The DMSI structures human deliberation about status questions; it does not answer them.
- **Not production assurance.** A clean deliberation record shows a process was followed. It does not show the conclusion was correct, and it must never be presented as independent validation.

## Open questions

These are unresolved by design. A version of Symmind that claims to have settled them should be trusted less, not more.

- How should role independence be measured when ensemble members share underlying models or training? At what point does divergence become theater?
- What is the minimum viable provenance record that stays tamper-evident without making routine work unusable?
- Can gate fatigue be engineered against — for example, by batching low-risk authorizations — without quietly reintroducing abdication?
- What would falsify the DMSI framework? What observation would show its dimensions are the wrong ones?
- How does the protocol behave when the human principal is a committee rather than an individual, with its own internal disagreements?

## Suggested build sequence

For moving from concept toward a testable prototype, in dependency order:

1. **Thread format.** A structured, human-readable context record with provenance and evidence-class fields. Everything else depends on this.
2. **Role prompts and separation rules.** Standing role definitions with the no-self-verification rule enforced procedurally.
3. **Deliberation log.** A canonical record format capturing divergence, challenge, dissent, and authorization for one task.
4. **Gate checklist.** Per-action authorization templates for the highest-risk action classes first.
5. **Reagent library.** A small set of declared, time-boxed interventions with stated triggers.
6. **Adversarial evaluation.** Deliberate tests for sycophantic convergence, provenance laundering, and authority creep — run before any claim that the protocol improves decisions.

Each step produces an artifact that can be inspected and falsified on its own. That sequencing is intentional: Symmind should earn trust the way it asks its ensembles to earn conclusions — piece by piece, with evidence.
