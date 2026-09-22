import re, sys

path = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
with open(path, encoding="utf-8", errors="replace") as f:
    lines = [l.rstrip("\n") for l in f]

blocks = []
cur = None
curg = None
for i, l in enumerate(lines):
    if len(l) < 8:
        continue
    col6 = l[5]
    col7 = l[6]
    col8 = l[7]
    is_plain_L = (col6 == ' ' and col7 == ' ' and col8 == 'L')
    is_plain_G = (col6 == ' ' and col7 == ' ' and col8 == 'G')
    is_cont_L = (col6 not in (' ',) and col7 == ' ' and col8 == 'L')
    is_cont_G = (col6 not in (' ',) and col7 == ' ' and col8 == 'G')
    is_comment_L = (col7 == 'c' or col7=='C') and col8 == 'L'
    is_comment_G = (col7 == 'c' or col7=='C') and col8 == 'G'

    if is_plain_L:
        if cur:
            blocks.append(cur)
        e_field = l[9:19].strip()
        de_field = l[19:21].strip()
        cur = {"lineno": i+1, "line": l, "E": e_field, "DE": de_field, "gammas": [], "cont": [], "comments": []}
        curg = None
    elif cur is not None:
        if is_plain_G:
            e = l[9:19].strip()
            de = l[19:21].strip()
            curg = {"lineno": i+1, "line": l, "E": e, "DE": de}
            cur["gammas"].append(curg)
        elif is_cont_L:
            cur["cont"].append(l)
        elif is_comment_L:
            cur["comments"].append(l)
        elif is_cont_G or is_comment_G:
            pass  # gamma continuation/comment, not needed for level trace

if cur:
    blocks.append(cur)

print(f"Total L blocks: {len(blocks)}")
results = []
for b in blocks:
    xref_str = None
    for c in b["cont"]:
        m = re.search(r'XREF=(\S+)', c)
        if m:
            xref_str = m.group(1)
    n_gam = len(b["gammas"])
    gam_with_unc = sum(1 for g in b["gammas"] if g["DE"])
    results.append({
        "lineno": b["lineno"], "E": b["E"], "DE": b["DE"],
        "n_gam": n_gam, "gam_with_unc": gam_with_unc, "xref": xref_str,
    })
    print(f"Line {b['lineno']}: E={b['E']!r} DE={b['DE']!r} nGam={n_gam} gamWithUnc={gam_with_unc} XREF={xref_str}")

import json
with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\adopted_levels.json", "w") as f:
    json.dump(results, f, indent=1)
