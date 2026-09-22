import re, json, os, hashlib

ADOPTED = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
BASE = r"d:\X\ND\ENSDF\A34\S34\new"

letter_to_file = {
    'A': 'S34_34p_beta_decay_12.43_s.ens',
    'B': 'S34_34cl_ec_decay_1.5266_s.ens',
    'C': 'S34_34cl_ec_decay_31.99_m.ens',
    'D': 'S34_3h_32s_pg.ens',
    'E': 'S34_3h_35cl_ag.ens',
    'F': 'S34_4he_30si_a_resonances.ens',
    'G': 'S34_12c_24mg_34sg.ens',
    'H': 'S34_24mg_16o_a2pg.ens',
    'I': 'S34_27al_10b_2png.ens',
    'J': 'S34_27al_12c_apg.ens',
    'K': 'S34_28si_34s_34sPg.ens',
    'L': 'S34_30si_a_g_a_n_resonances.ens',
    'M': 'S34_31p_a_pg.ens',
    'N': 'S34_32s_t_p.ens',
    'O': 'S34_32s_a_2he.ens',
    'P': 'S34_ng_E_thermal.ens',
    'Q': 'S34_33s_n_g_n_n_resonances.ens',
    'R': 'S34_33s_d_p.ens',
    'S': 'S34_34s_g_gP_pol_g_gP.ens',
    'T': 'S34_34s_e_eP.ens',
    'U': 'S34_34s_pi+_pi+P_pi-_pi-P.ens',
    'V': 'S34_34s_n_n_n_nP.ens',
    'W': 'S34_34s_p_pP_pol_p_pP.ens',
    'X': 'S34_34s_p_pPg.ens',
    'Y': 'S34_34s_pol_d_d_pol_d_dP.ens',
    'Z': 'S34_34s_a_a_a_aP_a_aPg.ens',
    'a': 'S34_35cl_g_p.ens',
    'b': 'S34_35cl_n_d.ens',
    'c': 'S34_35cl_d_3he.ens',
    'd': 'S34_37cl_p_ag.ens',
    'e': 'S34_206pb_34s_34sPg.ens',
    'f': 'S34_208pb_34s_34sP.ens',
    'g': 'S34_208pb_36s_34sg.ens',
}


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def num(s):
    m = re.match(r'^-?\d+(?:\.\d+)?', s)
    return float(m.group(0)) if m else None


def dec_places(s):
    m = re.match(r'^-?\d+\.(\d+)', s)
    return len(m.group(1)) if m else 0


def parse_adopted(path):
    """Parse adopted dataset: L records with their G records, XREF, and comments."""
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    blocks = []
    cur = None
    for i, l in enumerate(lines):
        if len(l) < 8:
            continue
        col6, col7, col8 = l[5], l[6], l[7]
        plain_L = col6 == ' ' and col7 == ' ' and col8 == 'L'
        plain_G = col6 == ' ' and col7 == ' ' and col8 == 'G'
        cont_L = col6 != ' ' and col7 == ' ' and col8 == 'L'
        com_L = (col7 in 'cC') and col8 == 'L'
        if plain_L:
            if cur:
                blocks.append(cur)
            cur = {
                "lineno": i + 1,
                "E_raw": l[9:19],
                "DE_raw": l[19:21],
                "J": l[22:39].strip(),
                "T": l[39:49].strip(),
                "C": (l[76] if len(l) > 76 else ' '),
                "Q": (l[79] if len(l) > 79 else ' '),
                "gammas": [],
                "xref": None,
                "comments": [],
                "raw": l,
            }
        elif cur is not None:
            if plain_G:
                cur["gammas"].append({"E_raw": l[9:19], "DE_raw": l[19:21], "raw": l, "lineno": i + 1})
            elif cont_L:
                m = re.search(r'XREF=(\S+)', l)
                if m:
                    cur["xref"] = m.group(1)
            elif com_L:
                cur["comments"].append(l)
    if cur:
        blocks.append(cur)

    out = []
    for b in blocks:
        e_str = b["E_raw"].strip()
        de_str = b["DE_raw"].strip()
        e = num(e_str)
        if e is None:
            continue
        out.append({
            "lineno": b["lineno"],
            "E_str": e_str,
            "E": e,
            "dec": dec_places(e_str),
            "DE_str": de_str,
            "DE_abs": (num(de_str) * 10 ** -dec_places(e_str)) if num(de_str) is not None else None,
            "Q": b["Q"],
            "C": b["C"],
            "nG": len(b["gammas"]),
            "nG_with_DE": sum(1 for g in b["gammas"] if g["DE_raw"].strip() and re.match(r'^\d', g["DE_raw"].strip())),
            "xref": b["xref"],
            "gE_strs": [g["E_raw"].strip() for g in b["gammas"]],
            "raw": b["raw"],
        })
    return out


def parse_dataset(path):
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    lv = []
    for i, l in enumerate(lines):
        if len(l) < 8:
            continue
        if l[5] == ' ' and l[6] == ' ' and l[7] == 'L':
            e_str = l[9:19].strip()
            de_str = l[19:21].strip()
            e = num(e_str)
            if e is None:
                continue
            lv.append({
                "lineno": i + 1, "E_str": e_str, "E": e,
                "dec": dec_places(e_str), "DE_str": de_str,
                "DE_abs": (num(de_str) * 10 ** -dec_places(e_str)) if num(de_str) is not None else None,
                "raw": l,
            })
    return lv


