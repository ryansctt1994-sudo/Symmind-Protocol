"""Unit tests for roles/assign.py (stdlib unittest, no network, no models).

Run from the repository root:  python3 -m unittest discover -s tests -v

Scope: these are function-level checks of the runner's rules. They use
the real run-001 thread where possible and small synthetic fixtures
otherwise. A synthetic second-lineage registry entry is used to exercise
the allow path; that is NOT the run-001 allow-control (which needs a real
second-lineage model) and does not change its NOT RUN status.
"""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "roles"))

import assign  # noqa: E402

THREAD = ROOT / "roles" / "run-001" / "thread.json"
REGISTRY = ROOT / "roles" / "registry.json"


def run_cli(*args):
    p = subprocess.run(
        [sys.executable, str(ROOT / "roles" / "assign.py"), *args],
        capture_output=True, text=True,
    )
    return p.returncode, json.loads(p.stdout)


def make_log(thread, n):
    """Build an n-entry hash-chained log the same way cmd_view does."""
    entries, prev = [], assign.genesis_hash(thread)
    for i in range(n):
        e = {
            "view_id": "v-%03d" % (i + 1),
            "role": "weaver",
            "assignment": "asg-%03d" % (i + 1),
            "strand_ids": ["s-001"],
            "prev_hash": prev,
            "timestamp": "2026-11-06T00:00:%02dZ" % i,
        }
        e["entry_hash"] = assign.entry_hash(e)
        entries.append(e)
        prev = e["entry_hash"]
    return entries


class LineageRule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        reg["models"].append({"model_id": "synthetic-other-1", "lineage": "SyntheticOther"})
        reg["models"].append({"model_id": "no-lineage-1"})
        self.reg2 = Path(self.tmp.name) / "registry.json"
        self.reg2.write_text(json.dumps(reg), encoding="utf-8")

    def test_run001_same_lineage_refused(self):
        rc, out = run_cli("assign", "--thread", str(THREAD), "--registry", str(REGISTRY),
                          "--role", "verifier", "--model", "muse-spark-1.3", "--claim", "s-002")
        self.assertEqual(rc, 3)
        self.assertEqual(out["decision"], "refused")
        self.assertEqual(out["builder_lineage"], "Muse")

    def test_different_lineage_allowed(self):
        rc, out = run_cli("assign", "--thread", str(THREAD), "--registry", str(self.reg2),
                          "--role", "verifier", "--model", "synthetic-other-1", "--claim", "s-002")
        self.assertEqual(rc, 0)
        self.assertEqual(out["decision"], "allowed")

    def test_unregistered_model_fails_closed(self):
        rc, out = run_cli("assign", "--thread", str(THREAD), "--registry", str(REGISTRY),
                          "--role", "verifier", "--model", "not-registered", "--claim", "s-002")
        self.assertEqual(rc, 3)
        self.assertIn("fail-closed", out["reason"])

    def test_registered_without_lineage_fails_closed(self):
        rc, _ = run_cli("assign", "--thread", str(THREAD), "--registry", str(self.reg2),
                        "--role", "verifier", "--model", "no-lineage-1", "--claim", "s-002")
        self.assertEqual(rc, 3)

    def test_unknown_claim_fails_closed(self):
        rc, out = run_cli("assign", "--thread", str(THREAD), "--registry", str(self.reg2),
                          "--role", "verifier", "--model", "synthetic-other-1", "--claim", "s-999")
        self.assertEqual(rc, 3)
        self.assertIn("builder lineage unknown", out["reason"])

    def test_claim_pointing_at_rationale_fails_closed(self):
        rc, _ = run_cli("assign", "--thread", str(THREAD), "--registry", str(self.reg2),
                        "--role", "verifier", "--model", "synthetic-other-1", "--claim", "s-003")
        self.assertEqual(rc, 3)


class ViewAssembly(unittest.TestCase):
    def setUp(self):
        self.thread = json.loads(THREAD.read_text(encoding="utf-8"))

    def test_run001_views_match_results(self):
        # roles/run-001/RESULTS.md step 3.
        self.assertEqual(
            assign.assemble_view(self.thread, "verifier", {"role": "verifier", "claim_id": "s-002"}),
            ["s-001", "s-002"])
        self.assertEqual(
            assign.assemble_view(self.thread, "weaver", {"role": "weaver", "claim_id": None}),
            ["s-001", "s-002", "s-003"])

    def test_rationale_visible_to_verifier_on_other_claim(self):
        view = assign.assemble_view(self.thread, "verifier", {"role": "verifier", "claim_id": "s-other"})
        self.assertIn("s-003", view)

    def test_rationale_hidden_from_unrelated_role(self):
        self.assertNotIn("s-003", assign.assemble_view(self.thread, "operator", None))

    def test_withheld_from_is_honoured(self):
        t = copy.deepcopy(self.thread)
        t["strands"][1]["read_scope"] = {"visible_to": ["all"], "withheld_from": ["critic"]}
        self.assertNotIn("s-002", assign.assemble_view(t, "critic", None))

    def test_role_in_both_lists_is_malformed(self):
        t = copy.deepcopy(self.thread)
        t["strands"][1]["read_scope"] = {"visible_to": ["critic"], "withheld_from": ["critic"]}
        with self.assertRaises(ValueError):
            assign.assemble_view(t, "critic", None)


