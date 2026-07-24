"""Generate compact cL comments and apply via targeted replacements."""
import re

with open(r'A34\S34\new\S34_32s_t_p.ens', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Compact config data: e_kev -> [(config, sii, siip), ...]
# From earlier parse
config_data = {
    0: [("(d{-3/2}){+2}", "100", "100"), ("(s{-1/2}){+2}", "13.8", "13.0")],
    2128: [("(d{-3/2}){+2}", "11.8", "11.5"), ("d{-3/2},s{-1/2}", "1.62", "1.52")],
    3308: [("(d{-3/2}){+2}", "9.12", "8.79"), ("d{-3/2},s{-1/2}", "1.18", "1.12")],
    3915: [("(d{-3/2}){+2}", "3.62", "3.33"), ("(s{-1/2}){+2}", "0.48", "0.42"), ("(f{-7/2}){+2}", "1.75", "2.18")],
    4121: [("(d{-3/2}){+2}", "4.50", "4.24"), ("d{-3/2},s{-1/2}", "0.59", "0.53"), ("(f{-7/2}){+2}", "2.25", "2.61")],
    4623: [("d{-3/2},f{-7/2}", "33.8", "33.3"), ("d{-3/2},p{-3/2}", "2.62", "2.67")],
    4690: [("(f{-7/2}){+2}", "2.00", "1.88"), ("d{-3/2},f{-7/2}", "0.48", "0.48")],
    4888: [("(d{-3/2}){+2}", "3.50", "3.30"), ("(f{-7/2}){+2}", "1.88", "1.88")],
    5225: [("(d{-3/2}){+2}", "5.38", "4.85"), ("(f{-7/2}){+2}", "3.38", "3.64"), ("(p{-3/2}){+2}", "0.29", "0.28")],
    5679: [("d{-3/2},p{-3/2}", "3.25", "3.18"), ("d{-3/2},f{-7/2}", "2.12", "2.18")],
    5759: [("d{-3/2},p{-3/2}", "9.38", "8.18")],
    5859: [("(f{-7/2}){+2}", "15.0", "")],
    6008: [("(f{-7/2}){+2}", "33.75", "33.33"), ("(p{-3/2}){+2}", "3.75", "3.03")],
    6128: [("(f{-7/2}){+2}", "7.75", "7.88")],
    6179: [("d{-3/2},p{-3/2}", "0.22", "0.21"), ("d{-3/2},f{-7/2}", "3.12", "2.73")],
    6349: [("d{-3/2},p{-3/2}", "6.38", "5.76")],
    6828: [("(f{-7/2}){+2}", "4.25", "4.55"), ("(p{-3/2}){+2}", "0.36", "")],
    7112: [("d{-3/2},f{-7/2}", "11.25", "10.00"), ("d{-3/2},p{-3/2}", "0.78", "0.67"), ("(f{-7/2}){+2}", "6.50", "6.67"), ("(p{-3/2}){+2}", "0.62", "0.55")],
    7245: [("d{-3/2},f{-7/2}", "22.50", "20.61"), ("d{-3/2},p{-3/2}", "1.62", "1.52")],
    7621: [("d{-3/2},f{-7/2}", "23.75", "23.03"), ("d{-3/2},p{-3/2}", "1.88", "1.61")],
    7739: [("(f{-7/2}){+2}", "4.75", "5.15"), ("(p{-3/2}){+2}", "0.48", "0.39")],
    7801: [("((f{-7/2}){+2}", "20.62", "")],
    8025: [("(p{-3/2}){+2}", "0.56", "")],
    8255: [("(f{-7/2}){+2}", "5.12", "5.15"), ("(p{-3/2}){+2}", "0.49", "0.36"), ("d{-3/2},p{-3/2}", "0.62", "0.52"), ("d{-3/2},f{-7/2}", "8.75", "4.24")],
    8293: [("(f{-7/2}){+2}", "4.75", "4.85"), ("d{-3/2},f{-7/2}", "1.12", "1.30")],
    8383: [("d{-3/2},p{-3/2}", "8.38", "")],
    8418: [("(f{-7/2}){+2}", "11.25", "")],
    8496: [("d{-3/2},p{-3/2}", "12.25", "")],
}

def build_compact_cl(rows):
    """Build compact cL comment lines."""
    parts = []
    for cfg, sii, siip in rows:
        if siip:
            parts.append(f"{cfg}. N={sii}, {siip}")
        else:
            parts.append(f"{cfg}. N={sii}")
    
    # Split into lines: each line can hold ~2-3 configs
    lines = []
    current = "$"
    for p in parts:
        candidate = current + " " + p + "."
        if len(candidate) > 72:  # " 34S  cL " = 9 chars, so ~71 chars for text
            # Check if just adding " " + p (without trailing dot on previous) works
            if current != "$":
                lines.append(current.rstrip() + ".")
                current = "$" + p
            else:
                # Single config too long for one line? Use it anyway
                lines.append("$" + p + ".")
                current = "$"
        else:
            if current == "$":
                current = "$" + p
            else:
                current = current + " " + p
    
    if current != "$":
        lines.append(current + ".")
    
    return lines

# Build compact cL text for each level
compact_map = {}
for e_kev, rows in sorted(config_data.items()):
    clines = build_compact_cl(rows)
    compact_map[e_kev] = clines
    print(f"E={e_kev}:")
    for cl in clines:
        print(f"  [{cl}]")

# Find L-record line indices
l_indices = {}
for i, line in enumerate(lines):
    if len(line) >= 19 and line[7] == 'L' and line[8] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                e_int = int(round(float(e_str)))
                l_indices[e_int] = i
            except ValueError:
                pass

print(f"\nFound {len(l_indices)} L-records")
