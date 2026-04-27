from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

UNITS = ["FS", "PS", "NS", "US", "MS", "S", "M", "H", "D", "Y"]
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

VAL_RE = re.compile(r"(?P<v>[0-9]+(?:\.[0-9]+)?(?:E[+-]?\d+)?)\s*(?P<u>FS|PS|NS|US|MS|S|M|H|D|Y)(?:\s*\{I(?P<unc>[^}]+)\})?", re.IGNORECASE)


@dataclass
class ParsedValue:
    value: float
    unit: str
    unc_digits: Optional[str]
    value_token: str


def parse_value_token(token: str, unit: str, unc: Optional[str]) -> ParsedValue:
    return ParsedValue(value=float(token), unit=unit.upper(), unc_digits=unc, value_token=token)


def unc_abs_in_unit(value_token: str, unc_digits: str) -> Optional[float]:
    # supports symmetric integer uncertainties only
    if not unc_digits or not unc_digits.isdigit():
        return None

    token = value_token.upper()
    exp = 0
    if "E" in token:
        base, e = token.split("E")
        exp = int(e)
    else:
        base = token

    if "." in base:
        decimals = len(base.split(".")[1])
    else:
        decimals = 0

    return int(unc_digits) * (10 ** (exp - decimals))


def to_seconds(v: float, unit: str) -> float:
    return v * UNIT_TO_S[unit]


def from_seconds(vs: float, unit: str) -> float:
    return vs / UNIT_TO_S[unit]


def parse_t_field(t_field: str) -> tuple[Optional[float], Optional[str]]:
    t = t_field.strip()
    if not t:
        return None, None
    parts = t.split()
    if len(parts) < 2:
        return None, None
    try:
        return float(parts[0]), parts[1].upper()
    except ValueError:
        return None, None


def main() -> None:
    blocks = json.loads(Path(".github/temp/2026-04-27_cl34_t_checks/cl34_t_blocks.json").read_text(encoding="utf-8"))

    missing_unc_findings = []
    weighted_findings = []
    conversion_findings = []

    for rec in blocks:
        l = rec["L"]
        if not l:
            continue

        l_line = l["line"]
        t_val, t_unit = parse_t_field(l["T"])

        # merge block comment text payload only (drop cols 1-9)
        comment_payload = " ".join(x["text"][9:].rstrip() for x in rec["block"]).replace("  ", " ")

        # find quoted values in comment payload
        vals = [parse_value_token(m.group("v"), m.group("u"), m.group("unc")) for m in VAL_RE.finditer(comment_payload)]

        for pv in vals:
            # finite value should carry uncertainty if not explicitly a limit nearby
            if pv.unc_digits is None:
                # skip if token is part of explicit limit pattern like '>1.8 ps' or '<3 fs'
                lim_pat = re.escape(pv.value_token) + r"\s*" + re.escape(pv.unit)
                idx = comment_payload.find(f"{pv.value_token} {pv.unit}")
                window = comment_payload[max(0, idx - 2): idx] if idx >= 0 else ""
                if ">" in window or "<" in window:
                    continue
                missing_unc_findings.append((l_line, rec["block"][0]["line"], f"{pv.value_token} {pv.unit}"))

        if "weighted average of" not in comment_payload.lower():
            continue

        # Weighted average check from quoted finite values with symmetric uncertainties only
        usable = []
        for pv in vals:
            unc_abs = unc_abs_in_unit(pv.value_token, pv.unc_digits or "")
            if unc_abs is None:
                continue
            usable.append((pv.value, unc_abs, pv.unit, pv.unc_digits, pv.value_token))

        # Need at least 2 points and same unit family by conversion through seconds
        if len(usable) < 2:
            weighted_findings.append((l_line, rec["block"][0]["line"], "SKIP", "<2 symmetric values"))
            continue

        xs = []
        sigs = []
        for v, u, unit, _, _ in usable:
            xs.append(to_seconds(v, unit))
            sigs.append(to_seconds(u, unit))

        # weighted mean in seconds
        try:
            wsum = sum(1.0 / (s * s) for s in sigs if s > 0)
            if wsum == 0:
                weighted_findings.append((l_line, rec["block"][0]["line"], "SKIP", "zero weight"))
                continue
            mean_s = sum(x / (s * s) for x, s in zip(xs, sigs)) / wsum
            dmean_s = math.sqrt(1.0 / wsum)
        except ZeroDivisionError:
            weighted_findings.append((l_line, rec["block"][0]["line"], "SKIP", "zero sigma"))
            continue

        weighted_findings.append((l_line, rec["block"][0]["line"], "OK", f"tau_wt={mean_s:.6e}s, dtau={dmean_s:.2e}s"))

        # ln(2) conversion check against T field
        if t_val is None or not t_unit:
            conversion_findings.append((l_line, rec["block"][0]["line"], "SKIP", "missing T field"))
            continue

        half_s = math.log(2.0) * mean_s
        t_from_comment_in_tunit = from_seconds(half_s, t_unit)

        # tolerance: half of T-field last decimal place
        t_str = l["T"].strip().split()[0]
        if "." in t_str:
            dec = len(t_str.split(".")[1])
            tol = 0.5 * (10 ** (-dec))
        else:
            tol = 0.5

        delta = abs(t_from_comment_in_tunit - t_val)
        status = "OK" if delta <= tol else "MISMATCH"
        conversion_findings.append(
            (
                l_line,
                rec["block"][0]["line"],
                status,
                f"T_field={t_val:g} {t_unit}; ln2*tau_wt={t_from_comment_in_tunit:.6g} {t_unit}; delta={delta:.3g}; tol={tol:g}",
            )
        )

    report = Path(".github/temp/2026-04-27_cl34_t_checks/cl34_t_report.txt")
    with report.open("w", encoding="utf-8") as f:
        f.write("CHECK 1: Missing uncertainty on quoted finite values\n")
        if not missing_unc_findings:
            f.write("  NONE\n")
        else:
            for x in missing_unc_findings:
                f.write(f"  L{x[0]} cL{x[1]} -> {x[2]}\n")

        f.write("\nCHECK 2: Weighted-average parse\n")
        for x in weighted_findings:
            f.write(f"  L{x[0]} cL{x[1]} [{x[2]}] {x[3]}\n")

        f.write("\nCHECK 3: ln2 conversion against T field\n")
        for x in conversion_findings:
            f.write(f"  L{x[0]} cL{x[1]} [{x[2]}] {x[3]}\n")

    print(f"report written: {report}")
    print(f"missing_unc_findings={len(missing_unc_findings)}")
    print(f"weighted_blocks={len(weighted_findings)}")
    print(f"conversion_checks={len(conversion_findings)}")
    mm = [x for x in conversion_findings if x[2] == 'MISMATCH']
    print(f"conversion_mismatch={len(mm)}")


if __name__ == "__main__":
    main()
