from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path

PY = r"C:\Users\sun\AppData\Local\Programs\Python\Python311\python.exe"
JAVA_AVG = r".github\scripts\Java_Average.py"

UNIT_TO_S = {
    "FS": 1e-15,
    "PS": 1e-12,
    "NS": 1e-9,
    "US": 1e-6,
    "MS": 1e-3,
    "S": 1.0,
    "M": 60.0,
    "H": 3600.0,
    "D": 86400.0,
    "Y": 31557600.0,
}

LIFETIME_RE = re.compile(
    r"\|t\s*(?P<op>[=<>])\s*(?P<v>[0-9]+(?:\.[0-9]+)?(?:E[+-]?\d+)?)\s*(?P<u>FS|PS|NS|US|MS|S|M|H|D|Y)(?:\s*\{I(?P<unc>[^}]+)\})?",
    re.IGNORECASE,
)

POINT_RE = re.compile(
    r"(?P<v>[0-9]+(?:\.[0-9]+)?(?:E[+-]?\d+)?)\s*(?P<u>FS|PS|NS|US|MS|S|M|H|D|Y)(?:\s*\{I(?P<unc>[^}]+)\})",
    re.IGNORECASE,
)

SUGGESTED_RE = re.compile(
    r"suggested adopted result:\s*(?P<v>[0-9]+(?:\.[0-9]+)?)\((?P<unc>[0-9]+)\)\s*(?P<u>[A-Za-z]+)",
    re.IGNORECASE,
)


def get_payload(block):
    return " ".join(x["text"][9:].rstrip() for x in block)


def parse_t_field(ltext: str):
    t_raw = ltext[39:49].strip()
    dt_raw = ltext[49:55].strip()
    if not t_raw:
        return None, None, None
    parts = t_raw.split()
    if len(parts) < 2:
        return None, None, None
    try:
        t_val = float(parts[0])
        t_unit = parts[1].upper()
    except ValueError:
        return None, None, None
    return t_val, t_unit, dt_raw


def unc_abs(value_token: str, unc_digits: str):
    if not unc_digits or not unc_digits.isdigit():
        return None
    tok = value_token.upper()
    exp = 0
    if "E" in tok:
        base, e = tok.split("E")
        exp = int(e)
    else:
        base = tok
    dec = len(base.split(".")[1]) if "." in base else 0
    return int(unc_digits) * (10 ** (exp - dec))


def to_seconds(v: float, u: str):
    return v * UNIT_TO_S[u]


def from_seconds(vs: float, u: str):
    return vs / UNIT_TO_S[u]


def dt_digits_from_abs(dabs: float, t_display: str):
    if "." in t_display:
        dec = len(t_display.split(".")[1])
    else:
        dec = 0
    raw = dabs * (10 ** dec)
    # nearest integer for comparison reporting; final ENSDF rounding rule checked manually if needed
    return int(round(raw)), dec


