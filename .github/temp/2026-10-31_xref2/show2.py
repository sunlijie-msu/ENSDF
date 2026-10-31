import io, re
t = io.open(r".github/temp/2026-10-31_xref2/report2.md", encoding="utf-8").read()
sec = {}
for blk in t.split("### ")[1:]:
    head, _, body = blk.partition("\n")
    sec[head.split(" (")[0]] = [l for l in body.split("\n") if l.startswith("|")]
for k in ["NO-OWN-LEVEL", "UNCLAIMED-LEVEL", "SWAPPED", "SHARED-NO-STAR", "FAR-PIN", "STAR-ONCE", "UNCITED-LEVEL", "MISSING-ADOPTED", "MALFORMED"]:
    print("\n##", k, len(sec.get(k, [])))
    for l in sec.get(k, []): print(l[:240])
print("\n## J-CONFLICT undocumented vs documented")
und = [l for l in sec["J-CONFLICT"] if "UNDOCUMENTED" in l]
print(len(und), "undocumented of", len(sec["J-CONFLICT"]))
for l in und: print(l[:200])
print("\n## cases the user named")
for pat in ["9336", "6854", "6844", "9327.3"]:
    for k, rows in sec.items():
        for l in rows:
            if pat in l: print(k, "|", l[:200])
