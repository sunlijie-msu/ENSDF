import io, re, math
from collections import defaultdict

PATH = "A75/A75_13NDS.ens"
norm = lambda s: re.sub(r"\s+", " ", s.upper().strip())


def parse_E(rec):
    e = rec[9:19].strip().replace(" ", ""); d = rec[19:21].strip()
    m = re.match(r"^([0-9]+\.?[0-9]*)(?:E([+-]?\d+))?$", e)
    if not m:
        return None, 0.0
    mant = m.group(1); exp = int(m.group(2)) if m.group(2) else 0
    dec = exp - (len(mant.split(".")[1]) if "." in mant else 0)
    return float(mant) * 10.0 ** exp, (int(d) * 10.0 ** dec if d.isdigit() else 0.0)


is_L = lambda r: r[5] == " " and r[6] == " " and r[7] == "L"
blocks, cur = [], []
for raw in io.open(PATH, encoding="utf-8", errors="replace"):
    r = raw.rstrip("\n").ljust(80)
    if r.strip() == "":
        if cur:
            blocks.append(cur); cur = []
    else:
        cur.append(r)
if cur:
    blocks.append(cur)

ds = {}
for b in blocks:
    ds.setdefault((b[0][:5], norm(b[0][9:39])), []).append(b)

for b in blocks:
    head = b[0]
    if "ADOPTED LEVELS" not in head[9:39].upper() or not any("XREF=-(" in r for r in b):
        continue
    nuc = head[:5]
    keys = {r[8]: norm(r[9:39]) for r in b if r[5] == " " and r[6] == " " and r[7] == "X" and r[8] != " "}
    letters = {}
    for k, dsid in keys.items():
        c = ds.get((nuc, dsid), [])
        letters[k] = c[0] if len(c) == 1 else None
    levels = defaultdict(list)
    for k, blk in letters.items():
        if blk:
            levels[k] = [parse_E(r) for r in blk if is_L(r)]
            levels[k] = [(E, s) for E, s in levels[k] if E is not None]
    idx = [i for i, r in enumerate(b) if is_L(r)]
    print("== %s  datasets in X-records: %d, resolved to a block: %d" % (nuc, len(keys), sum(1 for v in letters.values() if v)))
    tot = {"listed_has": 0, "listed_n": 0, "other_has": 0, "other_n": 0}
    for n, i in enumerate(idx):
        end = idx[n + 1] if n + 1 < len(idx) else len(b)
        xs = ""
        for j in range(i + 1, end):
            r = b[j]
            if r[5] != " " and r[7] == "L" and r[9:].lstrip().startswith("XREF"):
                xs += re.sub(r"^XREF(?:\+=|=)", "", r[9:80].strip()).replace("$", "")
        m = re.match(r"^-\(([^)]*)\)", xs)
        if not m:
            continue
        E, s = parse_E(b[i])
        excl = set(m.group(1))
        res = []
        for k, lv in levels.items():
            has = any(abs(e - E) <= max(5.0, 3.0 * math.hypot(s, se)) for e, se in lv)
            if k in excl:
                tot["listed_n"] += 1; tot["listed_has"] += has
            else:
                tot["other_n"] += 1; tot["other_has"] += has
            res.append((k, has, k in excl))
        bad_l = [k for k, h, ex in res if ex and h]
        bad_o = [k for k, h, ex in res if (not ex) and (not h)]
        print("  E=%-9s excl=%-7s listed-but-present=%s  not-listed-but-absent=%s" % (E, "".join(sorted(excl)), bad_l, bad_o))
    print("  listed datasets containing the level: %d of %d" % (tot["listed_has"], tot["listed_n"]))
    print("  other datasets containing the level : %d of %d" % (tot["other_has"], tot["other_n"]))
