import os, re, glob

# All S34 dataset files except adopted
folder = r"d:\X\ND\ENSDF\A34\S34\new"
files = [f for f in sorted(glob.glob(os.path.join(folder, "*.ens")))
         if os.path.basename(f).lower() != "s34_adopted.ens"]

# Error class patterns
checks = {
    "plain-isotope": r"(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b",
    "ug": r"\bug\b",
    "cm2": r"(?<!\{)\bcm2\b",
    "mgcm2": r"\bmg/cm2\b",
    "um": r"\b\d+-\s?um\b",
    "ditto": r"\b(\w+)\s+\1\b",
    "dollars-space": r"\$\s",
    "eq-space": r"=\s[0-9]",
    "neg-exp10": r"10\{-\d+\}",
    "unicode": r"[^\x00-\x7F]",
    "mixed": r"(?<![|{])(?<![{+0-9])([|g]|y|b)-ray|\bum\b|(?:[a-z]|[A-Z])\d{2,3}\b",
}

# Manual spelling list
spell = ["uisng", "usign", "stoped", "aslo", "analsyis", "magmtude", "varible",
         "deexite", "deexiting", "multiporities", "coeffcients", "van der graaff",
         "van de graaf", "cockroft-walton", "atazimuthal", "forils", "4he",
         "of of"]

# Valid element symbols (subset) to avoid false positives in plain-isotope
elems = set("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split())

isotope_re = re.compile(r"(?<!\{\+)\b(\d{1,3})([A-Z][a-z]?)\b")

def is_elem(sym):
    return sym in elems

total = 0
for fp in files:
    name = os.path.basename(fp)
    findings = []
    with open(fp, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n").rstrip("\r")
        if len(line) < 8:
            continue
        # only comment records: col 7 == 'c' (cL, cG, cB, cE, cN, cP, cQ) or continuation 2c/3c
        cont = line[5] if len(line) > 5 else " "
        typ = line[6] if len(line) > 6 else " "
        if not (typ == "c" or (cont.isalnum() and typ == "c")):
            continue
        body = line[9:]
        # plain isotope
        for m in isotope_re.finditer(body):
            num, sym = m.group(1), m.group(2)
            if is_elem(sym):
                findings.append((i, "isotope", m.group(0)))
        # ug
        for m in re.finditer(r"\bug\b", body):
            findings.append((i, "ug", m.group(0)))
        # cm2 unbraced
        for m in re.finditer(r"(?<!\{)\bcm2\b", body):
            findings.append((i, "cm2", m.group(0)))
        # mg/cm2
        for m in re.finditer(r"\bmg/cm2\b", body):
            findings.append((i, "mgcm2", m.group(0)))
        # um
        for m in re.finditer(r"\b\d+-\s?um\b", body):
            findings.append((i, "um", m.group(0)))
        # ditto
        for m in re.finditer(r"\b(\w+)\s+\1\b", body):
            findings.append((i, "ditto", m.group(0)))
        # dollars space
        for m in re.finditer(r"\$\s", body):
            findings.append((i, "dollars-space", m.group(0)))
        # eq space
        for m in re.finditer(r"=\s[0-9]", body):
            findings.append((i, "eq-space", m.group(0)))
        # 10{-n}
        for m in re.finditer(r"10\{-\d+\}", body):
            findings.append((i, "neg-exp10", m.group(0)))
        # unicode
        for m in re.finditer(r"[^\x00-\x7F]", body):
            findings.append((i, "unicode", m.group(0)))
        # spelling
        for w in spell:
            if re.search(r"\b" + re.escape(w) + r"\b", body):
                findings.append((i, "spell:"+w, w))
    if findings:
        total += len(findings)
        print(f"=== {name} ({len(findings)}) ===")
        for ln, cat, txt in findings:
            print(f"  L{ln} [{cat}] {txt} | {lines[ln-1].rstrip()[:80]}")

print(f"\nTOTAL: {total}")
