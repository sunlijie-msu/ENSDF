"""Inspect the 20 pre-existing short/long L lines: level, XREF, pure-L?, flag state."""
import re

P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
probe = [785, 789, 826, 836, 851, 861, 885, 888, 940, 947, 987, 995, 1071, 1077,
         1099, 1106, 1107, 1112, 1115, 1129]
for n in probe:
    ln = lines[n - 1]
    xref = lines[n] if "XREF=" in lines[n] else ""
    if not xref:
        for k in range(n, min(n + 4, len(lines))):
            if "XREF=" in lines[k]:
                xref = lines[k]
                break
    x = xref.split("XREF=", 1)[1].strip() if xref else ""
    clean = re.sub(r"\([^)]*\)", "", x).strip()
    flag = ln[76:77] if len(ln) > 76 else "N/A"
    print(f"line {n:5d} len={len(ln):3d} type={ln[6:9]!r} pureL={int(clean == 'L')} c77={flag!r} XREF={x}")
    print(f"      {ln!r}")
