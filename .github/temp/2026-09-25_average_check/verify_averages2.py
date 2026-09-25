"""Verify every average comment in S34_adopted.ens against Java_Average.py (v2).

Per comment unit containing "average of":
  * rebuild the unit (first line + continuations),
  * run Java_Average.py --comment "<unit>",
  * parse "suggested adopted result" + method label,
  * compare with (a) the value quoted before "average of" (if any) and
    (b) the owning data record field: E/DE, RI/DRI, T/DT (T = ln2*tau), BE2.

READ-ONLY with respect to .ens files.
"""
import io
import math
import re
import subprocess
import sys

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
TOOL = r"d:\X\ND\ENSDF\.github\scripts\Java_Average.py"
LN2 = math.log(2)
DEBUG = "--debug" in sys.argv


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


lines = load(AD)
is_com = lambda l: len(l) >= 9 and l[6:7] == "c"
is_rec = lambda l: len(l) >= 9 and l[5:6] == " " and l[7:8] in ("L", "G")

if "--raw" in sys.argv:
    want = int(sys.argv[sys.argv.index("--raw") + 1])
    raw = []  # collect explicit comment units for the requested start line
    i = 0
    while i < len(lines):
        l = lines[i]
        if is_com(l) and l[5:6] == " ":
            blk = [l]
            j = i + 1
            while j < len(lines) and is_com(lines[j]) and lines[j][5:6] != " ":
                blk.append(lines[j])
                j += 1
            if i + 1 == want:
                print("--- unit at line %d ---" % want)
                for b in blk:
                    print(repr(b))
                print("--- tool output ---")
                pr = subprocess.run([sys.executable, TOOL, "--comment", "\n".join(blk)],
                                    capture_output=True, text=True, cwd=r"d:\X\ND\ENSDF")
                print(pr.stdout + pr.stderr)
                sys.exit(0)
            i = j
            continue
        i += 1
    print("no comment unit starts at line %d" % want)
    sys.exit(1)


# ---------------- build comment units ----------------
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

# ---------------- owner record ----------------
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
    """'1320.168' -> (1320.168, 3, '1320.168'). None if not a plain number."""
    s = (txt or "").strip()
    m = re.match(r"^([+-]?[\d.]+(?:[Ee][+-]?\d+)?)$", s)
    if not m:
        return None
    vs = m.group(1)
    dec = len(vs.split(".")[1]) if "." in vs else 0
    if "e" in vs.lower():
        dec = 0
    try:
        val = float(vs)
    except ValueError:
        return None
    return {"val": val, "dec": dec, "txt": vs}


def val_unit(txt):
    """'85 FS' -> (85.0, 'FS'); '0.315 PS' -> (0.315, 'PS')."""
    s = (txt or "").strip()
    m = re.match(r"^([+-]?[\d.]+(?:[Ee][+-]?\d+)?)\s*([A-Za-z]{1,4})?$", s)
    if not m:
        return None
    return float(m.group(1)), (m.group(2) or "").upper()


def unc_of(rec):
    """record uncertainty field digits + value decimals -> absolute uncertainty."""
    return None


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
                return {"val": float(vs), "unc": int(m.group(2)) * 10.0 ** (-dec),
                        "dec": dec, "txt": vs}
        k += 1
    return None


def parse_sugg(s):
    m = re.match(r"^([\d.]+)(?:\((\d+)\))?\s*([A-Za-z]*)$", (s or "").strip())
    if not m:
        return None
    vs = m.group(1)
    dec = len(vs.split(".")[1]) if "." in vs else 0
    val = float(vs)
    unc = int(m.group(2)) * 10.0 ** (-dec) if m.group(2) else None
    return {"val": val, "unc": unc, "dec": dec, "unit": m.group(3).upper()}


