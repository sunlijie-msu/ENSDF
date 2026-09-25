"""Verify every average comment in S34_adopted.ens against Java_Average.py (v3).

Per comment unit containing "average of":
  * rebuild the unit text (all lines concatenated, ENSDF prefixes stripped),
  * run Java_Average.py --comment "<text>",
  * parse as  : quoted inputs, parsed inputs, weighted / unweighted / suggested results,
  * compare  : (a) value quoted inside the comment (value before "average of"),
               (b) owning data record field (E/DE, RI/DRI, T/DT with T = ln2*tau, BE2),
  * flag     : parse drops, method disagreements, value/uncertainty mismatches.

Writes a UTF-8 report next to this script.  READ-ONLY for .ens files.
"""
import io
import math
import os
import re
import subprocess
import sys

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
TOOL = r"d:\X\ND\ENSDF\.github\scripts\Java_Average.py"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_v3.txt")
LN2 = math.log(2)
lines_out = []


def emit(s=""):
    lines_out.append(s)


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


lines = load(AD)
is_com = lambda l: len(l) >= 9 and l[6:7] == "c"
is_rec = lambda l: len(l) >= 9 and l[5:7] == "  " and l[7:8] in ("L", "G")

units = []
i = 0
while i < len(lines):
    l = lines[i]
    if is_com(l) and l[5:6] == " ":
        raw = [l]
        j = i + 1
        while j < len(lines) and is_com(lines[j]) and lines[j][5:6] != " ":
            raw.append(lines[j])
            j += 1
        units.append({"start": i + 1, "raw": raw,
                      "text": re.sub(r"\s+", " ", " ".join(r[9:] for r in raw)).strip()})
        i = j
        continue
    i += 1

for u in units:
    owner = None
    k = u["start"] - 2
    while k >= 0:
        if is_rec(lines[k]):
            owner = {"line": k + 1, "kind": lines[k][7:8], "text": lines[k]}
            break
        k -= 1
    u["owner"] = owner


def num(txt):
    s = (txt or "").strip()
    m = re.match(r"^([+-]?[\d.]+(?:[Ee][+-]?\d+)?)$", s)
    if not m:
        return None
    vs = m.group(1)
    dec = 0 if "e" in vs.lower() else (len(vs.split(".")[1]) if "." in vs else 0)
    return {"val": float(vs), "dec": dec, "txt": vs}


def val_unit(txt):
    s = (txt or "").strip()
    m = re.match(r"^([+-]?[\d.]+(?:[Ee][+-]?\d+)?)\s*([A-Za-z]{1,4})?$", s)
    return (float(m.group(1)), (m.group(2) or "").upper()) if m else None


def parse_sugg(s):
    m = re.match(r"^([\d.]+)(?:\((\d+)\))?\s*([A-Za-z]*)$", (s or "").strip())
    if not m:
        return None
    vs = m.group(1)
    dec = len(vs.split(".")[1]) if "." in vs else 0
    return {"val": float(vs), "dec": dec,
            "unc": int(m.group(2)) * 10.0 ** (-dec) if m.group(2) else None,
            "unit": m.group(3).upper()}


def be2_of(owner):
    if owner is None or owner["kind"] != "L":
        return None
    k = owner["line"]
    while k < len(lines) and not is_rec(lines[k]):
        L = lines[k]
        if len(L) > 12 and L[5:6] != " " and L[7:8] == "L":
            m = re.search(r"BE2=([\d.]+)\s+(\d+)", L)
            if m:
                vs = m.group(1)
                dec = len(vs.split(".")[1]) if "." in vs else 0
                return {"val": float(vs), "unc": int(m.group(2)) * 10.0 ** (-dec), "dec": dec}
        k += 1
    return None


