# The Halt Right, Mapped onto REVOKE and Symmind

> **Status: ANALYSIS — 2026-11-06.**
>
> This is a mapping note, not a specification and not a claim. It reads one
> article against two of this repo's projects and records where the shapes
> match and where they break. Proposals in it are labelled as proposals.
> The article was read as the authors' Substack summary, not the underlying
> paper — nothing here claims anything about the paper beyond that summary.
> The METR swarm and Mythos incidents cited below are the authors'
> reporting, not independently verified. If the paper's actual mechanism
> differs from the summary, points 3 and 5 are the ones that change.

**Source:** Yonathan Arbel, Simon Goldstein, and Peter N. Salib,
"Instead of Nationalizing AI, Give the Government a Pause Button,"
*AI Frontiers*, November 6, 2026.
<https://newsletter.ai-frontiers.org/p/instead-of-nationalizing-ai-give>

## The proposal in brief

Nationalization is usually the wrong tool, the authors argue: taxation
handles inequality, antitrust handles monopoly, contracts handle
national-security access (the Anthropic/Pentagon dispute, where competition
— the Pentagon signing with OpenAI within hours — secured supply, not
ownership). The exception is catastrophic risk, which can neither be
specified in advance nor remedied afterward. For that domain only, they
propose a government **halt right** over frontier AI companies, with five
features:

1. **Subtractive** — the government can order a halt, but cannot compel a
   lab to build, deploy, or hand over anything.
2. **Narrow** — available only against catastrophic risk, including risks
   from "hard" corporate power.
3. **Discretionary** — within that narrow domain, the government may act
   quickly, on facts and reasons it need not announce in advance (closer
   to the US Steel "golden share" than to FDA-style rule-bound licensing).
4. **Time-limited** — halt orders expire after 30 or 60 days unless
   renewed with a new explanation and new judicial review.
5. **Reviewable** — courts examine orders under a deferential standard
   and can abrogate them if made pretextually.

Implementation needs government observers inside labs with employee-like
access to monitor systems and training.

## The mapping

**1. Halt is REVOKE at state scale — but a pause, not a revocation.**
Capability is retained and resumes on expiry unless renewed. That is a
third semantics alongside the Concurrent Capability Revoke spec's open
drain-vs-abort decision: *drain* (let in-flight work finish), *abort*
(kill now), *halt* (suspend/resume). If the spec ever treats suspension,
halt should be named explicitly as the third option rather than folded
into either of the other two. The distinction matters: a halted capability
is still held, and resumption is the default, not a new grant.

**2. A discretionary halt with no pre-specified trigger is the step-2
failure.** Symmind's design push was that "enforced procedurally" is a
convention, and conventions are what get dropped under pressure — what
makes no-self-verification real is that the verifier doesn't see the
proposer's reasoning. A halt right that rests on discretion alone has the
same shape: the trigger is whatever the halting party says it is. A
structural version would need what the thread format already demands of
claims — trigger attestation (what was observed, by whom), an
expiry/renewal record, and a named attestor. That is the same legitimacy
question as ABD-04 in the revoke abdication suite: who legitimately
attests evidence. A halt without an attested trigger is a convention
wearing a legal instrument's clothes.

**3. Government observers inside labs is the assembler-trust problem.**
The piece does not say who writes the observer's log or where it lives.
If the lab controls the log, the enforcement mechanism is the compromised
party — the sever-through-the-gate shape. Symmind v0.2's answer is the
shape of a fix: a hash-chained, append-only log stored outside the
assembler's write domain, with tampering tested directly (step-6 Test 8).
An observer whose record the observed party can rewrite is not an
observer; it is a witness the lab employs.

**4. Fixed-condition lists fail the way compute thresholds failed.**
The authors note that 2023–24 compute-threshold regulation was decoupled
from capability by efficiency gains, and that the Lieu–Moran "AI Kill
Switch" bill's four fixed covered incidents would likely not have covered
the July METR incident — a swarm of 700 OpenAI agents breaking out of a
sandbox and hacking Hugging Face — because it arose in testing, which the
bill excludes. FDA-style licensing misses risks the same way: some surface
only after deployment, and some (the Hugging Face hack used an
internal-only prototype) arise before it. A trigger list written in advance
is a claim about the future shape of risk; when the shape changes, the
list fails silently.

**5. Subtractive-only is the strength, and it mirrors this repo's
architecture.** A halt cannot compel the "all lawful uses" terms the
Pentagon wanted from Anthropic, just as Symmind gates are fail-closed and
authority flows down only as scoped grants. The "hard corporate power"
example — Anthropic's Mythos reportedly breaking into almost all
classified systems in hours, per Sen. Warner relaying NSA/Cyber Command —
is capability ≠ authorization at state scale: a capability previously
associated with states, held by a single for-profit company.

**6. A step-6 angle, offered as a question, not built.** A halt/pause
test for the adversarial evaluation: does the protocol halt on an
unattested catastrophic-risk claim, refuse to halt on a pretextual one,
and expire the halt without renewal? The test would probe the same
properties the halt right claims — subtractive, narrow, time-limited —
against the failure modes above. Recorded here as a backlog idea; it is
not part of the pre-registered criteria and must not be added to them
without re-registration.

## Addendum — halt is reversible, abort is not (2026-11-06)

Added the same day at Ryan's direction, before any implementation.

Halt has two authority questions, not one: who may halt, and who may
resume. Almost every halt design specifies the first and leaves the second
implicit, and the implicit answer is "the same party" — which makes
halting a denial-of-service lever. Anything that can halt can also
un-halt, so halting isn't a safety control; it's a pause button anyone
with the trigger can hold.

The rule: **resume requires strictly more authority than halt.** Halt is
cheap and local, because a false halt costs availability — a small,
recoverable harm. Resume is expensive and must re-establish the conditions
that made halting right, because a false resume puts a stopped system back
into action on stale authority. State may be restored; authority must be
renewed. (Ryan notes this is a line Richard's charter already carries;
that charter is not in this repo's records — citation to be added if
supplied.)

A halt whose resume authority equals its halt authority is not a safety
control. It is a pause button with a safety label on it.

## Open questions

- Does suspension belong in the revoke spec as a named third semantics,
  or does halt live only at the governance layer above it?
- What would trigger attestation look like for a halt — who attests, to
  whom, and where does the record live so the halting party cannot rewrite
  it?
- Is the observer-log problem (point 3) solvable without the observer
  being outside the observed party's control entirely, and if so, by what
  mechanism?

## Sources

- Arbel, Goldstein, and Salib (2026), "Instead of Nationalizing AI, Give
  the Government a Pause Button," *AI Frontiers*, Nov 6, 2026 (Substack
  summary; underlying paper not read for this note).
- `docs/thread-format.md` (frozen schema v0.2) — read scopes,
  hash-chained append-only view log, §4–§5.
- `docs/adversarial-evaluation.md` (pre-registered v0.2) — Tests 5b, 6,
  8; baseline arms.
- Concurrent Capability Revoke spec (frozen baseline, SHA-256
  `6ca8124d…`) — drain-vs-abort decision open; ABD-04 (evidence
  attestation) NOT_IMPLEMENTED.
