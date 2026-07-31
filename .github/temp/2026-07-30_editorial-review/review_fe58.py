#!/usr/bin/env python3
"""
Editorial review of comment records in all 58Fe datasets.
Implements error classes from .github/skills/editorial-review-guidelines/SKILL.md
Check-Only. Report findings.
"""

import re
import os
import glob

# All 58Fe dataset files
BASE = r"d:\X\ND\ENSDF\XUNDL\A58\Fe58\old"
FILES = sorted(glob.glob(os.path.join(BASE, "Fe58_*.ens")))

ELEMENT_SYMBOLS = set("""H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn
Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe
Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi
Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn
Nh Fl Mc Lv Ts Og""".split())


def is_comment_line(line):
    if len(line) < 8:
        return False
    return line[6] == 'c'


def get_first_data_line(lines):
    """0-based index of first L/G/E/B/DP/PN data record."""
    for i, line in enumerate(lines):
        if len(line) < 9:
            continue
        col6, col7, col8 = line[5], line[6], line[7]
        col9 = line[8] if len(line) > 8 else ' '
        if col7 == ' ' and col8 in ('L', 'G', 'E', 'B'):
            return i
        if col7 == ' ' and col8 == 'P' and col9 == 'N':
            return i
        if col7 == ' ' and col8 == 'D' and col9 == 'P':
            return i
        if col7 == ' ' and col8 == 'N':
            return i
    return len(lines)