XREF_RE = re.compile(r'([A-Za-z])(?:\((\d+(?:\.\d+)?)([*?])?\))?')

def parse_xref(x):
    out = []
    i = 0
    while i < len(x):
        ch = x[i]
        if ch.isalpha():
            m = re.match(r'\((\d+(?:\.\d+)?)([*?])?\)', x[i+1:])
            if m:
                out.append((ch, float(m.group(1)), m.group(2) or ''))
                i += 1 + m.end()
            else:
                out.append((ch, None, ''))
                i += 1
        else:
            i += 1
    return out


if __name__ == "__main__":
    print("adopted sha256[:16] =", sha(ADOPTED))
    adopted = parse_adopted(ADOPTED)
    print("adopted L records:", len(adopted))

    ds = {k: parse_dataset(os.path.join(BASE, v)) for k, v in letter_to_file.items()}

    eligible = [a for a in adopted if a["nG"] == 0 or a["nG_with_DE"] == 0]
    print("eligible (no gammas OR no gamma has uncertainty):", len(eligible))
    print("  of which nG==0:", sum(1 for a in eligible if a["nG"] == 0))
    print("  of which nG>0 but no DE:", sum(1 for a in eligible if a["nG"] > 0))

    rows = []
    for a in eligible:
        info = {"lineno": a["lineno"], "E": a["E_str"], "DE": a["DE_str"], "DE_abs": a["DE_abs"],
                "nG": a["nG"], "Q": a["Q"], "C": a["C"], "xref": a["xref"], "cands": []}
        if a["xref"]:
            for letter, paren_e, mk in parse_xref(a["xref"]):
                levels = ds.get(letter, [])
                best = None
                for L in levels:
                    d = abs(L["E"] - a["E"])
                    if best is None or d < best[0]:
                        best = (d, L)
                if best:
                    info["cands"].append({
                        "letter": letter, "paren_e": paren_e, "mark": mk,
                        "ds_E": best[1]["E_str"], "ds_DE": best[1]["DE_str"],
                        "ds_lineno": best[1]["lineno"], "diff": round(best[0], 4),
                    })
        if info["cands"]:
            plain = [c for c in info["cands"] if c["paren_e"] is None and not c["mark"]]
            info["min_plain_diff"] = min([c["diff"] for c in plain]) if plain else None
            info["min_any_diff"] = min([c["diff"] for c in info["cands"]])
        else:
            info["min_plain_diff"] = None
            info["min_any_diff"] = None
        rows.append(info)

    json.dump({"sha": sha(ADOPTED), "rows": rows},
              open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\eligible.json", "w"), indent=1)

    rows_sorted = sorted(rows, key=lambda r: (r["min_plain_diff"] is None, -(r["min_plain_diff"] or 0)))
    out = []
    out.append("=== Eligible levels ranked by distance to nearest plain-XREF dataset level ===")
    for r in rows_sorted:
        out.append(f"{r['lineno']:5d} E={r['E']:>11s} DE={r['DE']:>3s} nG={r['nG']} Q={r['Q']!r} "
                   f"minPlainDiff={r['min_plain_diff']} minAnyDiff={r['min_any_diff']} xref={r['xref']}")
        for c in r["cands"]:
            pr = f"({c['paren_e']}{c['mark']})" if c["paren_e"] is not None else ""
            out.append(f"        {c['letter']}{pr}: ds_E={c['ds_E']} ds_DE={c['ds_DE']} "
                       f"diff={c['diff']} (line {c['ds_lineno']})")

    print("minPlainDiff distribution:")
    vals = sorted([r["min_plain_diff"] for r in rows if r["min_plain_diff"] is not None], reverse=True)
    print("  max:", vals[0] if vals else None, " top10:", vals[:10])
    n_none = sum(1 for r in rows if r["min_plain_diff"] is None)
    print("  eligible levels with NO plain XREF letter (all parenthesized):", n_none)
    for r in rows:
        if r["min_plain_diff"] is None:
            print("   *", r["lineno"], r["E"], r["DE"], r["nG"], r["xref"], r["cands"])

    print("\n-- levels with plain-match diff > 0 --")
    for r in rows:
        d = r["min_plain_diff"]
        if d is not None and d > 0:
            print(f"  {r['lineno']:5d} E={r['E']} DE={r['DE']} nG={r['nG']} xref={r['xref']} minPlainDiff={d}")
            for c in r["cands"]:
                pr = f"({c['paren_e']}{c['mark']})" if c["paren_e"] is not None else ""
                print(f"        {c['letter']}{pr}: ds_E={c['ds_E']} ds_DE={c['ds_DE']} diff={c['diff']}")

    print("\n-- levels whose ONLY matches are parenthesized (documented off-energy) --")
    for r in rows:
        plain = [c for c in r["cands"] if c["paren_e"] is None and not c["mark"]]
        if not plain and r["cands"]:
            print(f"  {r['lineno']:5d} E={r['E']} DE={r['DE']} nG={r['nG']} xref={r['xref']}")
            for c in r["cands"]:
                pr = f"({c['paren_e']}{c['mark']})" if c["paren_e"] is not None else ""
                print(f"        {c['letter']}{pr}: ds_E={c['ds_E']} ds_DE={c['ds_DE']} diff={c['diff']}")

    with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\ranked.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
