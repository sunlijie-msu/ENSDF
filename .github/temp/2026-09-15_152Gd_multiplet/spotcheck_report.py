"""Independent 15% spot check of the multiplet report table against Table II and the .ens target."""
import re

AST = "\u2217"
MD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Multiplet_Gammas.md"
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = r"D:\X\ND\ENSDF\.github\temp\2026-09-15_152Gd_multiplet\spotcheck_report.txt"
OUT2 = r"D:\X\ND\ENSDF\.github\temp\2026-09-15_152Gd_multiplet\spotcheck_report_encoded.txt"

rep = [l.rstrip("\r") for l in open(MD, encoding="utf-8")]
src = [l.rstrip("\r") for l in open(SRC, encoding="utf-8")]
ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]

tbl = {}
for l in rep:
    m = re.match(r"\| (\d+) \| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| ([\d/]+) \| `(.)` \| ([A-D]) \| (.*?) \|$", l)
    if m:
        tbl[int(m.group(1))] = dict(ln=int(m.group(2)), ei=m.group(3), eg=m.group(4), ig=m.group(5),
                                    ef=m.group(6), ens=m.group(7), flag=m.group(8), cls=m.group(9))
assert len(tbl) == 53, len(tbl)

sample = [1, 8, 16, 23, 31, 38, 46, 53]  # deterministic 15% sample (8 of 53)
fail = []
enc = []
for k in sample:
    x = tbl[k]
    s = src[x["ln"] - 1]
    c = [f.strip() for f in s.strip("|").split("|")]
    # (a) source row: line number, Ei, Eg, Ig(asterisked), Ef  -- text compared after stripping the asterisk
    ok_src = (c[0] == x["ei"] and c[1] == x["eg"] and c[2].replace(AST, "").strip() == x["ig"]
              and c[3] == x["ef"] and AST in c[2])
    # (b) target record: line, NUCID/type, E field, RI+DRI field, column 77
    for ln in x["ens"].split("/"):
        e = ens[int(ln) - 1].ljust(80)
        eg_val, eg_unc = re.match(r"(-?\d+(?:\.\d+)?)\s*\((\d+)\)", x["eg"]).groups()
        ig_val, ig_unc = re.match(r"([\d.]+)\s*\((\d+)\)", x["ig"]).groups()
        same_eg = [t for t in tbl.values()
                   if abs(float(re.match(r"-?\d+(?:\.\d+)?", t["eg"]).group(0)) - float(eg_val)) < 0.005]
        uncs = {re.match(r"(-?\d+(?:\.\d+)?)\s*\((\d+)\)", t["eg"]).group(2) for t in same_eg}
        ok_ens = (e[5] == " " and e[6] == " " and e[7] == "G" and e[9:19].strip() == eg_val
                  and e[19:21].strip() in uncs and e[22:29].strip() == ig_val
                  and e[29:31].strip() == ig_unc and e[76] == x["flag"])
        # (c) parent level energy: target = Ei (offset 0.00) or Ei - 0.01 (GLSC refit);
        #     3271.97 -> 3271.73; class-A twin lines sit under the twin row's parent level
        j = int(ln) - 1
        while not (ens[j].ljust(80)[5] == " " and ens[j].ljust(80)[7] == "L"):
            j -= 1
        lvl = float(ens[j].ljust(80)[9:19])
        bases = []
        for t in same_eg:
            bases.append(float(re.match(r"-?\d+(?:\.\d+)?", t["ei"]).group(0)))
        if any(abs(b - 3271.97) < 0.02 for b in bases):
            bases.append(3271.73)
        ok_lvl = any(min(abs(lvl - b), abs(lvl - b + 0.01), abs(lvl - b + 0.02)) < 0.005 for b in bases)
        if not (ok_src and ok_ens and ok_lvl):
            fail.append((k, ok_src, ok_ens, ok_lvl, repr(s), repr(ens[int(ln) - 1][:80]),
                         repr(ens[j][:80]), x))
        enc.append("row {:<3} src line {:<4} ens line {:<9} E_lvl {:<10} flag {!r} | {} {} {}".format(
            k, x["ln"], x["ens"], lvl, e[76], "SRC-OK" if ok_src else "SRC-FAIL",
            "ENS-OK" if ok_ens else "ENS-FAIL", "LVL-OK" if ok_lvl else "LVL-FAIL"))

# (d) reverse: every flagged target G-record must appear in the report
flagged = []
for i, raw in enumerate(ens, 1):
    e = raw.ljust(80)
    if e[5] == " " and e[6] == " " and e[7] == "G" and e[76] in "*&@":
        flagged.append((i, e[76]))
rep_lines = {int(l) for x in tbl.values() for l in x["ens"].split("/")}
rev_fail = [(i, f) for i, f in flagged if i not in rep_lines]
print("flagged G-records in target:", len(flagged), "| distinct flag chars:", sorted({f for _, f in flagged}))
print("report ens lines:", len(rep_lines), "| reverse-check misses:", rev_fail)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("sample rows: {}\n".format(sample))
    fh.write("\n".join(enc) + "\n")
    fh.write("failures: {}\n".format(len(fail)))
    for f in fail:
        fh.write("  {}\n".format(f))
    fh.write("\nflagged G-records: {} distinct flags {}\n".format(len(flagged), sorted({f for _, f in flagged})))
    fh.write("report ens lines: {} reverse misses: {}\n".format(len(rep_lines), rev_fail))
# ASCII-escaped copy so the console can print it under the GBK code page
with open(OUT2, "w", encoding="ascii") as fh:
    fh.write("\n".join(l.encode("ascii", "backslashreplace").decode("ascii")
                       for l in open(OUT, encoding="utf-8").read().split("\n")))
print("failures:", len(fail))
