import re

# 1. Parse Source Markdown
# Table Row: | Energy (keV) | Intensity (mb) |
# Each row has value(unc) like 95.45(18) or 571.7(6) or 770.428(20) and intensity like 0.012(3) or 2.75(25)
# Some intensities might be like 0.222(26) or 2.75(25)
# Let's extract they: value (uncertainty)
# A regex to match value and uncertainty:
# val_unc_pat = re.compile(r"([0-9\.]+)\s*(?:\(([-+0-9\s]+)\))?")
# Wait, let's trace:
# 95.45(18) -> value 95.45, unc 18
# Let's write a parser function:
def parse_val_unc(text):
    text = text.strip()
    if not text:
        return None, None
    # match something like 95.45(18) or 571.7(6) or 5(3) or 2.75(25)
    # also handle things like 576.80(19) or similar.
    m = re.match(r"^([0-9\.]+)(?:\s*\(([-+0-9\s]+)\))?$", text)
    if m:
        val_str = m.group(1)
        unc_str = m.group(2) if m.group(2) is not None else ""
        return val_str, unc_str
    return None, None

source_rows = []
with open("A34/S34/raw/1985RA15_Table_V.md", "r", encoding="utf-8") as f:
    for line_idx, line in enumerate(f, 1):
        line = line.strip()
        if line.startswith("|") and not ("Energy" in line or "---" in line):
            parts = [p.strip() for p in line.split("|")]
            # parts[0] is empty because line starts with '|', parts[1] is Energy, parts[2] is Intensity, parts[3] is empty
            if len(parts) >= 3:
                e_str, e_unc = parse_val_unc(parts[1])
                ri_str, ri_unc = parse_val_unc(parts[2])
                if e_str is not None:
                    source_rows.append({
                        "line": line_idx,
                        "raw_line": line,
                        "e_str": e_str, "e_unc": e_unc,
                        "ri_str": ri_str, "ri_unc": ri_unc,
                        "e_val": float(e_str),
                        "ri_val": float(ri_str) if ri_str else None
                    })

print("Found source rows:", len(source_rows))
