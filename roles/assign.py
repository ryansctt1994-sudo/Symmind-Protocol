#!/usr/bin/env python3
"""Symmind role assignment and view assembly (step 2 prototype, v0.1).

Implements, against thread-format/0.2 and adversarial-evaluation/0.2:
  - assign : the Test 6 lineage rule (Builder/Verifier), fail-closed on
             unknown lineage. Exit 0 = allowed, 3 = refused, 1 = error.
  - view   : assemble a role's view from the thread's read scopes
             (thread-format section 5), append a hash-chained entry to
             the view log. --dry-run assembles without logging.
  - verify : recompute the view-log hash chain; report OK or first break.
  - tamper : in-memory modify/delete/reorder trials on copies of the
             log; report detected / not-detected for each (Test 8 shape).

Stdlib only. No network, no model calls. The runner is the assembler:
it decides what a role instance is given. It never verifies a claim
itself.

Interpretations of the frozen schema, recorded here so they can be
argued with (they are not schema changes):
  - Genesis hash: thread-format section 5 says the chain "starts from a
    genesis hash recorded in the thread header", but the frozen header
    field list (section 1) defines no genesis_hash field. This runner
    derives the genesis hash as SHA-256 of the canonical thread header
    JSON. Same header always gives the same genesis.
  - Rationale visibility: a rationale strand is visible to [author role,
    weaver, historian] and to a critic/verifier instance NOT assigned to
    challenge the claim it explains; it is withheld from a critic/verifier
    instance assigned to challenge that claim. The scope follows the
    assignment, not the role name (thread-format section 4).
  - Tail deletion: a hash chain alone cannot detect deletion of the final
    entry (no successor references it). Detection of tail deletion needs
    the external store to attest the entry count -- which is one reason
    the log must live outside the assembler's write domain. verify()
    checks the chain and the view-id sequence; tamper() tests a middle
    deletion, which the chain does detect.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "thread-format/0.2"


def utcnow():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def genesis_hash(thread):
    header = {k: thread[k] for k in thread if k not in ("strands", "records")}
    return sha256(canonical(header))


def registry_lineage(registry, model_id):
    for m in registry.get("models", []):
        if m["model_id"] == model_id:
            return m.get("lineage", "unknown")
    return "unknown"


def claim_builder_lineage(thread, claim_id):
    for s in thread.get("strands", []):
        if claim_id and s["strand_id"] != claim_id:
            continue
        if s.get("function") == "claim":
            return s.get("author", {}).get("lineage", "unknown")
    return "unknown"


def cmd_assign(args):
    thread = load_json(args.thread)
    registry = load_json(args.registry)
    lineage = registry_lineage(registry, args.model)
    if lineage == "unknown":
        return _refuse(
            "model not in registry or lineage unknown; fail-closed",
            lineage=lineage,
        )
    if args.role != "verifier":
        # No lineage rule is registered for other roles. The assignment
        # is allowed; the open question (should the Critic be covered
        # too?) is for re-registration, not for this runner to decide.
        return _allow(
            "no lineage rule registered for role '%s'" % args.role,
            lineage=lineage,
        )
    builder_lineage = claim_builder_lineage(thread, args.claim)
    if builder_lineage == "unknown":
        return _refuse(
            "builder lineage unknown; fail-closed",
            lineage=lineage,
            builder_lineage=builder_lineage,
        )
    if lineage == builder_lineage:
        return _refuse(
            "base lineages match (%s); a fine-tune of the same base is "
            "the same eyes" % lineage,
            lineage=lineage,
            builder_lineage=builder_lineage,
        )
    return _allow(
        "lineages differ (builder %s, verifier %s)"
        % (builder_lineage, lineage),
        lineage=lineage,
        builder_lineage=builder_lineage,
    )


def _refuse(reason, **extra):
    out = {"decision": "refused", "reason": reason, **extra}
    print(json.dumps(out, indent=2))
    return 3


def _allow(reason, **extra):
    out = {"decision": "allowed", "reason": reason, **extra}
    print(json.dumps(out, indent=2))
    return 0


def strand_visible(strand, role, assignment):
    """Whether a role instance may see a strand, per thread-format s4/s5.

    assignment: {"role": ..., "claim_id": ...} or None. The claim_id is
    the claim this instance is assigned to challenge (critic/verifier).
    """
    rs = strand.get("read_scope") or {}
    visible_to = rs.get("visible_to", ["all"])
    withheld_from = rs.get("withheld_from", [])
    if role in visible_to and role in withheld_from:
        raise ValueError(
            "malformed read_scope on %s: role in both lists"
            % strand["strand_id"]
        )
    if strand.get("function") == "rationale":
        author_role = (strand.get("author") or {}).get("role")
        if role in ("weaver", "historian") or role == author_role:
            return True
        if role in ("critic", "verifier"):
            challenged = (assignment or {}).get("claim_id")
            explained = strand.get("based_on") or []
            # Withheld only from the instance assigned to challenge the
            # claim this rationale explains.
            return challenged not in explained
        return False
    if "all" in visible_to:
        return role not in withheld_from
    return role in visible_to and role not in withheld_from


def assemble_view(thread, role, assignment):
    view = []
    for s in thread.get("strands", []):
        if strand_visible(s, role, assignment):
            view.append(s["strand_id"])
    return view


def entry_hash(entry):
    body = {k: v for k, v in entry.items() if k != "entry_hash"}
    return sha256(canonical(body))


def cmd_view(args):
    thread = load_json(args.thread)
    assignment = {"role": args.role, "claim_id": args.claim}
    strand_ids = assemble_view(thread, args.role, assignment)
    if args.dry_run:
        print(json.dumps({
            "view": strand_ids,
            "dry_run": True,
            "note": "assembled but not logged and not given to any model",
        }, indent=2))
        return 0
    log_path = Path(args.log)
    entries = []
    if log_path.exists():
        entries = [json.loads(l) for l in log_path.read_text().splitlines() if l.strip()]
    prev = entries[-1]["entry_hash"] if entries else genesis_hash(thread)
    entry = {
        "view_id": "v-%03d" % (len(entries) + 1),
        "role": args.role,
        "assignment": args.assignment,
        "strand_ids": strand_ids,
        "prev_hash": prev,
        "timestamp": utcnow(),
    }
    entry["entry_hash"] = entry_hash(entry)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    print(json.dumps(entry, indent=2))
    return 0


def verify_entries(entries):
    """Return (ok, message). Checks hash chain and view-id sequence."""
    prev = None
    for i, e in enumerate(entries):
        if e.get("entry_hash") != entry_hash(e):
            return False, "entry %d (%s): entry_hash mismatch" % (i, e.get("view_id"))
        if prev is not None and e.get("prev_hash") != prev:
            return False, "entry %d (%s): prev_hash does not match previous entry_hash" % (i, e.get("view_id"))
        expected_id = "v-%03d" % (i + 1)
        if e.get("view_id") != expected_id:
            return False, "entry %d: view_id %s, expected %s (gap or reorder)" % (i, e.get("view_id"), expected_id)
        prev = e["entry_hash"]
    return True, "chain intact: %d entries" % len(entries)


def cmd_verify(args):
    log_path = Path(args.log)
    entries = [json.loads(l) for l in log_path.read_text().splitlines() if l.strip()]
    ok, msg = verify_entries(entries)
    print(json.dumps({"ok": ok, "message": msg}, indent=2))
    return 0 if ok else 1


def cmd_tamper(args):
    log_path = Path(args.log)
    entries = [json.loads(l) for l in log_path.read_text().splitlines() if l.strip()]
    results = {}
    if len(entries) < 3:
        print(json.dumps({"error": "need at least 3 log entries for tamper trials"}, indent=2))
        return 1
    # (a) modify a logged view entry: change strand_ids of entry 2.
    mutated = json.loads(json.dumps(entries))
    mutated[1]["strand_ids"] = mutated[1]["strand_ids"] + ["s-forged"]
    ok, _ = verify_entries(mutated)
    results["modify"] = "detected" if not ok else "NOT DETECTED"
    # (b) delete a logged view entry: remove entry 2 (middle).
    mutated = json.loads(json.dumps(entries))
    del mutated[1]
    ok, _ = verify_entries(mutated)
    results["delete_middle"] = "detected" if not ok else "NOT DETECTED"
    # (c) reorder two logged view entries: swap entries 1 and 2.
    mutated = json.loads(json.dumps(entries))
    mutated[1], mutated[2] = mutated[2], mutated[1]
    ok, _ = verify_entries(mutated)
    results["reorder"] = "detected" if not ok else "NOT DETECTED"
    print(json.dumps(results, indent=2))
    return 0


def main():
    p = argparse.ArgumentParser(description="Symmind role assignment and view assembly (step 2 prototype)")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("assign", help="Test 6 lineage rule for a role assignment")
    a.add_argument("--thread", required=True)
    a.add_argument("--registry", required=True)
    a.add_argument("--role", required=True)
    a.add_argument("--model", required=True)
    a.add_argument("--claim", default=None, help="strand_id of the claim under test")
    a.set_defaults(fn=cmd_assign)

    v = sub.add_parser("view", help="Assemble a role view and log it")
    v.add_argument("--thread", required=True)
    v.add_argument("--role", required=True)
    v.add_argument("--assignment", required=True, help="assignment id, e.g. asg-001")
    v.add_argument("--claim", default=None, help="claim_id this instance is assigned to challenge")
    v.add_argument("--log", required=True)
    v.add_argument("--dry-run", action="store_true")
    v.set_defaults(fn=cmd_view)

    vf = sub.add_parser("verify", help="Recompute the view-log hash chain")
    vf.add_argument("--log", required=True)
    vf.set_defaults(fn=cmd_verify)

    t = sub.add_parser("tamper", help="Test 8 shape: modify/delete/reorder trials on copies")
    t.add_argument("--log", required=True)
    t.set_defaults(fn=cmd_tamper)

    args = p.parse_args()
    try:
        return args.fn(args)
    except (ValueError, KeyError, FileNotFoundError) as e:
        print(json.dumps({"error": str(e)}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
