"""Verify every average comment in S34_adopted.ens using Java_Average.py in-process (v4).

Uses the tool's own functions (parse_comment_data, weighted_average, unweighted_average,
find_suggested_average, fmt_val_unc) and replicates its adoption decision, then compares
the result with (a) the value quoted inside the comment and (b) the owning data record
field (E/DE, RI/DRI, T/DT with T = ln2*tau, BE2).  READ-ONLY for .ens files.
"""
import io
import math
import os
import re
import sys

sys.path.insert(0, r"d:\X\ND\ENSDF\.github\scripts")
import Java_Average as JA

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_v4.txt")
LN2 = math.log(2)
out = []
emit = lambda s="": out.append(s)


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


def run_tool(text):
    data, base_unit, src_max_dec = JA.parse_comment_data(text)
    if len(data) < 2:
        return None
    n = len(data)
    wt = JA.weighted_average(data)
    uw = JA.unweighted_average(data)
    crit = JA.critical_chi_sq_display(n)
    eff = max(JA.INCONSISTENCY_THRESHOLD, crit)
    if wt["reduced_chi_sq"] <= eff:
        label = "Weighted-Of-All"
        val = wt["value"]
        unc = JA.find_suggested_average(max(wt["internal_unc"], wt["external_unc"]), data)
    else:
        label = "Unweighted-Average"
        val = uw["value"]
        unc = JA.find_suggested_average(uw["final_unc"], data)
    unit = " %s" % base_unit if base_unit else ""
    return {
        "n": n, "label": label,
        "sugg_s": JA.fmt_val_unc(val, unc, src_max_dec) + unit,
        "wt_s": JA.fmt_val_unc(wt["value"], wt["internal_unc"], src_max_dec) + unit,
        "uw_s": JA.fmt_val_unc(uw["value"], uw["final_unc"], src_max_dec) + unit,
        "chi2": wt["reduced_chi_sq"], "crit": eff, "unit": (base_unit or "").upper(),
    }


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
    im = re.match(r"^([A-Za-z][A-Za-z0-9]{0,3})\$", t)
    ident = im.group(1).upper() if im else "(gen)"
    stated = "unweighted" if re.search(r"unweighted\s+average", t, re.I) else "weighted"

    cut = re.split(r"\bOthers?\b", t[re.search(r"\baverage\s+of\b", t, re.I).end():], flags=re.I)[0]
    quoted_n = len(re.findall(r"[\d.]+\s*(?:[A-Za-z]{1,4}\s*)?\{I", cut))

    res = run_tool(t)
    issues = []
    if res is None:
        rows.append({"line": u["start"], "ident": ident, "owner": u["owner"]["line"] if u["owner"] else 0,
                     "field": "", "qN": quoted_n, "pN": 0, "sugg": "TOOL-PARSE-FAIL", "label": "-",
                     "stated": stated, "rec": None, "match": [], "issues": ["tool parsed < 2 inputs"]})
        continue
    if res["n"] != quoted_n:
        issues.append("tool parsed %d of %d quoted inputs" % (res["n"], quoted_n))

    # (a) quoted value before "average of"
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
    rec, src = None, ""
    owner = u["owner"]
    if owner:
        L = owner["text"]
        if ident == "E":
            v, un = num(L[9:19]), num(L[19:21])
            if v:
                rec = dict(v, unc=(un["val"] * 10.0 ** (-v["dec"])) if un else None)
                src = "%s E/DE" % owner["kind"]
        elif ident == "RI":
            v, un = num(L[22:29]), num(L[29:31])
            if v:
                rec = dict(v, unc=(un["val"] * 10.0 ** (-v["dec"])) if un else None)
                src = "G RI/DRI"
        elif ident == "T":
            tu, du = val_unit(L[39:49]), val_unit(L[49:55])
            if tu:
                tt = L[39:49].strip().split()
                tdec = len(tt[0].split(".")[1]) if "." in tt[0] else 0
                rec = {"val": tu[0], "unit": tu[1], "dec": tdec,
                       "unc": (du[0] * 10.0 ** (-tdec)) if du else None}
                src = "L T/DT"
        elif ident == "BE2":
            b = be2_of(owner)
            if b:
                rec = b
                src = "2 L BE2"

    cands = {}
    for nm, s in (("suggested", res["sugg_s"]), ("weighted", res["wt_s"]), ("unweighted", res["uw_s"])):
        p = parse_sugg(s)
        if p:
            cands[nm] = p

    match = []
    if q:
        tol = 0.5 * 10.0 ** (-q["dec"]) + 1e-9
        all_hits = [nm for nm, c in cands.items()
                    if abs(c["val"] - q["val"]) <= tol and (c["unc"] is None or q["unc"] is None
                                                            or abs(c["unc"] - q["unc"]) <= tol)]
        if all_hits:
            match.append("quoted->" + ",".join(all_hits))
        sg = cands.get("suggested")
        ok_sugg = sg is not None and abs(sg["val"] - q["val"]) <= tol and (
            sg["unc"] is None or q["unc"] is None or abs(sg["unc"] - q["unc"]) <= tol)
        if not ok_sugg:
            issues.append("quoted %s(%.4g) != Suggested Adopted Result %s" % (q["txt"], q["unc"], res["sugg_s"]))
    if rec:
        if ident == "T":
            ratio = 1.0
            su, ru = res["unit"].lower(), rec["unit"].lower()
            if su == "ps" and ru == "fs":
                ratio = 1000.0
            elif su == "fs" and ru == "ps":
                ratio = 0.001
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
            if hits:
                match.append("record->" + ",".join(hits))
            else:
                sc = cands.get("suggested", {})
                issues.append("record T %s(%.4g)%s vs ln2*suggested %.4g(%.4g)"
                              % (rec["val"], rec["unc"] or 0, rec["unit"], LN2 * sc.get("val", 0) * ratio,
                                 (LN2 * (sc.get("unc") or 0) * ratio)))
        else:
            tol = 0.5 * 10.0 ** (-rec["dec"]) + 1e-9
            hits = [nm for nm, c in cands.items()
                    if abs(c["val"] - rec["val"]) <= tol and (c["unc"] is None or rec["unc"] is None
                                                              or abs(c["unc"] - rec["unc"]) <= tol)]
            if hits:
                match.append("record->" + ",".join(hits))
            else:
                sc = cands.get("suggested")
                issues.append("record %s vs suggested %s" % (rec["txt"], res["sugg_s"]))
    if rec is None and q is None:
        issues.append("no adopted target value located")
    if stated == "unweighted" and res["label"] == "Weighted-Of-All":
        issues.append("METHOD: comment says unweighted; tool recommends weighted (chi2/(n-1)=%.3f vs thresh %.3f)"
                      % (res["chi2"], res["crit"]))
    if stated == "weighted" and res["label"] == "Unweighted-Average":
        issues.append("METHOD: comment says weighted; tool recommends unweighted (chi2/(n-1)=%.3f vs thresh %.3f)"
                      % (res["chi2"], res["crit"]))

    rows.append({"line": u["start"], "ident": ident, "owner": owner["line"] if owner else 0,
                 "field": src, "qN": quoted_n, "pN": res["n"], "sugg": res["sugg_s"],
                 "label": res["label"], "stated": stated, "rec": rec, "match": match,
                 "issues": issues, "wt": res["wt_s"], "uw": res["uw_s"],
                 "ref": re.sub(r"\s+", " ", t)[:58]})

