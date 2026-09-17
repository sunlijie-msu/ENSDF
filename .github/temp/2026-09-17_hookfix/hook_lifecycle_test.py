"""Full token-lifecycle regression test for the patched guard/verify hooks.

Expected lifecycle:
  read issues token -> read's verify PRESERVES it -> edit allowed ->
  edit's verify consumes it -> next edit without read is denied with
  "No fresh-read token" (NOT "concurrent edit") -> re-read re-issues ->
  on-disk change produces the "changed on disk" denial.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = r"D:\X\ND\ENSDF"
GUARD = r".github/hooks/scripts/guard_ens_edit.py"
VERIFY = r".github/hooks/scripts/verify_ens_edit.py"
STATE = pathlib.Path(ROOT, ".github/temp/ens_guard/state.json")
DIR = pathlib.Path(ROOT, ".github/temp/2026-09-17_hookfix")
SCRATCH = DIR / "scratch_hooktest.ens"
KEY = str(SCRATCH)

results = []


def check(name, ok, detail=""):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  [{detail}]"))


def run(script, payload):
    p = subprocess.run([sys.executable, script], input=json.dumps(payload),
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    return (p.stdout or "").strip()


def pl(tool, **ti):
    return {"tool_name": tool, "tool_input": ti, "cwd": ROOT}


def state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {}


def disk_sha():
    text = open(SCRATCH, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def reason(out):
    try:
        return json.loads(out)["hookSpecificOutput"].get("permissionDecisionReason", "")
    except Exception:
        return out


# fresh scratch with two 80-char comment lines
line1 = (" 34S  cL SCRATCH COMMENT LINE ONE X1" + " " * 80)[:80]
line2 = (" 34S  cL SCRATCH COMMENT LINE TWO X2" + " " * 80)[:80]
SCRATCH.write_text(line1 + "\n" + line2 + "\n", encoding="utf-8", newline="")

g = run(GUARD, pl("read_file", filePath=KEY))
check("1. read issues token (guard)", state().get(KEY) == disk_sha())

v = run(VERIFY, pl("read_file", filePath=KEY))
check("2. read's verify preserves token", state().get(KEY) == disk_sha(), f"out={v}")

edit = pl("replace_string_in_file", filePath=KEY, oldString="LINE ONE X1", newString="LINE ONE Z1")
g = run(GUARD, edit)
check("3. edit allowed with fresh token", "deny" not in g, g)

v = run(VERIFY, edit)
check("4. edit's verify consumes token", KEY not in state(), f"out={v}")

g = run(GUARD, edit)
r = reason(g)
check("5. re-edit w/o read -> 'No fresh-read token'",
      "No fresh-read token" in r and "changed on disk" not in r, r)

run(GUARD, pl("read_file", filePath=KEY))
# simulate a human/on-disk change AFTER the read
SCRATCH.write_text(line1.replace("X1", "Q9") + "\n" + line2 + "\n", encoding="utf-8", newline="")
g = run(GUARD, edit)
r = reason(g)
check("6. on-disk change -> 'changed on disk'", "changed on disk" in r, r)

run(GUARD, pl("read_file", filePath=KEY))
g = run(GUARD, pl("read/readFile", filePath=KEY))
check("7. read/readFile spelling also issues token", state().get(KEY) == disk_sha())

term = pl("run_in_terminal", command=f"Set-Content -Path {KEY} -Value xx")
g = run(GUARD, term)
check("8. mutating terminal consumes token", KEY not in state(), g)
v = run(VERIFY, term)
check("9. terminal verify clean (no crash)", True, v)

run(GUARD, pl("read_file", filePath=KEY))
multi = pl("multi_replace_string_in_file",
           replacements=[{"filePath": KEY, "oldString": "LINE TWO X2", "newString": "LINE TWO W2"}])
g = run(GUARD, multi)
check("10. multi_replace shape allowed", "deny" not in g, g)
v = run(VERIFY, multi)
check("11. multi_replace verify consumes token", KEY not in state(), f"out={v}")

st = state()
st.pop(KEY, None)
STATE.write_text(json.dumps(st), encoding="utf-8")

fails = [r for r in results if not r[1]]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed")
sys.exit(1 if fails else 0)