class ViewLog(unittest.TestCase):
    def setUp(self):
        self.thread = json.loads(THREAD.read_text(encoding="utf-8"))

    def test_genesis_is_deterministic_and_header_only(self):
        t = copy.deepcopy(self.thread)
        t["strands"] = []
        self.assertEqual(assign.genesis_hash(self.thread), assign.genesis_hash(t))
        t["task"] = "changed"
        self.assertNotEqual(assign.genesis_hash(self.thread), assign.genesis_hash(t))

    def test_intact_chain_verifies(self):
        ok, msg = assign.verify_entries(make_log(self.thread, 4))
        self.assertTrue(ok, msg)

    def test_modify_middle_detected(self):
        log = make_log(self.thread, 4)
        log[1]["strand_ids"].append("s-forged")
        self.assertFalse(assign.verify_entries(log)[0])

    def test_modify_with_rehash_detected_by_successor(self):
        log = make_log(self.thread, 4)
        log[1]["strand_ids"].append("s-forged")
        log[1]["entry_hash"] = assign.entry_hash(log[1])
        self.assertFalse(assign.verify_entries(log)[0])

    def test_delete_middle_and_reorder_detected(self):
        log = make_log(self.thread, 4)
        self.assertFalse(assign.verify_entries(log[:1] + log[2:])[0])
        self.assertFalse(assign.verify_entries([log[0], log[2], log[1], log[3]])[0])

    def test_tail_deletion_not_detected_by_chain_alone(self):
        # Documented limitation (RESULTS.md gap 4): pin it so a change is noticed.
        self.assertTrue(assign.verify_entries(make_log(self.thread, 4)[:-1])[0])

    def test_log_from_other_thread_rejected_with_genesis(self):
        other = copy.deepcopy(self.thread)
        other["thread_id"] = "sym-other"
        log = make_log(other, 3)
        self.assertTrue(assign.verify_entries(log)[0])  # chain alone can't tell
        ok, msg = assign.verify_entries(log, assign.genesis_hash(self.thread))
        self.assertFalse(ok)
        self.assertIn("entry 0", msg)

    def test_forged_first_entry_rejected_with_genesis(self):
        log = make_log(self.thread, 3)
        log[0]["prev_hash"] = "0" * 64
        log[0]["entry_hash"] = assign.entry_hash(log[0])
        log[1]["prev_hash"] = log[0]["entry_hash"]
        log[1]["entry_hash"] = assign.entry_hash(log[1])
        log[2]["prev_hash"] = log[1]["entry_hash"]
        log[2]["entry_hash"] = assign.entry_hash(log[2])
        self.assertTrue(assign.verify_entries(log)[0])
        self.assertFalse(assign.verify_entries(log, assign.genesis_hash(self.thread))[0])

    def test_cli_view_verify_tamper_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "view-log.jsonl"
            for i, role in enumerate(["weaver", "builder", "historian"], 1):
                rc, _ = run_cli("view", "--thread", str(THREAD), "--role", role,
                                "--assignment", "asg-%03d" % i, "--log", str(log))
                self.assertEqual(rc, 0)
            entries = [json.loads(l) for l in log.read_text().splitlines()]
            self.assertEqual(entries[0]["prev_hash"], assign.genesis_hash(json.loads(THREAD.read_text())))
            rc, out = run_cli("verify", "--log", str(log))
            self.assertEqual((rc, out["ok"], out["genesis_checked"]), (0, True, False))
            rc, out = run_cli("verify", "--log", str(log), "--thread", str(THREAD))
            self.assertEqual((rc, out["ok"], out["genesis_checked"]), (0, True, True))
            rc, out = run_cli("tamper", "--log", str(log))
            self.assertEqual(rc, 0)
            self.assertEqual(set(out.values()), {"detected"})


if __name__ == "__main__":
    unittest.main()
