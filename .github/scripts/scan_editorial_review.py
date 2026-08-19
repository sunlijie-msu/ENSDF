#!/usr/bin/env python3
"""Editorial-review scanner for ENSDF comment lines (check-only).

Sweeps c/cL/cG/cB/cE/cN/cP/cQ comment records for the error classes defined
in .github/skills/editorial-review-guidelines/SKILL.md. Reports findings
grouped by file; never edits files.

Usage:
  python .github/scripts/scan_editorial_review.py [PATH] [--skip PAT ...]

PATH:  an .ens file or a folder (scans *.ens). Default: current folder.
--skip: exclude filenames containing any PAT (e.g. --skip adopted).

Exit code 0 = no findings; 1 = findings found.
"""

import argparse
import glob
import os
import re
import sys

# --------------------------------------------------------------------------
# Element symbols, full periodic table Z=1-118 (for isotope / formula checks)
# --------------------------------------------------------------------------
ELEMENTS = set("""
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu
Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs
Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl
Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg
Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og
""".split())

# Common misspellings seen in ENSDF comments
SPELLINGS = [
    "uisng", "usign", "uising", "deexiting", "multiporities", "grand-daughter",
    "ohter", "stoped", "striped", "coeffcients", "magmtude", "forils",
    "varible", "cloride", "hyphotheses", "analsyis", "atazimuthal",
    "van der graaff", "van de graaf", "cockroft-walton", "branchi ng",
    "aslo", "phosphorous",
]

# --------------------------------------------------------------------------
# Regex checks: (category, pattern)
# Patterns run on comment text (starting column 10).
# --------------------------------------------------------------------------
CHECKS = [
    ("unicode",              r"[^\x00-\x7F]"),
    ("isotope",              r"(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b"),  # 34S, 4He
    ("bare-I",               r"(?<!\{)\bI\d{1,3}\b"),              # I5, not {I5}
    ("chem-formula",         r"[A-Z][a-z]?\d+"),                  # H3 in H3BO3, C6 in C6Cl6
    ("unit-ug",              r"\bug\b"),
    ("unit-cm2",             r"(?<!\{)\bcm2\b"),
    ("unit-cm3",             r"(?<!\{)\bcm3\b"),
    ("unit-mgcm2",           r"\bmg/cm2\b"),
    ("unit-um",              r"\bum\b"),
    ("neg-exp10",            r"10\{-\d+\}"),
    ("eq-space",             r"=\s[+\-0-9]"),
    ("dollar-space",         r"\$\s"),
    ("dittography",          r"\b(\w+)\s+\1\b"),
    ("leaked-tag",           r"\s(cL|cG|cB|cE|cN|cP|cQ)\s"),
]

# Categories needing element validation before reporting
ELEM_CHECKED = {"isotope", "chem-formula"}


def is_comment(line):
    """True for comment records: column 7 == 'c' (incl. 2c/3c continuations)."""
    return len(line) > 7 and line[6] == "c"


def nucid_case_error(line):
    """NUCID (cols 1-5) element letters must be uppercase; None if OK."""
    nucid = line[:5]
    return nucid if any(c.islower() for c in nucid) else None


def elem_of(token):
    """Element symbol of an isotope (34S) or formula (H3) token, or None."""
    m = re.match(r"^(\d+)([A-Z][a-z]?)$", token)
    if m:
        return m.group(2)  # isotope: digits then element
    m = re.match(r"^([A-Z][a-z]?)(\d+)$", token)
    return m.group(1) if m else None  # formula: element then digits


def in_nsr_key(text, start):
    """True if token at `start` is the element part of an NSR key (1985Ra15)."""
    before = text[max(0, start - 4):start]
    return len(before) == 4 and before.isdigit()


