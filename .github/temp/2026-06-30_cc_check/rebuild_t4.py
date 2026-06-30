import re, pathlib, math

raw_path = pathlib.Path("XUNDL/raw.md")
t1_path = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_Table_I.md")
out_path = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md")

# ---------- Parse Table I: float Ei -> (Ei_raw_with_uncertainty, Jpi) ----------
t1_lines = t1_path.read_text(encoding="utf-8").splitlines()
levels_t1 = {}
for line in t1_lines:
    s = line.strip()
    if not s.startswith("|"):
        continue
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) < 9:
        continue
    if cells[0].startswith("$E_i$"):
        continue
    if re.fullmatch(r"[-: ]*", "".join(cells)):
        continue
    ei_m = re.match(r"([\d\.]+)", cells[0])
    if not ei_m:
        continue
    try:
        levels_t1[float(ei_m.group(1))] = (cells[0], cells[1])  # (Ei_raw, Jpi)
    except ValueError:
        pass

def find_level(e_val, tol=2.0):
    """Find closest T1 level within tol. Return (Ei_raw, Jpi, Ei_float) or fallback (str, '', e_val)."""
    best, best_diff = None, float("inf")
    for ei_f, (ei_raw, jpi) in levels_t1.items():
        diff = abs(ei_f - e_val)
        if diff < best_diff:
            best, best_diff = (ei_raw, jpi, ei_f), diff
    if best is not None and best_diff <= tol:
        return best
    # Fallback: raw computed value
    return (f"{e_val:.1f}", "", e_val)

# ---------- Parse raw.md (original 10-column format) ----------
raw_lines = raw_path.read_text(encoding="utf-8").splitlines()
new_lines = []
header_written = False
sep_written = False

for line in raw_lines:
    s = line.strip()
    # Title line
    if s.startswith("###"):
        new_lines.append(line)
        continue
    # Old header
    if (s.startswith("| $E_i$") or s.startswith("| $E_1$")) and "$J_1$" in s:
        new_lines.append("| $E_1$ | $E_{\\gamma1}$ | $E_{\\gamma2}$ | $A_0$ | $A_2$ | $A_4$ | $E_2$ | $E_3$ | $J_1$ | $J_2$ | $J_3$ | $\\delta_1$ |")
        header_written = True
        continue
    # Old separator
    if s.startswith("| :---"):
        new_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        sep_written = True
        continue
    # Non-table lines
    if not s.startswith("|"):
        new_lines.append(line)
        continue
    # Data row: parse 10 columns
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) < 10:
        new_lines.append(line)
        continue
    ei_m = re.match(r"([\d\.]+)", cells[0])
    eg1_m = re.match(r"([\d\.]+)", cells[1])
    eg2_m = re.match(r"([\d\.]+)", cells[2])
    if not (ei_m and eg1_m and eg2_m):
        new_lines.append(line)
        continue
    ei_val = float(ei_m.group(1))
    eg1_val = float(eg1_m.group(1))
    eg2_val = float(eg2_m.group(1))

    # Compute intermediate and final level energies from T1
    e_int = ei_val - eg1_val
    e_fin = ei_val - eg1_val - eg2_val
    e2 = find_level(e_int)
    e3 = find_level(e_fin)

    # Build 12-column row: E1 | Eg1 | Eg2 | A0 | A2 | A4 | E2 | E3 | J1 | J2 | J3 | d1
    new_cells = [
        cells[0],  # E1
        cells[1],  # Eg1
        cells[2],  # Eg2
        cells[3],  # A0
        cells[4],  # A2
        cells[5],  # A4
        e2[0],     # E2 (intermediate level from T1)
        e3[0],     # E3 (final level from T1)
        cells[6],  # J1
        cells[7],  # J2
        cells[8],  # J3
        cells[9],  # d1
    ]
    new_lines.append("| " + " | ".join(new_cells) + " |")

# Verify
assert header_written, "Header not found!"
assert sep_written, "Separator not found!"

out_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
print(f"Done. {len(new_lines)} lines written.")
print(f"Header: {new_lines[1]}")
print(f"Sep:    {new_lines[2]}")
# Print first few data rows for verification
for i, l in enumerate(new_lines[3:8], 4):
    print(f"Row {i}: {l[:120]}...")
# Verify key rows have d1 preserved
print()
print("Verification of key mixing ratios:")
for l in new_lines[3:]:
    if "0.006 (6)" in l or "-2.83 (4)" in l or "4.03 (20)" in l:
        print(f"  OK: {l[:130]}")
