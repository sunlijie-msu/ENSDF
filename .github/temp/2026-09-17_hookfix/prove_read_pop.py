"""Confirm: does the read's own PostToolUse verify pop the token just issued?

Simulates the real call order for a single read_file call:
  PreToolUse  guard_ens_edit.py   (issues token)
  [read happens]
  PostToolUse verify_ens_edit.py  (current code: collect paths -> pop)
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

ROOT = r"D:\X\ND\ENSDF"
GUARD = r".github/hooks/scripts/guard_ens_edit.py"
VERIFY = r".github/hooks/scripts/verify_ens_edit.py"
STATE_PATH = pathlib.Path(ROOT, ".github/temp/ens_guard/state.json")
SCRATCH_DIR = pathlib.Path(ROOT, ".github/temp/2026-09-17_hookfix")
SCRATCH = SCRATCH_DIR / "scratch_hooktest.ens"

SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
line1 = (" 34S  cL SCRATCH COMMENT LINE ONE X1" + " " * 80)[:80]
line2 = (" 34S  cL SCRATCH COMMENT LINE TWO X2" + " " * 80)[:80]
SCRATCH.write_text(line1 + "\n" + line2 + "\n", encoding="utf-8", newline="")

def run(script, payload):
    return subprocess.run([sys.executable, script], input=json.dumps(payload),
                          capture_output=True, text=True, encoding="utf-8", cwd=ROOT).stdout.strip()

def payload(tool, **ti):
    return {"tool_name": tool, "tool_input": ti, "cwd": ROOT}

key = str(SCRATCH)
def state():
    try:
        return json.load(open(STATE_PATH, encoding="utf-8"))
    except Exception:
        return {}

# 1. PreToolUse(read_file) -> token issued
print("guard(read_file) ->", run(GUARD, payload("read_file", filePath=key)) or "{}")
print("  token present after guard:", key in state())

# 2. PostToolUse(read_file) -> does it pop the token?
print("verify(read_file) ->", run(VERIFY, payload("read_file", filePath=key)) or "{}")
print("  token present after verify:", key in state(), "  <-- pre-fix: False (BUG)")

# 3. cleanup
st = state()
st.pop(key, None)
STATE_PATH.write_text(json.dumps(st), encoding="utf-8")