def scan_line(text):
    """Yield (category, match) for one comment line's text."""
    for cat, pat in CHECKS:
        for m in re.finditer(pat, text):
            tok = m.group(0)
            if cat in ELEM_CHECKED:
                el = elem_of(tok)
                if el is None or el not in ELEMENTS:
                    continue
            # chemical formula: exclude NSR keys (1985Ra15), braced {I15},
            # and all-caps acronyms/code names (CHUCK3, DWUCK4, GXPF1A)
            prev = text[m.start() - 1] if m.start() > 0 else " "
            prev2 = text[m.start() - 2] if m.start() > 1 else " "
            if cat == "chem-formula" and (in_nsr_key(text, m.start()) or
                                          prev in "{+" or
                                          (prev.isupper() and prev2.isupper())):
                continue
            # NOTE: instrument names (S800, K1200, CH89) still match
            # chem-formula/isotope — flagged for manual review by design.
            # exclude bare-I matches that are inside {I...} (paranoia for
            # lookbehind edge cases) and isotope tokens followed by '|'
            if cat == "bare-I" and text[max(0, m.start() - 1)] == "{":
                continue
            if cat == "isotope" and m.end() < len(text) and text[m.end()] == "|":
                continue
            yield cat, tok
    for word in SPELLINGS:
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            yield "spelling", word


def scan_file(path):
    """Return list of (lineno, category, token, context) findings."""
    findings = []
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n").rstrip("\r")
        if not is_comment(line):
            continue
        bad_nucid = nucid_case_error(line)
        if bad_nucid:
            findings.append((i, "nucid-case", bad_nucid, line.strip()[:72]))
        text = line[9:]  # comment text starts at column 10
        for cat, tok in scan_line(text):
            findings.append((i, cat, tok, text.strip()[:72]))
    return findings


# --------------------------------------------------------------------------
# Self-test: regression guard, run with --selftest (no files touched)
# --------------------------------------------------------------------------
_SELFTEST_CASES = [
    # (text, category, expect_match: bool)
    ("0.025 e{+2}b{+2} {I4} to 0.0263", "bare-I", False),
    ("|d=+0.05 I5", "bare-I", True),
    ("A{-2}=0.5 A6=-0.1", "isotope", False),
    ("16-18-MeV 4He beams", "isotope", True),
    ("1985Ra15 gives 0.220", "chem-formula", False),
    ("CHUCK3-CCBA analyses", "chem-formula", False),
    ("Targets were mixtures of H3BO3", "chem-formula", True),
    ("NaCl, CsI, GaP, MgO", "chem-formula", False),
    ("the target was 400 ug/cm2", "unit-ug", True),
    ("1500 um thick", "unit-um", True),
    ("1500-|mm-thick", "unit-um", False),
    ("mixtures of of H3BO3", "dittography", True),
    ("cL J$ from ...", "dollar-space", True),
    ("|w|g= 0.45", "eq-space", True),
    ("|w|g= +0.45", "eq-space", True),
    ("10{-3}", "neg-exp10", True),
    ("10{+-3}", "neg-exp10", False),
    ("with 2I|g = 0.5", "isotope", False),
]


def run_selftest():
    """Assert each _SELFTEST_CASES expectation; print PASS/FAIL, no file I/O."""
    failed = 0
    for text, cat, expect in _SELFTEST_CASES:
        got = any(c == cat for c, _ in scan_line(text))
        ok = got == expect
        print(f"{'PASS' if ok else 'FAIL'}  [{cat:13s}] expect={expect!s:5s} got={got!s:5s} | {text!r}")
        failed += not ok
    nucid_ok = nucid_case_error(" 34S ") is None and nucid_case_error(" 34Si") is not None
    print(f"{'PASS' if nucid_ok else 'FAIL'}  [nucid-case   ] uppercase/lowercase NUCID discrimination")
    failed += not nucid_ok
    print(f"\nSELFTEST: {len(_SELFTEST_CASES) + 1 - failed}/{len(_SELFTEST_CASES) + 1} passed")
    return failed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", default=".", help=".ens file or folder")
    ap.add_argument("--skip", nargs="*", default=[], help="exclude matching filenames")
    ap.add_argument("--selftest", action="store_true", help="run regression guard, exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return 1 if run_selftest() else 0

    if os.path.isdir(args.path):
        files = sorted(glob.glob(os.path.join(args.path, "*.ens")))
    else:
        files = [args.path]

    total = 0
    for fp in files:
        if any(s in os.path.basename(fp) for s in args.skip):
            continue
        finds = scan_file(fp)
        if not finds:
            continue
        total += len(finds)
        print(f"=== {os.path.basename(fp)} ({len(finds)}) ===")
        for ln, cat, tok, ctx in finds:
            print(f"  L{ln:4d} [{cat:13s}] {tok!r} | {ctx}")
    print(f"\nTOTAL FINDINGS: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
