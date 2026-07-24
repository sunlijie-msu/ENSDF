"""Compute final S34_32s_t_p.ens with compact cL comments, output to temp file."""
import re

with open(r'A34\S34\new\S34_32s_t_p.ens', 'r', encoding='utf-8', newline='') as f:
    raw = f.read()
    # Detect line ending
    if '\r\n' in raw:
        le = '\r\n'
    else:
        le = '\n'
    lines = raw.split(le)

# Compact config strings: e_kev -> [cL_lines]
# Format: "$cfg. N=v1, v2. cfg. N=v1, v2."
def make_cl(e_kev, rows):
    chunks = []
    for cfg, sii, siip in rows:
        if siip:
            chunks.append(f"{cfg}. N={sii}, {siip}.")
        else:
            chunks.append(f"{cfg}. N={sii}.")
    # Split into ~70-char lines
    result = []
    cur = ""
    for c in chunks:
        if not cur:
            cur = "$" + c
        else:
            t = cur + " " + c
            if len(t) <= 72:
                cur = t
            else:
                result.append(cur)
                cur = "$" + c
    if cur:
        result.append(cur)
    # Format with ENSDF prefixes (cols 1-5=NUCID, cols 6-9=prefix, col 10+=text)
    out = []
    nucid = " 34S "
    for j, txt in enumerate(result):
        if j == 0:
            pfx = " cL "  # col6=space, col7=c, col8=L, col9=space
        else:
            cont = str(j+1) if j < 9 else chr(ord('a')+j-9)
            pfx = f"{cont}cL "  # col6=cont, col7=c, col8=L, col9=space
        out.append(f"{nucid}{pfx}{txt}".ljust(80))
    return out

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

# Precompute all cL blocks
cl_blocks = {}
for e_kev, rows in config_data.items():
    cl_blocks[e_kev] = make_cl(e_kev, rows)

# Build new file: iterate through lines, when we see an L-record with config data:
# - If it already has our cL comments after it, skip them (they'll be replaced)
# - Insert new cL after the L-record

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # Check if this is an L-record with config data
    if len(line) >= 19 and line[7] == 'L' and line[8] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                e_int = int(round(float(e_str)))
            except ValueError:
                i += 1
                continue
            
            if e_int in cl_blocks:
                # Skip any existing cL comments we previously added (verbose or compact)
                # Strategy: if the first cL line after L contains our markers (N= or |s{-rel}),
                # skip it and all continuation cL lines until next non-cL line
                skip_count = 0
                found_ours = False
                for k in range(i+1, min(i+20, len(lines))):
                    nxt = lines[k]
                    if len(nxt) < 8: break
                    is_cl = (nxt[6] == 'c' or (len(nxt) > 7 and nxt[7] == 'c'))  # col7='c'
                    # Actually check col7='c' for comment records
                    is_comment = (len(nxt) > 7 and nxt[7] == 'c')
                    if is_comment and ('N=' in nxt or '|s{-rel}' in nxt or found_ours):
                        found_ours = True
                        skip_count += 1
                    elif is_comment and found_ours and nxt[6] != ' ':  # continuation of our block
                        skip_count += 1
                    else:
                        break
                if skip_count > 0:
                    i += skip_count
                
                # Add compact cL
                for cl in cl_blocks[e_int]:
                    new_lines.append(cl)
    
    i += 1

# Write new content
new_content = le.join(new_lines) + le
with open(r'.github\temp\2026-07-24_s34_config\new_content.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(new_content)

print(f"Old: {len(lines)} lines")
print(f"New: {len(new_lines)} lines")
print("Preview of first 20 data lines:")
for i, l in enumerate(new_lines):
    if i >= 13:
        print(f"  {i+1}: [{l.rstrip()}]")
    if i >= 35: break
