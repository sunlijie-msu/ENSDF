"""Diagnose guard freshness state and re-seed it for the adopted file."""
import hashlib
import json
import os
import subprocess
import sys

ROOT = r"D:\X\ND\ENSDF"
P = r"A34/S34/new/S34_adopted.ens"
os.chdir(ROOT)
key = os.path.realpath(P)
txt = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
d = hashlib.sha256(txt.encode("utf-8")).hexdigest()

st = json.load(open(r".github/temp/ens_guard/state.json", encoding="utf-8"))
print("before seed: key present:", key in st, "| match:", st.get(key) == d, "| keys:", len(st))

payload = {"tool_name": "read_file", "tool_input": {"filePath": P}, "cwd": ROOT}
r = subprocess.run([sys.executable, r".github/hooks/scripts/guard_ens_edit.py"],
                   input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8")
print("guard seed rc:", r.returncode, "out:", (r.stdout or "").strip()[:160])

st2 = json.load(open(r".github/temp/ens_guard/state.json", encoding="utf-8"))
print("after seed: match:", st2.get(key) == d)