def main():
    data = json.loads(Path(".github/temp/2026-04-27_cl34_t_checks/cl34_t_blocks.json").read_text(encoding="utf-8"))

    check1 = []
    check2 = []
    check3 = []

    for rec in data:
        l = rec["L"]
        if not l:
            continue
        payload = get_payload(rec["block"])
        if "cL T$" not in rec["block"][0]["text"]:
            continue

        m_tau = LIFETIME_RE.search(payload)
        if not m_tau:
            continue

        op = m_tau.group("op")
        tau_v = float(m_tau.group("v"))
        tau_u = m_tau.group("u").upper()
        tau_unc = m_tau.group("unc")

        # CHECK 1: quoted values in average clause must have units+uncertainties
        if "average of" in payload.lower():
            avg_seg = re.split(r"average of", payload, flags=re.IGNORECASE, maxsplit=1)[1]
            avg_seg = re.split(r"\bOther[s]?:", avg_seg, flags=re.IGNORECASE, maxsplit=1)[0]

            # finite value tokens with unit in average segment (with or without uncertainty)
            # Require at least one space between value and unit to avoid false matches in NSR keys like 1977Da02.
            bare_vals = re.findall(
                r"([0-9]+(?:\.[0-9]+)?(?:E[+-]?\d+)?)\s+(FS|PS|NS|US|MS|S|M|H|D|Y)(?!\s*\{I)",
                avg_seg,
                flags=re.IGNORECASE,
            )
            # ignore limits (>x unit, <x unit)
            for vtok, utok in bare_vals:
                pat = re.escape(vtok) + r"\s*" + re.escape(utok)
                idx = re.search(pat, avg_seg, flags=re.IGNORECASE)
                if idx:
                    pre = avg_seg[max(0, idx.start()-2):idx.start()]
                    if ">" in pre or "<" in pre:
                        continue
                check1.append((l["line"], rec["block"][0]["line"], f"missing uncertainty: {vtok} {utok}"))

        # CHECK 2: averaged result in cL T comment using Java_Average.py
        if "average of" in payload.lower() and op == "=":
            cmd = [PY, JAVA_AVG, "--comment", payload]
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            out = proc.stdout + "\n" + proc.stderr
            m_s = SUGGESTED_RE.search(out)
            if not m_s:
                check2.append((l["line"], rec["block"][0]["line"], "PARSE_FAIL", "Java_Average suggested result not found"))
            else:
                s_v = float(m_s.group("v"))
                s_u = m_s.group("u").upper()
                s_unc_digits = m_s.group("unc")
                status = "OK"
                notes = []
                if s_u != tau_u:
                    # compare in seconds if units differ
                    tau_s = to_seconds(tau_v, tau_u)
                    sug_s = to_seconds(s_v, s_u)
                    if abs(tau_s - sug_s) > 1e-18:
                        status = "MISMATCH"
                        notes.append(f"tau value {tau_v} {tau_u} vs Java {s_v} {s_u}")
                else:
                    if abs(tau_v - s_v) > (0.5 * (10 ** (-3))):
                        status = "MISMATCH"
                        notes.append(f"tau value {tau_v} {tau_u} vs Java {s_v} {s_u}")

                if tau_unc and tau_unc.isdigit():
                    if tau_unc != s_unc_digits:
                        status = "MISMATCH"
                        notes.append(f"tau unc {tau_unc} vs Java {s_unc_digits}")

                check2.append((l["line"], rec["block"][0]["line"], status, "; ".join(notes) if notes else f"matches Java {s_v}({s_unc_digits}) {s_u}"))

        # CHECK 3: ln2 conversion from cL lifetime to L-record T field
        if op == "=":
            t_val, t_unit, dt_raw = parse_t_field(l["text"])
            if t_val is None:
                check3.append((l["line"], rec["block"][0]["line"], "SKIP", "missing/invalid T field"))
                continue

            half_s = math.log(2.0) * to_seconds(tau_v, tau_u)
            half_in_tunit = from_seconds(half_s, t_unit)

            t_display = l["text"][39:49].strip().split()[0]
            if "." in t_display:
                dec = len(t_display.split(".")[1])
                tol = 0.5 * (10 ** (-dec))
            else:
                tol = 0.5

            delta = abs(half_in_tunit - t_val)
            status = "OK" if delta <= tol else "MISMATCH"
            note = f"T={t_val:g} {t_unit}; ln2*tau={half_in_tunit:.6g} {t_unit}; tol={tol:g}"

            # optional DT check for symmetric numeric uncertainty
            if tau_unc and tau_unc.isdigit() and dt_raw and dt_raw.isdigit():
                tau_dabs = unc_abs(m_tau.group("v"), tau_unc)
                if tau_dabs is not None:
                    dhalf = math.log(2.0) * to_seconds(tau_dabs, tau_u)
                    dhalf_in_tunit = from_seconds(dhalf, t_unit)
                    dt_digits_calc, _ = dt_digits_from_abs(dhalf_in_tunit, t_display)
                    note += f"; DT={dt_raw} vs ln2*dTau~{dt_digits_calc}"
                    # Uncertainty-aware consistency: if T is within ln2*tau ± ln2*dtau, treat as consistent.
                    if delta <= max(tol, dhalf_in_tunit):
                        status = "OK"

            check3.append((l["line"], rec["block"][0]["line"], status, note))

    out = Path(".github/temp/2026-04-27_cl34_t_checks/cl34_t_lifetime_checks.txt")
    with out.open("w", encoding="utf-8") as f:
        f.write("CHECK 1: quoted lifetime values/units/uncertainties in average clauses\n")
        if not check1:
            f.write("  NONE\n")
        else:
            for x in check1:
                f.write(f"  L{x[0]} cL{x[1]}: {x[2]}\n")

        f.write("\nCHECK 2: averaged results in cL T comments (vs Java_Average)\n")
        for x in check2:
            f.write(f"  L{x[0]} cL{x[1]} [{x[2]}] {x[3]}\n")

        f.write("\nCHECK 3: ln2 conversion from cL lifetime to L-record T field\n")
        for x in check3:
            f.write(f"  L{x[0]} cL{x[1]} [{x[2]}] {x[3]}\n")

    print(f"wrote {out}")
    print(f"check1_findings={len(check1)}")
    print(f"check2_total={len(check2)}, mismatches={sum(1 for x in check2 if x[2]=='MISMATCH')}")
    print(f"check3_total={len(check3)}, mismatches={sum(1 for x in check3 if x[2]=='MISMATCH')}")


if __name__ == "__main__":
    main()
