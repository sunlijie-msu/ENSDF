"""Find all L-records (col8='L', col6=' ') not exactly 80 chars; report pure-L status."""
import re

P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
bad = 0
for i, ln in enumerate(lines, 1):
    if len(ln) >= 70 and ln[6:7] == " " and ln[7:8] == "L" and len(ln) != 80:
        x = ""
        for k in range(i, min(i + 4, len(lines))):
            if "XREF=" in lines[k]:
                x = lines[k].split("XREF=", 1)[1].strip()
                break
        clean = re.sub(r"\([^)]*\)", "", x).strip()
        bad += 1
        print(f"line {i} len={len(ln)} pureL={int(clean == 'L')} c77={(ln[76:77] if len(ln) > 76 else 'N/A')!r} XREF={x}")
        print("   ", repr(ln))
print("L-records with len!=80:", bad)
