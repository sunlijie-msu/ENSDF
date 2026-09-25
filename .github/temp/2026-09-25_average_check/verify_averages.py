"""Verify every average comment in S34_adopted.ens against Java_Average.py.

For each comment unit containing "average of":
  * rebuild the comment unit (first line + continuations),
  * run .github/scripts/Java_Average.py --comment "<unit>",
  * parse the tool's "suggested adopted result" and method label,
  * compare with the adopted value: the value quoted before "average of" if present,
    else the field of the owning data record (E/DE, RI/DRI, T/DT (T = ln2*tau), BE2).

READ-ONLY: writes nothing to .ens files.
"""
import io
import math
import os
import re
import subprocess
import sys

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
TOOL = r"d:\X\ND\ENSDF\.github\scripts\Java_Average.py"
LN2 = math.log(2)


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


lines = load(AD)


def is_com(l):
    return len(l) >= 9 and l[6:7] == "c"


def is_rec(l):
    return len(l) >= 9 and l[5:6] == " " and l[7:8] in ("L", "G")


# ---- build comment units (first line + continuation lines) ----
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
        units.append(
            {
                "start": i + 1,
                "end": j,
                "raw": raw,
                "text": re.sub(r"\s+", " ", " ".join(r[9:] for r in raw)).strip(),
            }
        )
        i = j
        continue
    i += 1

# ---- owner record for each unit ----
for u in units:
    owner = None
    k = u["start"] - 2
    while k >= 0:
        if is_rec(lines[k]):
            owner = {"line": k + 1, "kind": lines[k][7:8], "text": lines[k]}
            break
        k -= 1
    u["owner"] = owner


def field(line, a, b):
    return line[a:b]


def rec_level(owner):
    """Parse (value, unc, decimals) from an L/G record E, RI or T field."""
    L = owner["text"]

    def num(txt):
        txt = txt.strip()
        m = re.match(r"^([+-]?[\d.]+(?:E[+-]?\d+)?)$", txt)
        return (float(m.group(1)), txt) if m else (None, txt)

    out = {}
    v, vt = num(field(L, 9, 19))
    out["E"] = (v, vt)
    u, ut = num(field(L, 19, 21))
    out["DE"] = (u, ut)
    v, vt = num(field(L, 22, 29))
    out["RI"] = (v, vt)
    u, ut = num(field(L, 29, 31))
    out["DRI"] = (u, ut)
    out["T"] = num(field(L, 39, 49))
    out["DT"] = num(field(L, 49, 55))
    return out


def parse_suggestion(s):
    """'1320.168(20)' / '85(7)' / '0.0203(13) fs' -> (val, unc, decimals, unit)."""
    m = re.match(r"^([\d.]+)(?:\((\d+)\))?\s*(\S*)$", s.strip())
    if not m:
        return None
    vs = m.group(1)
    dec = len(vs.split(".")[1]) if "." in vs else 0
    val = float(vs)
    unc = int(m.group(2)) * 10.0 ** (-dec) if m.group(2) else None
    return val, unc, dec, m.group(3)


def parse_ensdf_field(vtxt, utxt):
    """('1320.168','20') -> (1320.168, 0.020, 3)."""
    if vtxt is None:
        return None
    vs = vtxt.strip()
    dec = len(vs.split(".")[1]) if "." in vs else 0
    try:
        val = float(vs)
    except ValueError:
        return None
    u = None
    if utxt:
        us = utxt.strip()
        if re.match(r"^\d+$", us):
            u = int(us) * 10.0 ** (-dec)
    return val, u, dec


def be2_of(owner):
    """Look for BE2= in the owner L-record's continuation lines."""
    if owner is None or owner["kind"] != "L":
        return None
    k = owner["line"]  # 1-based; continuations follow
    while k < len(lines) and not is_rec(lines[k]):
        L = lines[k]
        if len(L) > 12 and L[6:7] == " " and L[7:8] == "L":
            m = re.search(r"BE2=([\d.E+-]+)\s+(\d+)", L)
            if m:
                vs = m.group(1)
                dec = len(vs.split(".")[1]) if "." in vs else 0
                return float(vs), int(m.group(2)) * 10.0 ** (-dec), dec
        k += 1
    return None