rows = []
for u in units:
    t = u["text"]
    if "average of" not in t.lower():
        continue
    ident_m = re.match(r"^([A-Za-z][A-Za-z0-9]{0,3})\$", t)
    ident = ident_m.group(1).upper() if ident_m else "(gen)"
    stated = "unweighted" if re.search(r"unweighted\s+average", t, re.I) else "weighted"

    # text of the averaging set (after "average of", before any "Other")
    cut = t[re.search(r"\baverage\s+of\b", t, re.I).end():]
    cut = re.split(r"\bOthers?\b", cut, flags=re.I)[0]
    quoted_n = len(re.findall(r"[\d.]+\s*(?:[A-Za-z]{1,4}\s*)?\{I", cut))

    pr = subprocess.run([sys.executable, TOOL, "--comment", t], capture_output=True,
                        text=True, cwd=r"d:\X\ND\ENSDF")
    out = pr.stdout + pr.stderr
    parsed_n = None
    m = re.search(r"Parsed (\d+) data point", out)
    if m:
        parsed_n = int(m.group(1))
    wt = re.search(r"weighted average:\s*(\S+)", out)
    uw = re.search(r"unweighted average:\s*(\S+)", out)
    sg = re.search(r"suggested adopted result:\s*(\S+)", out)
    lb = re.search(r"\((Weighted-Of-All|Unweighted-Average)\)", out)
    wt_s = wt.group(1) if wt else "-"
    uw_s = uw.group(1) if uw else "-"
    sg_s = sg.group(1) if sg else "TOOL-ERROR"
    label = lb.group(1) if lb else "-"

    # (a) quoted result value (before "average of")
    pre = t[: re.search(r"\baverage\s+of\b", t, re.I).start()]
    q = None
    mq = re.findall(r"([\d.]+)\s*(?:[A-Za-z]{1,4}\s*)?\{I([^}]+)\}", pre)
    if mq:
        vs, us = mq[-1]
        dec = len(vs.split(".")[1]) if "." in vs else 0
        try:
            q = {"val": float(vs), "dec": dec, "txt": vs,
                 "unc": int(us.split("-")[0].lstrip("+")) * 10.0 ** (-dec)}
        except ValueError:
            q = None

    # (b) owning record field
    rec = None
    src = ""
    owner = u["owner"]
    if owner:
        L = owner["text"]
        if ident == "E":
            v = num(L[9:19]); un = num(L[19:21])
            if v:
                rec = dict(v, unc=(un["val"] * 10.0 ** (-v["dec"])) if un else None)
                src = "%s E/DE" % owner["kind"]
        elif ident == "RI":
            v = num(L[22:29]); un = num(L[29:31])
            if v:
                rec = dict(v, unc=(un["val"] * 10.0 ** (-v["dec"])) if un else None)
                src = "G RI/DRI"
        elif ident == "T":
            tu = val_unit(L[39:49]); du = val_unit(L[49:55])
            if tu:
                ttxt = L[39:49].strip()
                tdec = len(ttxt.split()[0].split(".")[1]) if "." in ttxt.split()[0] else 0
                rec = {"val": tu[0], "unit": tu[1], "dec": tdec,
                       "unc": (du[0] * 10.0 ** (-tdec)) if du else None}
                src = "L T/DT"
        elif ident == "BE2":
            b = be2_of(owner)
            if b:
                rec = b
                src = "2 L BE2"

    # candidate results from the tool
    cands = {}
    for name, s in (("suggested", sg_s), ("weighted", wt_s), ("unweighted", uw_s)):
        p = parse_sugg(s if "(" in s or s.replace(".", "").isdigit() else None)
        if p is None and s != "-" and "TOOL" not in s:
            p = parse_sugg(s)
        if p:
            cands[name] = p

    issues = []
    if parsed_n is None:
        issues.append("tool produced no parsed-point count")
    elif parsed_n != quoted_n:
        issues.append("parsed %d of %d quoted inputs" % (parsed_n, quoted_n))

    def cmp_val(target, tol_dec):
        """which candidate matches target (val,unc)?"""
        tol = 0.5 * 10.0 ** (-tol_dec) + 1e-9
        hits = []
        for nm, c in cands.items():
            dv = abs(c["val"] - target["val"])
            if dv > tol:
                # record T case: compare ln2*tau
                continue
            if "unc" in target and target["unc"] is not None and c["unc"] is not None:
                if abs(c["unc"] - target["unc"]) > tol:
                    continue
            hits.append(nm)
        return hits

    match_names = []
    if q:
        hits = cmp_val({"val": q["val"], "unc": q["unc"]}, q["dec"])
        if not hits:
            sb = cands.get("suggested")
            issues.append("quoted %s(%.4g) vs suggested %s" % (q["txt"], q["unc"], sg_s))
        else:
            match_names.append("quoted->" + ",".join(hits))
    if rec:
        if ident == "T":
            su = (cands.get("suggested", {}) or {}).get("unit", "").lower()
            ru = rec["unit"].lower()
            ratio = 1.0
            if su == "ps" and ru == "fs":
                ratio = 1000.0
            elif su == "fs" and ru == "ps":
                ratio = 0.001
            target = {"val": rec["val"], "unc": rec["unc"], "ratio": ratio}
            tol = 0.5 * 10.0 ** (-rec["dec"]) + 1e-9
            hits = []
            for nm, c in cands.items():
                eT = LN2 * c["val"] * ratio
                eDT = LN2 * c["unc"] * ratio if c["unc"] else None
                if abs(eT - rec["val"]) > tol:
                    continue
                if rec["unc"] is not None and eDT is not None and abs(eDT - rec["unc"]) > tol:
                    continue
                hits.append(nm)
            if not hits:
                sc = cands.get("suggested", {})
                issues.append("record T %s(%.3g) vs ln2*suggested %.4g(%.4g)"
                              % (rec["val"], rec["unc"] or 0, LN2 * sc.get("val", 0) * ratio,
                                 LN2 * (sc.get("unc") or 0) * ratio))
            else:
                match_names.append("record->" + ",".join(hits))
        else:
            hits = cmp_val({"val": rec["val"], "unc": rec["unc"]}, rec["dec"])
            if not hits:
                sc = cands.get("suggested")
                d1 = "" if sc is None else " vs suggested %.10g" % sc["val"]
                issues.append("record %s%s" % (rec["txt"], d1))
            else:
                match_names.append("record->" + ",".join(hits))

    if stated == "unweighted" and label == "Weighted-Of-All":
        issues.append("METHOD: comment says unweighted, tool recommends weighted")
    if stated == "weighted" and label == "Unweighted-Average":
        issues.append("METHOD: comment says weighted, tool recommends unweighted")
    if rec is None and q is None:
        issues.append("no adopted target value located (comment-only)")

    rows.append({"line": u["start"], "ident": ident, "owner": owner["line"] if owner else 0,
                 "field": src, "quoted_n": quoted_n, "parsed_n": parsed_n,
                 "sugg": sg_s, "label": label, "wt": wt_s, "uw": uw_s,
                 "stated": stated, "match": match_names, "issues": issues,
                 "rec": rec, "owner_text": owner["text"] if owner else ""})

