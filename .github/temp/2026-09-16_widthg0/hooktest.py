"""Test the .ens edit guard against a disposable scratch file (never touches
real ENSDF data): byte-exact anchors, freshness across edit chains, terminal
mutating-command gating, and apply_patch refusal."""
import json
import subprocess
import sys
from pathlib import Path

GUARD = ".github/hooks/scripts/guard_ens_edit.py"
SCRATCH = Path(".github/temp/2026-09-16_widthg0/scratch.ens")
STATE = Path(".github/temp/ens_guard/state.json")

LINES = [f" 34S  cL $Scratch line {i}".ljust(80) for i in range(10)]
VARIANT = " 34S  cL $Scratch LINE 0".ljust(80)


def reset_scratch(lines=LINES):
    SCRATCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(payload):
    p = subprocess.run([sys.executable, GUARD], input=json.dumps(payload), capture_output=True, text=True)
    return p.stdout.strip()


def read_event():
    return run({"tool_name": "read_file", "tool_input": {"filePath": str(SCRATCH)}})


def edit_event(old, new):
    return {"tool_name": "replace_string_in_file",
            "tool_input": {"filePath": str(SCRATCH), "oldString": old, "newString": new}}


def edit_files_event(old, new, tool_name="editFiles"):
    return {"tool_name": tool_name,
            "tool_input": {"files": [{"path": str(SCRATCH),
                                        "edits": [{"oldText": old, "newText": new}]}]}}


def patch_event(old, new):
    patch = ("*** Begin Patch\n"
             f"*** Update File: {SCRATCH.as_posix()}\n"
             "@@\n"
             f"-{old}\n"
             f"+{new}\n"
             "*** End Patch")
    return {"tool_name": "apply_patch", "tool_input": {"input": patch}}


def denied(payload):
    return "deny" in run(payload)


checks = []

reset_scratch()
read_event()
checks.append(("read seeds freshness", STATE.exists()))
checks.append(("nonexistent anchor denied (0 hits)", denied(edit_event("NOPE-NOT-PRESENT", "x"))))
checks.append(("single-space anchor denied (many hits)", denied(edit_event(" ", "  "))))
span_old = "\n".join(LINES[0:9])
checks.append(("span cap denied (9 lines)", denied(edit_event(span_old, span_old))))

# byte-exact anchor allowed; apply it like the real tool would, then chain a
# SECOND edit with NO intervening read_file - must be allowed (state-prediction fix)
checks.append(("byte-exact anchor allowed", not denied(edit_event(LINES[0], VARIANT))))
reset_scratch([VARIANT] + LINES[1:])
checks.append(("chained edit without re-read allowed", not denied(edit_event(VARIANT, LINES[0]))))
reset_scratch()

# editFiles workspace-edit shape must receive the same protection
read_event()
checks.append(("editFiles exact anchor allowed", not denied(edit_files_event(LINES[0], VARIANT))))
reset_scratch([VARIANT] + LINES[1:])
checks.append(("editFiles chained edit allowed", not denied(edit_files_event(VARIANT, LINES[0], "edit/editFiles"))))
reset_scratch()
read_event()
checks.append(("editFiles unanchored .ens edit denied", denied({"tool_name": "editFiles",
    "tool_input": {"files": [{"path": str(SCRATCH), "content": "replacement"}]}})))

# apply_patch is allowed only for one exact cL/cG replacement
reset_scratch()
read_event()
checks.append(("anchored comment apply_patch allowed", not denied(patch_event(LINES[0], VARIANT))))

# concurrent edit: mutate scratch WITHOUT a read_file, then try to edit the old text
read_event()
reset_scratch([VARIANT] + LINES[1:])  # simulates a human edit the guard was never told about
checks.append(("concurrent edit denied", denied(edit_event(LINES[0], VARIANT))))
reset_scratch()
read_event()

# terminal command that rewrites the whole file bypasses anchors entirely
mutate_cmd = f'python .github/scripts/column_calibrate.py "{SCRATCH.as_posix()}" --fix'
term_event = {"tool_name": "run_in_terminal", "tool_input": {"command": mutate_cmd}}
checks.append(("mutating terminal command allowed when fresh", not denied(term_event)))
checks.append(("edit denied right after terminal mutation (state invalidated)", denied(edit_event(LINES[0], VARIANT))))

read_event()
reset_scratch([VARIANT] + LINES[1:])  # concurrent change with no read_file
checks.append(("mutating terminal command denied when stale", denied(term_event)))
reset_scratch()
read_event()

dry_cmd = mutate_cmd + " --dry-run"
checks.append(("--dry-run exempted", not denied({"tool_name": "run_in_terminal", "tool_input": {"command": dry_cmd}})))
ro_cmd = f'python .github/scripts/ensdf_1line_ruler.py --file "{SCRATCH.as_posix()}"'
checks.append(("read-only terminal command allowed", not denied({"tool_name": "run_in_terminal", "tool_input": {"command": ro_cmd}})))

unanchored_patch = {"tool_name": "apply_patch", "tool_input": {"input": f"*** Update File: {SCRATCH.as_posix()}\n@@\n-old\n+new\n"}}
checks.append(("unanchored apply_patch denied", denied(unanchored_patch)))

for name, ok in checks:
    print(("PASS " if ok else "FAIL ") + name)
print("all passed:", all(ok for _, ok in checks))
