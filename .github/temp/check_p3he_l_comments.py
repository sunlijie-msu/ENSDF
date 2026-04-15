"""
Cross-check: adopted cL J$ comments quoting (p,3He) L values
vs. actual L-transfer values in S35_37cl_p_3he.ens

ENSDF column layout (0-indexed Python):
  0-4: NUCID
    5: col6 = continuation marker (blank=first, digit/letter=continuation)
    6: col7 = blank for data; 'c' for comment
    7: col8 = record type ('L','G','B','E','X',etc.)
    8: col9 = blank (readability)
  9+: field data
"""

import re

SRC = r"d:\X\ND\ENSDF\A35\S35\new\S35_37cl_p_3he.ens"
TGT = r"d:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens"

# -----------------------------------------------------------------------
# 1. Parse (p,3He) source: E -> L  (L-field = cols 55:64, 0-indexed)
# -----------------------------------------------------------------------
src_levels = {}  # float(E) -> {'E_str':..., 'L':...}

with open(SRC, "r", encoding="utf-8") as f:
    for line in f:
        if len(line) < 9:
            continue
        col6 = line[5]   # continuation marker (blank = first record)
        col8 = line[7]   # record type
        if col6 == " " and col8 == "L":
            E_str = line[9:19].strip()
            L_str = line[55:64].strip()
            try:
                src_levels[float(E_str)] = {"E_str": E_str, "L": L_str}
            except ValueError:
                pass

print(f"(p,3He) levels parsed: {len(src_levels)}")
for E in sorted(src_levels):
    print(f"  {E:8.1f}  L={src_levels[E]['L']!r}")

# -----------------------------------------------------------------------
# 2. Parse adopted file: find L-records and collect cL J$ blocks
# -----------------------------------------------------------------------
# Build list of adopted L-records with their XREF string and J$ comment text
adopted_blocks = []  # each: {'lineno':int, 'E_str':str, 'E':float, 'XREF':str, 'J_comment':str}

lines = open(TGT, "r", encoding="utf-8").readlines()

cur_block = None

def finish_block():
    if cur_block is not None:
        adopted_blocks.append(cur_block)

i = 0
while i < len(lines):
    line = lines[i]
    if len(line) < 9:
        i += 1
        continue

    col6 = line[5]
    col8 = line[7]

    # New L-record (col6=' ', col8='L')
    if col6 == " " and col8 == "L":
        finish_block()
        E_str = line[9:19].strip()
        try:
            E = float(E_str)
        except ValueError:
            E = None
        cur_block = {
            "lineno": i + 1,
            "E_str": E_str,
            "E": E,
            "XREF": "",
            "J_comment": ""
        }
        i += 1
        continue

    # XREF line (col6='X', col8='L')
    if col6 == "X" and col8 == "L" and cur_block is not None:
        cur_block["XREF"] = line[9:].rstrip()
        i += 1
        continue

    # cL J$ comment line
    # Format: col6=' '|digit/letter, col8='c', col9='L', "J$" somewhere
    if cur_block is not None and col8 == "c" and len(line) > 8 and line[8] == "L":
        # First cL comment
        text = line[9:].rstrip()
        if "J$" in text:
            cur_block["J_comment"] = text
            # Collect continuation lines (2cL, 3cL, etc.)
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if len(nxt) < 9:
                    break
                c6 = nxt[5]
                c8 = nxt[7]
                c9 = nxt[8] if len(nxt) > 8 else ""
                if c8 == "c" and c9 == "L" and c6 != " ":
                    # continuation cL
                    cur_block["J_comment"] += " " + nxt[9:].rstrip()
                    j += 1
                else:
                    break
            i = j
            continue

    # G-record: don't reset cur_block, just skip
    i += 1

finish_block()

print(f"\nAdopted L-blocks parsed: {len(adopted_blocks)}")

# -----------------------------------------------------------------------
# 3. Find adopted blocks whose J$ comment quotes (p,3He)
# -----------------------------------------------------------------------
p3he_re = re.compile(r"\(p,\{?\+?3\}?He\)")
l_val_re = re.compile(r"L=([\(\)\d\+\s,]+?)\s+from\s+3/2\+\s+in\s+\(p,\{?\+?3\}?He\)")

def find_p3he_XREF_E(xref_str):
    """Extract (p,3He) label L energy from XREF string. Returns None if no L."""
    # XREF label for (p,3He) is 'L'
    m = re.search(r"L\(([^)]+)\)", xref_str)
    if m:
        return m.group(1)  # parenthetical energy
    if "L" in xref_str:
        return None  # exact match (no parenthetical)
    return "ABSENT"  # L not in XREF at all

def best_p3he_match(adopted_E, xref_str):
    """Find best matching (p,3He) level for this adopted level."""
    # Check for parenthetical energy in XREF
    m = re.search(r"L\(([^*)]+)\*?\)", xref_str)
    if m:
        try:
            hint_E = float(m.group(1).replace("*",""))
            candidates = [(abs(E - hint_E), E) for E in src_levels]
            candidates.sort()
            if candidates and candidates[0][0] < 20:
                return src_levels[candidates[0][1]]
        except ValueError:
            pass
    # Use adopted_E with tolerance
    if adopted_E is not None:
        candidates = [(abs(E - adopted_E), E) for E in src_levels]
        candidates.sort()
        if candidates and candidates[0][0] < 25:
            return src_levels[candidates[0][1]]
    return None

print("\n" + "="*80)
print("Adopted cL J$ comments quoting (p,3He) L — cross-check vs source")
print("="*80)

rows = []
for blk in adopted_blocks:
    j_cmt = blk["J_comment"]
    if not p3he_re.search(j_cmt):
        continue
    # Extract quoted L value
    m = l_val_re.search(j_cmt)
    quoted_L = m.group(1).strip() if m else "?? not parsed"

    # Match to source level
    has_L_in_xref = "L" in blk["XREF"]
    src_match = best_p3he_match(blk["E"], blk["XREF"]) if has_L_in_xref else None
    src_L = src_match["L"] if src_match else "NO MATCH"
    src_E = src_match["E_str"] if src_match else "—"

    status = "PASS" if (src_L and quoted_L == src_L) else "FAIL"

    rows.append({
        "line": blk["lineno"],
        "adopted_E": blk["E_str"],
        "xref": blk["XREF"][:35],
        "quoted_L": quoted_L,
        "src_E": src_E,
        "src_L": src_L,
        "status": status,
    })

    print(f"\n  Adopted {blk['E_str']:>12} keV  [line {blk['lineno']}]")
    print(f"  XREF: {blk['XREF'][:50]}")
    print(f"  J$ quoted L     : {quoted_L!r}")
    print(f"  Source (p,3He)  : E={src_E}  L={src_L!r}")
    print(f"  => {status}")

print("\n" + "="*80)
passes = sum(1 for r in rows if r["status"] == "PASS")
fails = sum(1 for r in rows if r["status"] == "FAIL")
print(f"TOTAL: {len(rows)} J$ (p,3He) comments  |  PASS: {passes}  |  FAIL: {fails}")

# Spot-check: 15% = at least 2
import random
random.seed(42)
sample = random.sample(rows, max(2, len(rows) // 7))
print("\n--- Random 15% Spot-Check ---")
for r in sample:
    print(f"  Adopted {r['adopted_E']:>10}  quoted={r['quoted_L']!r}  src={r['src_L']!r}  {r['status']}")
