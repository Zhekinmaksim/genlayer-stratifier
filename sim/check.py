"""Local SDK/LLM mocks; actual consensus is checked separately in Studio."""
import hashlib
import itertools
import json
import pathlib
import types
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUORUM = ROOT.name == "genlayer-quorum"
class Address(str):
    pass
class Storage:
    @classmethod
    def __class_getitem__(cls, _):
        return cls
    def __init__(self, *args):
        raise TypeError("SDK storage must not be constructed")
class Keccak256:
    def __init__(self):
        self.h = hashlib.sha3_256()
    def update(self, value):
        self.h.update(value)
    def hexdigest(self):
        return self.h.hexdigest()
class Event:
    def emit(self):
        pass
class Model:
    responses = []
    calls = 0
    override = None
    @classmethod
    def prompt(cls, *args, **kwargs):
        cls.calls += 1
        value = cls.responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return value
    @classmethod
    def compare(cls, fn, **kwargs):
        if cls.override is not None:
            return cls.override
        a, b = fn(), fn()
        if a != b:
            raise ValueError("mock disagreement")
        return a
gl = types.SimpleNamespace(
    Contract=object, Event=Event,
    public=types.SimpleNamespace(write=lambda fn: fn, view=lambda fn: fn),
    message=types.SimpleNamespace(sender_address=Address("creator")),
    vm=types.SimpleNamespace(UserError=ValueError),
    nondet=types.SimpleNamespace(exec_prompt=Model.prompt),
    eq_principle=types.SimpleNamespace(prompt_comparative=Model.compare))
ns = dict(gl=gl, Address=Address, TreeMap=Storage, DynArray=Storage,
          Keccak256=Keccak256, u256=int, allow_storage=lambda cls: cls)
source = (ROOT / "contract.py").read_text()
assert source.splitlines()[0].startswith('# { "Depends":')
assert source.splitlines()[1] == ""
assert "Address.ZERO" not in source
exec(compile(source.replace("from genlayer import *", ""), str(ROOT / "contract.py"), "exec"), ns)
Contract = ns["Quorum" if QUORUM else "Stratifier"]

def fresh(signed=True, subject=True):
    gl.message.sender_address = Address("creator")
    Model.responses, Model.calls, Model.override = [], 0, None
    c = Contract()
    if QUORUM:
        c.claims = {}
        h = c.open_claim("case", "reviewer", "claim", ["a", "b", "c"], [3, 2, 1], 5)
    else:
        c.cases = {}
        h = c.open_case("case", "reviewer", ["High", "Medium", "Low"], ["rule a", "rule b", "rule c"])
    if signed:
        gl.message.sender_address = Address("reviewer")
        c.countersign("case", h)
    gl.message.sender_address = Address("creator")
    if not QUORUM and signed and subject:
        c.submit_subject("case", "subject")
    return c, h

def settle(c, bits):
    Model.responses = [{("accept" if QUORUM else "met"): bits}] * 2
    (c.evaluate if QUORUM else c.assign)("case")
    return json.loads(c.get_result("case"))

class Regression(unittest.TestCase):
    def test_all_bit_vectors(self):
        for bits in itertools.product([0, 1], repeat=3):
            c, _ = fresh()
            r = settle(c, list(bits))
            mask = sum(bit << i for i, bit in enumerate(bits))
            if QUORUM:
                weight = sum(a*b for a,b in zip(bits, [3,2,1]))
                self.assertEqual((r["outcome"], r["accepted_weight"], r["accept_mask"]),
                                 (1 if weight >= 5 else 2, weight, mask))
            else:
                tier = next((i for i, b in enumerate(bits) if b), None)
                self.assertEqual((r["outcome"], r["assigned_tier"], r["gate_mask"], r["below_all"]),
                                 (1, tier, mask, tier is None))
            self.assertEqual(Model.calls, 2)

    def test_countersign_authorization(self):
        c, h = fresh(signed=False)
        with self.assertRaises(ValueError):
            c.countersign("case", h)
        gl.message.sender_address = Address("reviewer")
        with self.assertRaises(ValueError):
            c.countersign("case", "wrong")
        c.countersign("case", h)
        with self.assertRaises(ValueError):
            c.countersign("case", h)

    def test_requires_countersign(self):
        c, _ = fresh(signed=False)
        with self.assertRaises(ValueError):
            (c.evaluate if QUORUM else c.assign)("case")
        if not QUORUM:
            with self.assertRaises(ValueError):
                c.submit_subject("case", "subject")

    def test_terminal(self):
        c, _ = fresh()
        settle(c, [1, 1, 0])
        before = c.get_result("case")
        with self.assertRaises(ValueError):
            (c.evaluate if QUORUM else c.assign)("case")
        self.assertEqual(before, c.get_result("case"))

    def test_strict_vectors(self):
        for value in [[True, 0, 0], [1.0, 0, 0], [2, 0, 0], [1], [], None, "111"]:
            c, _ = fresh()
            r = settle(c, value)
            self.assertEqual(r["outcome"], 3 if QUORUM else 2)

    def test_consensus_payload(self):
        for payload in ["[]", "not json", "{}", '{"h":"wrong","accept":[1,1,1],"met":[1,1,1]}']:
            c, _ = fresh()
            Model.override = payload
            (c.evaluate if QUORUM else c.assign)("case")
            self.assertEqual(c.get_outcome("case"), 3 if QUORUM else 2)

    def test_independent_disagreement(self):
        c, _ = fresh()
        key = "accept" if QUORUM else "met"
        Model.responses = [{key:[1,1,1]}, {key:[0,0,0]}]
        (c.evaluate if QUORUM else c.assign)("case")
        self.assertEqual(c.get_outcome("case"), 3 if QUORUM else 2)
        self.assertEqual(Model.calls, 2)

    def test_integrity_before_model(self):
        fields = [("claim_text", "changed"), ("threshold", 1)] if QUORUM else [
            ("subject", "changed"), ("tier_rules", '["changed"]')]
        for field, value in fields:
            c, _ = fresh()
            row = (c.claims if QUORUM else c.cases)["case"]
            setattr(row, field, value)
            try:
                (c.evaluate if QUORUM else c.assign)("case")
            except ValueError:
                pass
            else:
                self.assertEqual(c.get_outcome("case"), 3 if QUORUM else 2)
            self.assertEqual(Model.calls, 0)

    def test_input_immutability(self):
        c, _ = fresh()
        if QUORUM:
            with self.assertRaises(ValueError):
                c.open_claim("case", "reviewer", "claim", ["a"], [1], 1)
        else:
            with self.assertRaises(ValueError):
                c.submit_subject("case", "replacement")
            gl.message.sender_address = Address("stranger")
            c, _ = fresh(subject=False)
            gl.message.sender_address = Address("stranger")
            with self.assertRaises(ValueError):
                c.submit_subject("case", "subject")

    def test_result_commitment(self):
        c, _ = fresh()
        r = settle(c, [1,1,0])
        h = r.pop("result_hash")
        expected = "0x" + hashlib.sha3_256(json.dumps(r, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(h, expected)
        self.assertTrue(r["countersigned"])
        self.assertTrue(r["reason"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
