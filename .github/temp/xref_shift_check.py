"""Compute all K->L, L->M, M->N, N->O XREF shifts in S35_adopted.ens."""
import re
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
last_l_line = None
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if re.match(r" 35S   L ", stripped):
        last_l_line = stripped
    m = re.match(r"( 35S X L XREF=)(\S+)", stripped)
    if not m:
        continue
    prefix, xref_val = m.group(1), m.group(2)
    new_val = shift_xref(xref_val)
    if new_val != xref_val:
        old_line_full = stripped.ljust(80)
        new_line_full = (prefix + new_val).ljust(80)
        changes.append({
            "lineno": i + 1,
            "context_l": last_l_line,
            "old": old_line_full,
            "new": new_line_full,
        })

print(f"Total XREF lines needing changes: {len(changes)}")
print()
for ch in changes:
    print(f"Line {ch['lineno']}:")
    if ch["context_l"]:
        print(f"  L-rec: {ch['context_l']}")
    print(f"  OLD: {ch['old']}")
    print(f"  NEW: {ch['new']}")
    print()