emit("average comments checked: %d" % len(rows))
emit("clean: %d    flagged: %d" % (sum(1 for r in rows if not r["issues"]),
                                   sum(1 for r in rows if r["issues"])))
emit()
hdr = "%-6s %-5s %-6s %-10s %-4s %-4s %-16s %-17s %-10s %-14s %s"
emit(hdr % ("line", "id", "owner", "field", "qN", "pN", "suggested", "recommend", "stated", "record", "matched-by"))
for r in rows:
    rv = "-"
    if r["rec"]:
        rv = "%.10g" % r["rec"]["val"]
        if r["rec"].get("unc") is not None:
            rv += "(%.3g)" % r["rec"]["unc"]
    emit(hdr % (r["line"], r["ident"], r["owner"], r["field"], r["quoted_n"], r["parsed_n"],
                r["sugg"], r["label"], r["stated"], rv, ",".join(r["match"]) or "-"))
emit()
emit("=== FLAGGED (%d) ===" % sum(1 for r in rows if r["issues"]))
for r in rows:
    if r["issues"]:
        emit("line %-6d %-4s owner %-6s stated %-10s rec. %-17s | %s"
             % (r["line"], r["ident"], r["owner"], r["stated"], r["label"], "; ".join(r["issues"])))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines_out) + "\n")
print("\n".join(lines_out[:4]))
print("... report written to %s" % OUT)