def scan_file(filepath):
    errors = []
    short = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    first_data = get_first_data_line(lines)

    for i, line in enumerate(lines):
        ln = i + 1
        raw = line.rstrip('\n\r')
        if not is_comment_line(raw):
            continue

        is_top = i < first_data
        text = raw[9:] if len(raw) > 9 else ''
        col8 = raw[7] if len(raw) > 7 else ' '
        ctype = f"c{col8}" if col8 != ' ' else 'c'

        # ---- 1. ENSDF Notation ----

        # 1a. superscript wrapping: {+56Sc} should be {+56}Sc
        for m in re.finditer(r'\{\+\d+[A-Z][a-z]?', text):
            errors.append((short, ln, "Superscript-Notation",
                f"Element inside superscript braces: {extract(text, m.start())}",
                "Close braces after mass number", "`{+n}` wraps only mass number"))

        # 1b. plain isotope tokens
        for m in re.finditer(r'(?<!\{\+)\b(\d{1,3})([A-Z][a-z]?)\b', text):
            num, elem = m.group(1), m.group(2)
            if elem in ELEMENT_SYMBOLS:
                after = text[m.end():m.end()+1] if m.end() < len(text) else ''
                if after != '|' and after != ',' and after != ')':
                    errors.append((short, ln, "Isotope-Notation",
                        f"Plain isotope '{num}{elem}': {extract(text, m.start())}",
                        f"{{+{num}}}{elem}", "Isotope needs {+n} wrapping"))

        # 1c. Unicode leakage
        for j, ch in enumerate(raw):
            if ord(ch) > 127:
                errors.append((short, ln, "Unicode-Leakage",
                    f"Non-ASCII U+{ord(ch):04X}: {extract(raw, j)}",
                    "Use ENSDF | escape", "Raw Unicode not allowed"))
                break

        # 1d. Missing {I}
        for m in re.finditer(r'(?<![\{I=])I(\d{1,3})\b', text):
            pre = text[max(0, m.start()-6):m.start()]
            if '{' not in pre and re.search(r'[=\s]', pre):
                errors.append((short, ln, "Missing-{I}",
                    f"Bare I{m.group(1)}: {extract(text, m.start())}",
                    f"{{I{m.group(1)}}}", "Uncertainty needs {I} braces"))

        # 1e. non-ENSDF unit spellings
        for pat, wrong, correct in [
            (r'(?<!\{)\bcm2\b(?!\})', 'cm2', 'cm{+2}'),
            (r'(?<!\{)\bmg/cm2\b(?!\})', 'mg/cm2', 'mg/cm{+2}'),
            (r'(?<!\{)\bg/cm2\b(?!\})', 'g/cm2', 'g/cm{+2}'),
            (r'(?<!\|)\bug\b', 'ug', '|mg'),
        ]:
            for m in re.finditer(pat, text):
                errors.append((short, ln, "Non-ENSDF-Units",
                    f"'{wrong}': {extract(text, m.start())}", correct,
                    "Use ENSDF unit notation"))

        # 1f. mixed symbol-text (raw greek/mu)
        for m in re.finditer(r'[γμ]', text):
            errors.append((short, ln, "Symbol-Text-Mix",
                f"Raw '{m.group()}' char: {extract(text, m.start())}",
                "Use |g or |m", "No raw Greek glyphs"))

        # 1g. leaked record tags in cols 10-80
        body = text
        for m in re.finditer(r'\s(cL|cG|cB|cE|cN|cP)\s|\sL\s|\sG\s', body):
            errors.append((short, ln, "Leaked-Tag",
                f"Spurious tag '{m.group().strip()}': {extract(body, m.start())}",
                "Remove stray record tag", "Copy-paste artifact"))

        # 1h. inconsistent subscripts A6= (missing {-n})
        for m in re.finditer(r'\b([A-Z][a-z]?)(\d+)=', text):
            if not text[max(0, m.start()-20):m.start()].endswith('}'):
                errors.append((short, ln, "Subscript-Notation",
                    f"'{m.group(1)}{m.group(2)}=' no subscript: {extract(text, m.start())}",
                    f"Verify subscript", "Indexed variables need {-n}"))

        # ---- 2. Grammar and Style ----

        # 2a. capitalization for $field$ comments (record-specific, not top-block)
        fm = re.match(r'^\s*\$?([A-Za-z0-9(),]+)\$(.*)', text)
        if fm and not is_top and ctype not in ('cN', 'cP'):
            field, rest = fm.group(1), fm.group(2).strip()
            if rest and rest[0].isupper():
                first = rest.split()[0] if rest.split() else ''
                acronyms = ('E1','E2','M1','M2','D','Q','O','B(E2)','R(','RUL','VS-',
                            'From','RDDS','L(t,p)','L(d,p)','L(p,p\'','ECIS','NSR',
                            'A2','A4','GXPF','BM1W','BE2W','BE2','BM2','Fig','Table')
                if not (first[0].isdigit() or first.startswith(('{','|')) or
                        any(first.startswith(a) for a in acronyms)):
                    errors.append((short, ln, "Capitalization",
                        f"{ctype} {field}$ starts uppercase '{first}': {extract(text, fm.start())}",
                        f"Lowercase after {field}$",
                        "Record-specific $field$ comments lowercase"))

        # 2b. NUCID case
        nucid = raw[:5]
        if re.search(r'[a-z]', nucid):
            errors.append((short, ln, "NUCID-Case", f"NUCID '{nucid}'",
                f"'{nucid.upper()}'", "NUCID must be uppercase"))

        # 2c. extra space after $
        for m in re.finditer(r'\$ +(\S)', text):
            pre = text[max(0, m.start()-6):m.start()]
            if re.search(r'[A-Za-z0-9,()]+\$$', pre):
                errors.append((short, ln, "Extra-Space-After-$",
                    f"'$ {m.group(1)}': {extract(text, m.start())}",
                    f"'${m.group(1)}'", "No space after $"))

        # 2d. dittography
        for m in re.finditer(r'\b(\w+)\s+\1\b', text, re.IGNORECASE):
            if len(m.group(1)) > 2:
                errors.append((short, ln, "Dittography",
                    f"'{m.group(1)} {m.group(1)}': {extract(text, m.start())}",
                    f"Remove duplicate '{m.group(1)}'", "Repeated word"))

        # ---- 3. Punctuation ----
        if len(re.findall(r'\band\b', text)) > 1 and len(re.findall(r',', text)) >= len(re.findall(r'\band\b', text)):
            errors.append((short, ln, "Oxford-Comma",
                f"Multiple 'and': {text[:50]}", "Oxford comma, one 'and'",
                "List punctuation"))

        # ---- 4. Hyphenation ----
        if re.search(r'\bhalf life\b', text, re.IGNORECASE):
            errors.append((short, ln, "Hyphenation", "'half life'",
                "'half-life'", "Always hyphenate"))
        if re.search(r'\bL transfer', text, re.IGNORECASE):
            errors.append((short, ln, "Hyphenation", "'L transfer'",
                "'L-transfer'", "Always hyphenate"))

        # ---- 5. Spelling ----
        spell = {
            'deexiting': 'deexciting', 'multiporities': 'multipolarities',
            'multipority': 'multipolarity', 'grand-daughter': 'granddaughter',
            'grand daughter': 'granddaughter', 'ohter': 'other', 'usign': 'using',
            'stoped': 'stopped', 'coeffcients': 'coefficients',
            'novelly designed': 'newly designed', 'superseeds': 'supersedes',
            'superseed': 'supersede', 'evaluatord': 'evaluators',
            'neutrom': 'neutron', 'striped': 'stripped',
            'Van der Graaff': 'Van de Graaff', 'Van de Graaf': 'Van de Graaff',
            'Van der Graaf': 'Van de Graaff', 'Cockroft-Walton': 'Cockcroft-Walton',
            'memebr': 'member', 'brances': 'branches', 'explictiy': 'explicitly',
            'multiplicity' : 'multiplicity', 'states. ' : '',
        }
        for wrong, correct in spell.items():
            for m in re.finditer(re.escape(wrong), text, re.IGNORECASE):
                errors.append((short, ln, "Spelling",
                    f"'{m.group()}': {extract(text, m.start())}",
                    f"'{correct}'", "Misspelling"))

        # ---- 6. Text Integrity ----
        for m in re.finditer(r'=\s+(\d)', text):
            errors.append((short, ln, "Extra-Space-After-=",
                f"'= {m.group(1)}': {extract(text, m.start())}",
                f"='{m.group(1)}'", "No space after ="))
        for m in re.finditer(r'\{I[^}]+\}([a-z])', text):
            errors.append((short, ln, "Missing-Space",
                f"No space after {m.group()}: {extract(text, m.start())}",
                f"{m.group()} {m.group(1)}", "Space after {I...}"))
        # space within number: =NN NN pattern
        for m in re.finditer(r'=\d{2,4}\s+\d{2,4}\b', text):
            errors.append((short, ln, "Space-In-Number",
                f"Split number: {extract(text, m.start())}",
                "Verify digits", "Possible missing digit"))

    return errors


def extract(text, pos, w=28):
    s = max(0, pos - w)
    e = min(len(text), pos + w)
    ctx = text[s:e]
    if s > 0:
        ctx = '...' + ctx
    if e < len(text):
        ctx = ctx + '...'
    return ctx


def main():
    all_errors = []
    for fp in FILES:
        if os.path.exists(fp):
            all_errors.extend(scan_file(fp))

    # dedupe
    seen = set()
    uniq = []
    for e in all_errors:
        k = (e[0], e[1], e[2], e[3][:35])
        if k not in seen:
            seen.add(k)
            uniq.append(e)
    uniq.sort(key=lambda x: (x[0], x[1]))

    print(f"Files scanned: {len(FILES)}")
    print(f"Total findings: {len(uniq)}\n")
    print("| File | Line | Category | Current Text | Recommended | Rationale |")
    print("|------|------|----------|-------------|-------------|-----------|")
    for e in uniq:
        fname, line, cat, curr, rec, rat = e
        esc = lambda s: s.replace('|', '\\|').replace('\n', ' ')[:80]
        print(f"| {fname} | {line} | {cat} | {esc(curr)} | {esc(rec)[:60]} | {esc(rat)[:60]} |")


if __name__ == '__main__':
    main()
