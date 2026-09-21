"""Read-only audit: pair each G record with its own comment block
(cG / continuation cG lines, 2 G / F G continuation records) and classify the
M field (cols 33-41) against the evidence tokens stated in that comment.

Column map (1-based): 1-5 NUCID, 6 CONT, 7 c/space, 8 TYPE,
G: E 10-19, DE 20-21, RI 23-29, DRI 30-31, M 33-41, MR 42-49, DMR 50-55,
   CC 56-62, DCC 63-64, TI 65-74, DTI 75-76, flag 77, 78-79, Q 80.
L: E 10-19, DE 20-21, J 23-39, T 40-49, DT 50-55.
"""
import re

PATH = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
OUT = r"d:\X\ND\ENSDF\.github\temp\2026-09-21_mfield-parens-scan\final_mfield_table.txt"

lines = [l.rstrip("\n") for l in open(PATH, encoding="ascii").read().split("\n")]

recs = []
curL = None
for i, raw in enumerate(lines, 1):
    if len(raw) < 10:
        continue
    cont = raw[5]
    col7 = raw[6]
    typ = raw[7]
    if typ in ("L", "G") and col7 == " ":
        if cont == " ":
            rec = {"kind": typ, "line": i, "raw": raw, "cmt": [],
                   "fl": [], "level": curL if typ == "G" else None}
            if typ == "L":
                curL = rec
            recs.append(rec)
        else:
            tgt = next((r for r in reversed(recs) if r["kind"] == typ), None)
            if tgt:
                tgt["fl"].append(raw)
    elif typ in ("L", "G") and col7 == "c":
        tgt = next((r for r in reversed(recs) if r["kind"] == typ), None)
        if tgt:
            tgt["cmt"].append(raw)

rows = []
for r in recs:
    if r["kind"] != "G":
        continue
    raw = r["raw"]
    e = raw[9:19].strip()
    de = raw[19:21].strip()
    ri = raw[22:29].strip()
    dri = raw[29:31].strip()
    m = raw[32:41].strip()
    mr = raw[41:49].strip()
    dmr = raw[49:55].strip()
    flag = raw[76] if len(raw) > 76 else " "
    q = raw[79] if len(raw) > 79 else " "
    lv = jpi = lt = ""
    if r["level"] is not None:
        L = r["level"]["raw"]
        lv = L[9:19].strip() + L[19:21].strip()
        jpi = L[22:39].strip()
        lt = (L[39:49].strip() + " " + L[49:55].strip()).strip()
    ctext = " ".join(c[8:].strip() for c in r["cmt"])
    fltxt = " ".join(x[8:].strip() for x in r["fl"])
    tok = []
    if re.search(r"\bRUL\b", ctext):
        tok.append("RUL")
    if "POL" in ctext:
        tok.append("POL")
    if "azimuthal" in ctext:
        tok.append("AZ")
    if "ADO" in ctext:
        tok.append("ADO")
    if "level scheme" in ctext:
        tok.append("LS")
    if "resonances" in ctext:
        tok.append("RES")
    if "|g(|q)" in ctext:
        tok.append("gth")
    if "|g|g(|q)" in ctext:
        tok.append("ggth")
    klass = ("paren" if m.startswith("(") else
             "bracket" if m.startswith("[") else
             "firm" if m else "empty")
    rows.append(dict(line=r["line"], e=e, de=de, ri=ri, dri=dri, m=m, mr=mr,
                     dmr=dmr, flag=flag, q=q, lv=lv, jpi=jpi, lt=lt,
                     tok=",".join(tok), klass=klass, cmt=ctext, fl=fltxt))

chars = re.compile(r"\b[EM][0-9]")
checks = [
    ("C1 tentative/bracket M field whose own comment cites RUL/POL/AZ",
     [x for x in rows if x["klass"] in ("paren", "bracket")
      and re.search(r"RUL|POL|azimuthal", x["cmt"])]),
    ("C2 firm E/M character with NO RUL/POL/AZ in own comment",
     [x for x in rows if x["klass"] == "firm" and chars.search(x["m"])
      and not re.search(r"RUL|POL|azimuthal", x["cmt"])]),
    ("C3 empty M field but M$ comment present",
     [x for x in rows if x["klass"] == "empty" and "M$" in x["cmt"]]),
    ("C4 comment writes D(+Q) but M field not tentative",
     [x for x in rows if "D(+Q)" in x["cmt"] and x["klass"] != "paren"]),
    ("C5 bracket [..] M field with provenance comment (comment unneeded)",
     [x for x in rows if x["klass"] == "bracket" and x["cmt"]]),
    ("C6 tentative M field with FIRM D+Q measured and RUL/LS basis",
     [x for x in rows if x["klass"] == "paren"
      and re.search(r"D\+Q|D,Q", x["cmt"])]),
    ("C7 firm E/M character + own comment cites RUL",
     [x for x in rows if x["klass"] == "firm" and chars.search(x["m"])
      and "RUL" in x["cmt"]]),
]

out = ["total G records: %d" % len(rows)]
for name, b in checks:
    out.append("")
    out.append("%s : %d" % (name, len(b)))
    for x in b:
        out.append("  L%-5d E=%-10s M=%-11s flag=%s q=%s lvl=%-10s Jpi=%-9s "
                   "T=%-14s tok=%s" % (x["line"], x["e"], x["m"], x["flag"],
                                       x["q"], x["lv"], x["jpi"], x["lt"],
                                       x["tok"]))
        out.append("        cmt: %s" % x["cmt"][:160])

out.append("")
out.append("=== full table ===")
for x in rows:
    out.append("L%-5d %-10s d=%-3s RI=%-7s %-11s MR=%-8s flag=%s q=%s lvl=%-10s "
               "Jpi=%-9s T=%-14s %-9s %-16s %s"
               % (x["line"], x["e"], x["de"], x["ri"], x["m"] or "-",
                  x["mr"] or "-", x["flag"].strip() or "-", x["q"].strip() or "-",
                  x["lv"], x["jpi"], x["lt"], x["klass"], x["tok"],
                  x["cmt"][:110]))
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:56]))
print("->", OUT)
