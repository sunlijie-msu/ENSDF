"""Generate exact multi_replace context strings for all K->L, L->M, M->N, N->O XREF shifts."""
import re
import json
from pathlib import Path


def shift_xref(xref_val):
    shift = {"K": "L", "L": "M", "M": "N", "N": "O"}
    result = ""
    i = 0
    while i < len(xref_val):
        c = xref_val[i]
        if c.isalpha():
            new_c = shift.get(c, c)
            result += new_c
            i += 1
            if i < len(xref_val) and xref_val[i] == "(":
                j = xref_val.index(")", i)
                result += xref_val[i:j+1]
                i = j + 1
        else:
            result += c
            i += 1
    return result


file = Path(r"d:/X/ND/ENSDF/A35/S35/new/S35_adopted.ens")
lines = file.read_text(encoding="latin-1").splitlines()

changes = []
last_l_idx = None
for i, line in enumerate(lines):
    if re.match(r" 35S   L ", line):
        last_l_idx = i
    m = re.match(r"( 35S X L XREF=)(\S+)", line.rstrip())
    if not m:
        continue
    prefix, xref_val = m.group(1), m.group(2)
    new_val = shift_xref(xref_val)
    if new_val != xref_val:
        changes.append({
            "xref_idx": i,
            "l_idx": last_l_idx,
        })

result = []
for ch in changes:
    xi = ch["xref_idx"]
    li = ch["l_idx"]
    # Use: line before L, L-record, old XREF line, line after XREF (4 lines context)
    prev_line = lines[li - 1] if li > 0 else ""
    l_line = lines[li]
    xref_line = lines[xi]
    next_line = lines[xi + 1] if xi + 1 < len(lines) else ""

    xref_stripped = xref_line.rstrip()
    m = re.match(r"( 35S X L XREF=)(\S+)", xref_stripped)
    prefix, xref_val = m.group(1), m.group(2)
    new_val = shift_xref(xref_val)
    new_xref = (prefix + new_val).ljust(80)

    old_str = prev_line + "\n" + l_line + "\n" + xref_line + "\n" + next_line
    new_str = prev_line + "\n" + l_line + "\n" + new_xref + "\n" + next_line

    result.append({
        "xref_lineno": xi + 1,
        "l_lineno": li + 1 if li is not None else None,
        "oldXref": xref_stripped,
        "newXref": new_xref,
        "oldString": old_str,
        "newString": new_str,
    })

print(f"// Total changes: {len(result)}")
print()
for r in result:
    print(f"// Line {r['xref_lineno']} (L-rec at {r['l_lineno']}): {r['oldXref'].strip()} -> {r['newXref'].strip()}")
    print(repr(r["oldString"]))
    print(repr(r["newString"]))
    print()