rows = []
for u in units:
    t = u["text"]
    if "average of" not in t.lower():
        continue
    ident_m = re.match(r"^([A-Za-z]{1,3})\$", t)
    ident = ident_m.group(1).upper() if ident_m else "(general)"
    stated = "unweighted" if re.search(r"unweighted\s+average", t, re.I) else "weighted"

    proc = subprocess.run(
        [sys.executable, TOOL, "--comment", "\n".join(u["raw"])],
        capture_output=True,
        text=True,
        cwd=r"d:\X\ND\ENSDF",
    )
    out = proc.stdout + proc.stderr
    sug = re.search(r"suggested adopted result:\s*(\S+)", out)
    lab = re.search(r"\((Weighted-Of-All|Unweighted-Average)\)", out)
    sug_str = sug.group(1) if sug else "TOOL-ERROR"
    label = lab.group(1) if lab else "?"

    # value quoted BEFORE "average of" (previous/adopted result) if any
    pre = t[: re.search(r"\baverage\s+of\b", t, re.I).start()]
    pre_nums = re.findall(r"([\d.]+)\s*\{I([^}]+)\}", pre)
    quoted = None
    if pre_nums:
        vs, us = pre_nums[-1]
        dec = len(vs.split(".")[1]) if "." in vs else 0
        try:
            quoted = (float(vs), int(us.split("-")[0].lstrip("+")) * 10.0 ** (-dec), dec)
        except ValueError:
            quoted = None

    # expected from the owning data record
    exp = None
    exp_src = ""
    owner = u["owner"]
    if owner:
        f = rec_level(owner)
        if ident == "E":
            exp = parse_ensdf_field(f["E"][1], f["DE"][1])
            exp_src = "%s E/DE" % owner["kind"]
        elif ident == "RI":
            exp = parse_ensdf_field(f["RI"][1], f["DRI"][1])
            exp_src = "G RI/DRI"
        elif ident == "T":
            TT, TTt = f["T"]
            DT, DTt = f["DT"]
            if TT is not None:
                unit = TTt.upper()
                exp = (TT, DT, 0, unit)
                exp_src = "L T/DT (x1/ln2 -> tau)"
        elif ident == "BE2":
            b = be2_of(owner)
            if b:
                exp = b
                exp_src = "2 L BE2"

    s = parse_suggestion(sug_str)
    verdict = "?"
    detail = ""
    if s is None:
        verdict = "TOOL-ERROR/NOPARSE"
    else:
        sval, sunc, sdec, sunit = s
        tol = 0.5 * 10.0 ** (-sdec) + 1e-12
        # A) compare with the value quoted inside the comment
        if quoted:
            qval, qunc, qdec = quoted
            dv = abs(qval - sval)
            du = abs(qunc - sunc) if sunc is not None else 9e9
            okq = dv <= 0.5 * 10.0 ** (-qdec) + 1e-9 and du <= 0.5 * 10.0 ** (-qdec) + 1e-9
            detail += "quoted=%s(%.0f) " % (qval, qunc * 10**qdec)
            verdict = "OK" if okq else "MISMATCH-quoted"
        # B) compare with the data record field
        if exp:
            e = list(exp)
            if ident == "T":
                tval, tunc, tdec, tunit = e
                # tool suggestion is tau in the comment's unit; record holds T = ln2*tau
                ratio = 1.0
                if sunit and sunit.lower() == "ps" and tunit == "FS":
                    ratio = 1000.0
                elif sunit and sunit.lower() == "fs" and tunit == "PS":
                    ratio = 0.001
                expT = LN2 * sval * ratio
                expDT = (LN2 * sunc * ratio) if sunc is not None else None
                okT = abs(tval - expT) <= 0.5 + 1e-9
                okDT = (tunc is None) or (expDT is None) or (abs(tunc - expDT) <= 0.5 + 1e-9)
                detail += "recT=%s(%.1f) expT=%.1f(%.1f) " % (tval, tunc or 0, expT, expDT or 0)
                v2 = "OK" if (okT and okDT) else "MISMATCH-record"
            else:
                ev, eu, ed = e
                dval = abs(ev - sval)
                dun = 9e9 if eu is None else abs(eu - sval * 0 + eu - (sunc if sunc else 0))
                dun = 9e9 if (eu is None or sunc is None) else abs(eu - sunc)
                tolE = 0.5 * 10.0 ** (-ed) + 1e-12
                okE = dval <= tolE and dun <= tolE
                detail += "rec=%s(%.4g) " % (ev, eu if eu is not None else -1)
                v2 = "OK" if okE else "MISMATCH-record"
            if verdict in ("OK", "?"):
                verdict = v2
            elif v2 == "MISMATCH-record":
                verdict += "+record"
    meth = "OK" if ((stated == "weighted" and label == "Weighted-Of-All") or
                    (stated == "unweighted" and label == "Unweighted-Average")) else "METHOD(%s vs %s)" % (stated, label)

    rows.append((u["start"], ident, owner["line"] if owner else -1, exp_src, sug_str, label, meth, verdict, detail))

print("=== average comments checked: %d ===" % len(rows))
print()
hdr = "%-6s %-9s %-7s %-20s %-16s %-18s %-6s %s"
print(hdr % ("line", "ident", "own", "expected-src", "tool-suggest", "method", "meth", "verdict"))
for r in rows:
    print(hdr % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
print()
bad = [r for r in rows if not r[7].startswith("OK")]
print("=== non-OK rows: %d ===" % len(bad))
for r in bad:
    print(" line %-6s %-4s owner %-6s suggest %-14s verdict %-28s %s" % (r[0], r[1], r[2], r[4], r[7], r[8]))
