"""Independent re-derivation of ALL multiplet partners per asterisked row.

Reads the source markdown table directly (fresh parser, no imports from the
report generator) and compares the result against section 7 of the report.

Source column order: | E_i | E_gamma | I_gamma | E_f | Jpi_f |
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TBL = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd_Table_II.md")
REP = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd_Multiplet_Gammas.md")
TOL = 1.0
NUM = re.compile(r"^[0-9]")


def num(s):
    s = s.strip()
    if not s:
        return None
    m = re.match(r"^([-+]?[0-9]*\.?[0-9]+)", s)
    return float(m.group(1)) if m else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


rows = []
with open(TBL, encoding="utf-8") as fh:
    for ln, raw in enumerate(fh, 1):
        line = raw.rstrip("\r\n")
        if not line.startswith("|"):
            continue
        c = cells(line)
        if len(c) < 5:
            continue
        eg = c[1]
        if not NUM.match(eg.strip()):
            continue
        rows.append(dict(ln=ln, eg=eg, ig=c[2], ei=c[0], ef=c[3],
                         E=num(eg)))

astro = [r for r in rows if "*" in r["ig"]]
print("source rows parsed: {} | asterisked rows: {}".format(len(rows), len(astro)))

multi = {}
for r in astro:
    part = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    part.sort(key=lambda q: (abs(q["E"] - r["E"]), q["ln"]))
    multi[r["ln"]] = part

hist = {}
for r in astro:
    hist[len(multi[r["ln"]])] = hist.get(len(multi[r["ln"]]), 0) + 1
print("partner-count histogram (partners -> records):", sorted(hist.items()))
print("total pairs: {}".format(sum(len(v) for v in multi.values())))

print("\n--- records with MORE THAN ONE partner ---")
for r in astro:
    p = multi[r["ln"]]
    if len(p) > 1:
        print("row {}  Eg={}  Ig={}  Ei={}".format(r["ln"], r["eg"], r["ig"], r["ei"]))
        for q in p:
            print("    partner row {}  Eg={}  Ig={}  Ei={}  dE={:+.2f}".format(
                q["ln"], q["eg"], q["ig"], q["ei"], q["E"] - r["E"]))

insec = False
sec = []
with open(REP, encoding="utf-8") as fh:
    for ln, raw in enumerate(fh, 1):
        line = raw.rstrip("\r\n")
        if line.startswith("## 7."):
            insec = True
            continue
        if insec and line.startswith("## 8."):
            break
        if insec and line.startswith("|"):
            c = cells(line)
            if c and NUM.match(c[0].strip()):
                sec.append((ln, c))
print("\nsection 7 data rows: {}".format(len(sec)))


def src_tuple(r, q):
    return (r["eg"], r["ig"], r["ei"], r["ef"], q["eg"], q["ig"], q["ei"], q["ef"])


src_pairs = [src_tuple(r, q) for r in astro for q in multi[r["ln"]]]

maxp = 1
rep_pairs = []
print("\nsection 7 columns: {} | rows: {}".format(len(sec[0][1]) if sec else 0, len(sec)))


def expand(c):
    """Split the five stacked partner subcells into 4-tuples."""
    parts = [v.split("<br>") for v in c[5:9]]
    n = len(parts[0])
    if any(len(p) != n for p in parts):
        print("CELL-COUNT MISMATCH", c)
        return []
    return [tuple(p[k] for p in parts) for k in range(n)]


for ln, c in sec:
    for g in expand(c):
        rep_pairs.append(tuple(c[1:5]) + g)
print("expected pairs: {} | report pairs: {}".format(len(src_pairs), len(rep_pairs)))
miss = sorted(p for p in src_pairs if p not in rep_pairs)
extra = sorted(p for p in rep_pairs if p not in src_pairs)
print("missing from report: {} | extra in report: {}".format(len(miss), len(extra)))
for p in miss:
    print("  MISS ", p)
for p in extra:
    print("  EXTRA", p)

print("\n--- per-record expansion check ---")
bad = 0
multirec = 0
for r in astro:
    p = multi[r["ln"]]
    key = (r["eg"], r["ig"], r["ei"], r["ef"])
    hits = [c for _, c in sec if tuple(c[1:5]) == key]
    ngot = sum(len(expand(c)) for c in hits)
    if len(hits) != 1 or ngot != len(p):
        bad += 1
        print("BAD row {}  Eg={:<14} partners={} report rows={} listed={}".format(
            r["ln"], r["eg"], len(p), len(hits), ngot))
    if len(p) > 1:
        multirec += 1
        print("OK  row {}  Eg={:<14} partners={}  {}".format(
            r["ln"], r["eg"], len(p),
            " | ".join(q["eg"].split()[0] for q in p)))
print("two-partner records: {} | rows/expansion mismatches: {}".format(multirec, bad))
print("report rows: {} | asterisked source rows: {}".format(len(sec), len(astro)))