rows = []
for u in units:
    t = u["text"]
    if "average of" not in t.lower():
        continue
    ident_m = re.match(r"^([A-Za-z]{1,3})\$", t)
    ident = ident_m.group(1).upper() if ident_m else "(gen)"
    stated = "unweighted" if re.search(r"unweighted\s+average", t, re.I) else "weighted"

    proc = subprocess.run([sys.executable, TOOL, "--comment", "\n".join(u["raw"])],
                          capture_output=True, text=True, cwd=r"d:\X\ND\ENSDF")
    out = proc.stdout + proc.stderr
    sug = re.search(r"suggested adopted result:\s*(\S+)", out)
    lab = re.search(r"\((Weighted-Of-All|Unweighted-Average)\)", out)
    sugg_s = sug.group(1) if sug else "TOOL-ERROR"
    label = lab.group(1) if lab else "?"

    # (a) value quoted before "average of"
    pre = t[: re.search(r"\baverage\s+of\b", t, re.I).start()]
    q = None
    mq = re.findall(r"([\d.]+)\s*(?:[A-Za-z]{1,4}\s*)?\{I([^}]+)\}", pre)
    if mq:
        vs, us = mq[-1]
        dec = len(vs.split(".")[1]) if "." in vs else 0
        try:
            q = {"val": float(vs), "dec": dec,
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
                rec = {"val": tu[0], "unit": tu[1], "unc": du[0] if du else None,
                       "dec": 0, "txt": L[39:49].strip()}
                src = "L T/DT"
        elif ident == "BE2":
            b = be2_of(owner)
            if b:
                rec = b
                src = "2 L BE2"

    s = parse_sugg(sugg_s)
    miss = []
    if s is None:
        miss.append("tool-output-unparsed")
    else:
        # (a) quoted
        if q:
            if abs(q["val"] - s["val"]) > 0.5 * 10.0 ** (-q["dec"]) + 1e-9:
                miss.append("quoted value %s vs %s" % (q["val"], s["val"]))
            elif abs(q["unc"] - (s["unc"] or 0)) > 0.5 * 10.0 ** (-q["dec"]) + 1e-9:
                miss.append("quoted unc %.4g vs %.4g" % (q["unc"], s["unc"]))
        # (b) record
        if rec:
            if ident == "T":
                ratio = 1.0
                su = (s["unit"] or "").lower()
                ru = rec["unit"].lower()
                if su == "ps" and ru == "fs":
                    ratio = 1000.0
                elif su == "fs" and ru == "ps":
                    ratio = 0.001
                elif su and ru and su != ru and su[0] != ru[0]:
                    miss.append("unit %s vs %s" % (s["unit"], rec["unit"]))
                expT = LN2 * s["val"] * ratio
                expDT = LN2 * s["unc"] * ratio if s["unc"] else None
                tol = 0.5 * 10.0 ** (-rec["dec"]) + 1e-9
                if abs(rec["val"] - expT) > tol:
                    miss.append("record T %s vs ln2*tau %.4g" % (rec["val"], expT))
                if rec["unc"] is not None and expDT is not None and abs(rec["unc"] - expDT) > tol:
                    miss.append("record DT %s vs ln2*unc %.4g" % (rec["unc"], expDT))
            else:
                tol = 0.5 * 10.0 ** (-rec["dec"]) + 1e-9
                if abs(rec["val"] - s["val"]) > tol:
                    miss.append("record %.10g vs tool %.10g" % (rec["val"], s["val"]))
                if rec["unc"] is not None and s["unc"] is not None and abs(rec["unc"] - s["unc"]) > tol:
                    miss.append("record unc %.4g vs tool %.4g" % (rec["unc"], s["unc"]))
            if stated == "weighted" and label == "Unweighted-Average":
                miss.append("METHOD: comment says weighted, tool says Unweighted")

    rows.append((u["start"], ident, owner["line"] if owner else 0, src, sugg_s, label,
                 "CONSISTENT" if not miss else "; ".join(miss), u, rec, q, s))

print("average comments checked: %d" % len(rows))
ok_n = sum(1 for r in rows if r[6] == "CONSISTENT")
print("consistent: %d   inconsistent: %d" % (ok_n, len(rows) - ok_n))
print()
print("%-6s %-4s %-6s %-12s %-16s %-18s %s" % ("line", "id", "owner", "field", "tool-suggest", "method", "status"))
for r in rows:
    print("%-6d %-4s %-6d %-12s %-16s %-18s %s" % r[:7])
print()
print("=== inconsistent rows ===")
for r in rows:
    if r[6]:
        print("line %-6d ident %-4s owner %-6d suggest %-16s | %s" % (r[0], r[1], r[2], r[4], r[6]))

if DEBUG:
    print()
    print("=== debug: owner records of inconsistent rows ===")
    for r in rows:
        if r[6]:
            u = r[7]
            print("line %d owner %d %r" % (r[0], r[2], u["owner"]["text"] if u["owner"] else None))
            print("   record-parsed: %r  quoted: %r  sugg: %r" % (r[8], r[9], r[10]))
