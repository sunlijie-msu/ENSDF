import re

REP = r".github\temp\quoted_check\report_fresh.txt"
ENS = r"A34\S34\new\S34_adopted.ens"
OUT = r".github\temp\quoted_check\inspect.txt"

raw = open(REP, encoding="utf-8", errors="replace").read()
raw = re.sub(r"\x1b\[[0-9;]*m", "", raw)

findings = []
cur = None
for ln in raw.splitlines():
    m = re.match(r"\s*#(\d+) \[(\w+)\]\s+line (\d+)", ln)
    if m:
        cur = {"id": int(m.group(1)), "type": m.group(2), "line": int(m.group(3)), "quoted": None, "actual": None, "context": ""}
        findings.append(cur)
        continue
    if cur is None:
        continue
    m = re.match(r'\s*Quoted "([^"]+)" keV, [GL]-record has "([^"]+)" keV', ln)
    if m:
        cur["quoted"], cur["actual"] = m.group(1), m.group(2)
        continue
    m = re.match(r'\s*Quoted "([^"]+)" keV, No G-record', ln)
    if m:
        cur["quoted"] = m.group(1)
        continue
    m = re.match(r"\s*No [GL]-record within [\d.]+ keV of ([\d.]+) keV", ln)
    if m:
        cur["quoted"] = m.group(1)
        continue
    m = re.match(r'\s*Quoted J-pi "([^"]+)", L-record J field is "([^"]+)"', ln)
    if m:
        cur["quoted"], cur["actual"] = m.group(1), m.group(2)
        continue
    m = re.match(r'\s*Quoted "([^"]+)", G-record M field is "([^"]+)"', ln)
    if m:
        cur["quoted"], cur["actual"] = m.group(1), m.group(2)
        continue
    m = re.match(r"\s*Context: (.*)", ln)
    if m:
        cur["context"] = m.group(1).strip()

lines = open(ENS, encoding="ascii", errors="replace").read().splitlines()

L = []
G = []
for i, ln in enumerate(lines, 1):
    if len(ln) > 8 and ln[5] == " " and ln[7] == "L":
        e = ln[9:19].strip()
        j = ln[22:39].strip() or ln[21:39].strip()
        if re.match(r"^\d+(\.\d+)?$", e):
            L.append((i, e, float(e), j))
    if len(ln) > 8 and ln[5] == " " and ln[7] == "G":
        e = ln[9:19].strip()
        mf = ln[32:41].strip() or ln[31:41].strip()
        if re.match(r"^\d+(\.\d+)?$", e):
            G.append((i, e, float(e), mf))


def nearest(pool, val, n=3):
    return sorted(pool, key=lambda r: abs(r[2] - val))[:n]


def block(lno):
    idx = lno - 1
    s = idx
    while s - 1 >= 0 and len(lines[s - 1]) > 6 and lines[s - 1][6] == "c":
        s -= 1
    e = idx
    while e + 1 < len(lines) and len(lines[e + 1]) > 6 and lines[e + 1][6] == "c":
        e += 1
    return ["%5d|%s|" % (k + 1, lines[k]) for k in range(s, e + 1)]


out = []
for f in findings:
    out.append("=" * 88)
    out.append("#%d [%s] line %d  quoted=%s actual=%s" % (f["id"], f["type"], f["line"], f["quoted"], f["actual"]))
    out.append("  ctx: %s" % f["context"])
    if f["quoted"] is not None and re.match(r"^[\d.]+$", f["quoted"]):
        val = float(f["quoted"])
        if f["type"].startswith("GAMMA"):
            for r in nearest(G, val):
                par = [x for x in L if x[0] < r[0]]
                out.append("   G? line %d E=%-9s M=%-8s (dE=%+.3f) parent=%s %s"
                           % (r[0], r[1], r[3], r[2] - val, par[-1][1] if par else "?", par[-1][3] if par else ""))
        elif f["type"].startswith("LEVEL"):
            for r in nearest(L, val):
                out.append("   L? line %d E=%-9s J=%-10s (dE=%+.3f)" % (r[0], r[1], r[3], r[2] - val))
    for b in block(f["line"]):
        out.append("  " + b)

open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("findings=%d lines=%d" % (len(findings), len(out)))
