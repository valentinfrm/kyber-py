import json
import kem
import params
from kyber_py.ml_kem import ML_KEM_512

k_map = {
    "ML-KEM-512":  {"k": 2, "eta1": 3, "du": 10, "dv": 4},
    "ML-KEM-768":  {"k": 3, "eta1": 2, "du": 10, "dv": 4},
    "ML-KEM-1024": {"k": 4, "eta1": 2, "du": 11, "dv": 5},
}

with open("pytest/keygen_prompt.json") as f:
    input = json.load(f)

with open("pytest/keygen_expectedResults.json") as f:
    expectedResults = json.load(f)

expected = {}
# 1: {"tcId": 1, "ek": "1CAB...", "dk": "C8D4..."} in expected
for group in expectedResults["testGroups"]:
    for test in group["tests"]:
        expected[test["tcId"]] = test

def test_keygen():
    for group in input["testGroups"]:
        p = k_map[group["parameterSet"]]
        params.k    = p["k"]
        params.eta1 = p["eta1"]
        params.du   = p["du"]
        params.dv   = p["dv"]
        for test in group["tests"]:
            print(test["tcId"], group["parameterSet"])
            z = bytes.fromhex(test["z"])
            d = bytes.fromhex(test["d"])
            ek, dk = kem._keygen_internal(d, z)
            # ek, dk = ML_KEM_512.key_derive(d + z)
            assert ek == bytes.fromhex(expected[test["tcId"]]["ek"]) # expected[key][var]
            assert dk == bytes.fromhex(expected[test["tcId"]]["dk"])