emit("average comments checked: %d" % len(rows))
emit("clean: %d    flagged: %d" % (sum(1 for r in rows if not r["issues"]), sum(1 for r in rows if r["issues"])))
emit()
hdr = "%-6s %-5s %-6s %-9s %-4s %-4s %-16s %-18s %-11s %-16s %s"
emit(hdr % ("line", "id", "owner", "field", "qN", "pN", "tool-suggests", "recommends", "comment-says", "record", "matched-by"))
for r in rows:
    rv = "-"
    if r["rec"]:
        rv = "%.10g" % r["rec"]["val"]
        if r["rec"].get("unc") is not None:
            rv += "(%.3g)%s" % (r["rec"]["unc"], r["rec"].get("unit", ""))
    emit(hdr % (r["line"], r["ident"], r["owner"], r["field"], r["qN"], r["pN"], r["sugg"],
                r["label"], r["stated"], rv, ",".join(r["match"]) or "-"))
emit()
emit("=== FLAGGED (%d) ===" % sum(1 for r in rows if r["issues"]))
for r in rows:
    if r["issues"]:
        emit("line %-6d %-5s owner %-6s stated %-11s tool: %-16s %-18s"
             % (r["line"], r["ident"], r["owner"], r["stated"], r["sugg"], r["label"]))
        emit("        comment: %s" % r["ref"])
        emit("        issue  : %s" % "; ".join(r["issues"]))
emit()
emit("=== weighted vs unweighted candidates for flagged rows ===")
for r in rows:
    if r["issues"]:
        rv = "-"
        if r["rec"]:
            rv = r["rec"].get("txt") or "%.10g" % r["rec"]["val"]
            if r["rec"].get("unc") is not None:
                rv += "(%.3g)" % r["rec"]["unc"]
        emit("line %-6d weighted=%-16s unweighted=%-16s record=%s" % (r["line"], r.get("wt", "-"),
                                                                      r.get("uw", "-"), rv))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("\n".join(out[:3]))
print("report -> %s" % OUT)
