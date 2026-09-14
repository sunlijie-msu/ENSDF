#!/usr/bin/env python3
"""Audit: verify that git diff changes are COMMENT records only.

ENSDF comment record: column 7 (1-based) is NON-blank (e.g. 'c').
ENSDF data record:    column 7 is BLANK.

Parses `git diff -U0` for the target file and reports every changed
(added or removed) line whose column 7 is BLANK -> DATA record = violation.
"""
import re
import subprocess
import sys

TARGET = "A34/S34/new/S34_adopted.ens"
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def main():
    repo = r"d:\X\ND\ENSDF"
    out = subprocess.run(
        ["git", "diff", "-U0", "--", TARGET],
        cwd=repo, capture_output=True, text=True,
    )
    if out.returncode != 0:
        print("git diff failed:", out.stderr)
        sys.exit(2)
    diff = out.stdout

    old_ln = new_ln = None
    violations = []   # (side, line_no_side, side_label, raw)
    comments = []
    for rawline in diff.splitlines():
        m = HUNK_RE.match(rawline)
        if m:
            old_ln = int(m.group(1))
            new_ln = int(m.group(3))
            continue
        if rawline.startswith("+++") or rawline.startswith("---"):
            continue
        if rawline.startswith("+"):
            content = rawline[1:]
            col7_blank = len(content) < 7 or content[6] == " "
            rec = ("NEW", new_ln, content)
            (violations if col7_blank else comments).append(rec)
            if new_ln is not None:
                new_ln += 1
        elif rawline.startswith("-"):
            content = rawline[1:]
            col7_blank = len(content) < 7 or content[6] == " "
            rec = ("OLD", old_ln, content)
            (violations if col7_blank else comments).append(rec)
            if old_ln is not None:
                old_ln += 1

    print("TARGET FILE      :", TARGET)
    print("COMMENT changes  :", len(comments))
    print("DATA changes     :", len(violations), "  <-- must be 0")
    print()
    print("=== First 20 DATA-record changes (col 7 BLANK) ===")
    for side, ln, content in violations[:20]:
        print(f"  [{side} L{ln}] col7=blank len={len(content)} :: {content!r}")
    if not violations:
        print("  (none)")
    print()
    print("=== First 10 COMMENT changes (col 7 non-blank) ===")
    for side, ln, content in comments[:10]:
        c7 = content[6] if len(content) >= 7 else "<short>"
        print(f"  [{side} L{ln}] col7={c7!r} :: {content!r}")
    print()
    print("RESULT:", "PASS" if not violations else "FAIL")


if __name__ == "__main__":
    main()
