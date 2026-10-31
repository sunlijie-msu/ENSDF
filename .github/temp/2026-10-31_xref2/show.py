import io, re
t = io.open(r".github/temp/2026-10-31_xref2/report.md", encoding="utf-8").read()
sec = {}
for blk in t.split("### ")[1:]:
    head, _, body = blk.partition("\n")
    sec[head.split(" (")[0]] = [l for l in body.split("\n") if l.startswith("|")]
for k in ["NO-OWN-LEVEL", "UNCLAIMED-LEVEL", "SWAPPED", "SHARED-NO-STAR", "STAR-ONCE", "PHANTOM-ENERGY", "FAR-PIN",
          "J-CONFLICT", "UNCITED-LEVEL", "MALFORMED"]:
    print("\n##", k, len(sec.get(k, [])))
    for l in sec.get(k, []):
        print(l[:230])
mp = sec.get("MISSING-PARENTHETICAL", [])
print("\n## MISSING-PARENTHETICAL by letter:")
from collections import Counter
print(Counter(l.split("|")[1].strip() for l in mp).most_common())
print("\nlargest dE:")
rows = []
for l in mp:
    m = re.search(r"dE=([0-9.]+)", l)
    if m: rows.append((float(m.group(1)), l))
for d, l in sorted(rows, reverse=True)[:12]:
    print(l[:200])
print("\nMISSING-ADOPTED:")
for l in sec.get("MISSING-ADOPTED", []): print(l[:200])
