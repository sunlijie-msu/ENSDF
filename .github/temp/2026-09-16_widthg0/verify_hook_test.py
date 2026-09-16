"""Test verify_ens_edit.py (PostToolUse) against the disposable scratch file:
ASCII check, ruler skip-on-comment-only, and terminal-command path detection.
Never touches real ENSDF data."""
import json
import subprocess
import sys
from pathlib import Path

VERIFY = ".github/hooks/scripts/verify_ens_edit.py"
SCRATCH = Path(".github/temp/2026-09-16_widthg0/scratch.ens")

# scratch.ens: line 0 is a comment (col7='c'), line 1 is a plain data-like line
COMMENT_LINE = " 34S  cL $Scratch comment".ljust(80)
DATA_LINE = " 34S   L 1234.5    12 3/2+".ljust(80)
BAD_LEN_LINE = " 34S   L short"  # deliberately not 80 chars -> ruler should flag it
NONASCII_LINE = (" 34S  cL $bad\u2212value").ljust(80)


def reset_scratch(l1=DATA_LINE):
    SCRATCH.write_text(COMMENT_LINE + "\n" + l1 + "\n", encoding="utf-8")


def run(payload):
    p = subprocess.run([sys.executable, VERIFY], input=json.dumps(payload), capture_output=True, text=True)
    return p.stdout.strip()


def edit_payload(old, new):
    return {"tool_name": "replace_string_in_file",
            "tool_input": {"filePath": str(SCRATCH), "oldString": old, "newString": new},
            "cwd": r"D:\X\ND\ENSDF"}


checks = []

# 1. comment-only edit on a file with a BAD (short) data line elsewhere -> ruler must be SKIPPED
reset_scratch(BAD_LEN_LINE)
out = run(edit_payload(COMMENT_LINE, COMMENT_LINE.replace("Scratch", "Edited")))
checks.append(("comment-only edit skips ruler despite bad data line elsewhere", out == "{}" or out == ""))

# 2. data-record edit on the SAME bad-line file -> ruler must RUN and BLOCK
reset_scratch(BAD_LEN_LINE)
out = run(edit_payload(BAD_LEN_LINE, BAD_LEN_LINE + "x"))
checks.append(("data edit triggers ruler and blocks on bad-length line", '"decision": "block"' in out))

# 3. clean file, clean data edit -> ruler runs and PASSES
reset_scratch(DATA_LINE)
out = run(edit_payload(DATA_LINE, DATA_LINE))
checks.append(("clean data edit passes ruler", out in ("{}", "")))

# 4. ASCII violation always blocks, even declared as comment-only
# (PostToolUse fires AFTER the real write, so the test must apply the edit to
# disk first — validate_ens_ascii reads the file, not the payload strings)
reset_scratch(DATA_LINE)
SCRATCH.write_text(NONASCII_LINE + "\n" + DATA_LINE + "\n", encoding="utf-8")
out = run(edit_payload(COMMENT_LINE, NONASCII_LINE))
checks.append(("non-ASCII comment edit blocked", '"decision": "block"' in out and "ASCII" in out))

# 5. mutating terminal command referencing scratch.ens -> path detected, validated (clean -> passes)
reset_scratch(DATA_LINE)
term_payload = {"tool_name": "run_in_terminal",
                "tool_input": {"command": f'python .github/scripts/column_calibrate.py "{SCRATCH.as_posix()}" --fix'},
                "cwd": r"D:\X\ND\ENSDF"}
checks.append(("mutating terminal command on clean file passes", run(term_payload) in ("{}", "")))

# 6. mutating terminal command referencing a BAD file -> path detected, ruler runs, blocks
reset_scratch(BAD_LEN_LINE)
checks.append(("mutating terminal command on bad file blocks", '"decision": "block"' in run(term_payload)))

# 7. read-only terminal command -> no path extracted -> no-op
reset_scratch(BAD_LEN_LINE)
ro_payload = {"tool_name": "run_in_terminal",
              "tool_input": {"command": f'python .github/scripts/ensdf_1line_ruler.py --file "{SCRATCH.as_posix()}"'},
              "cwd": r"D:\X\ND\ENSDF"}
checks.append(("read-only terminal command is a no-op", run(ro_payload) in ("{}", "")))

reset_scratch()

for name, ok in checks:
    print(("PASS " if ok else "FAIL ") + name)
print("all passed:", all(ok for _, ok in checks))
