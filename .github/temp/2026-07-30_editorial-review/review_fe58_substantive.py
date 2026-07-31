#!/usr/bin/env python3
"""
Substantive error scan for all 58Fe datasets.
Omit: minor capitalization, extra/missing single spaces.
Report: real spelling, dittography, data integrity, stray/double chars.
"""
import re, os, glob

BASE = r"d:\X\ND\ENSDF\XUNDL\A58\Fe58\old"
FILES = sorted(glob.glob(os.path.join(BASE, "*.ens")))

def extract(text, pos, w=28):
    s, e = max(0, pos-w), min(len(text), pos+w)
    ctx = text[s:e]
    return ('...' if s > 0 else '') + ctx + ('...' if e < len(text) else '')

def is_comment(line):
    return len(line) > 7 and line[6] == 'c'

def scan_file(fp):
    errs = []
    sn = os.path.basename(fp)
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        ln = i + 1
        raw = line.rstrip('\n\r')
        if not is_comment(raw):
            continue
        txt = raw[9:] if len(raw) > 9 else ''

        # Dittography
        for m in re.finditer(r'\b(\w+)\s+\1\b', txt, re.IGNORECASE):
            wd = m.group(1)
            if len(wd) > 2:
                errs.append((sn, ln, "Dittography",
                    f"'{wd} {wd}'", f"'{wd}'", "Repeated word"))

        # Real spelling errors
        sp = {
            'deexiting': 'deexciting', 'multiporities': 'multipolarities',
            'grand-daughter': 'granddaughter',
            'ohter': 'other', 'usign': 'using', 'stoped': 'stopped',
            'coeffcients': 'coefficients', 'novelly designed': 'newly designed',
            'superseeds': 'supersedes', 'evaluatord': 'evaluators',
            'neutrom': 'neutron',
            'memebr': 'member', 'brances': 'branches',
            'explictiy': 'explicitly',
        }
        for w, c in sp.items():
            for m in re.finditer(re.escape(w), txt, re.IGNORECASE):
                errs.append((sn, ln, "Spelling",
                    f"'{m.group()}'", f"'{c}'", "Misspelling"))

        # Stray double $$ in comment
        for m in re.finditer(r'\$\$', txt):
            errs.append((sn, ln, "Integrity",
                f"Double '$$': {extract(txt, m.start())}",
                "'$'", "Double dollar sign"))

        # Suspicious F prefix before ENSDF symbols
        for m in re.finditer(r'(?<=\$)([A-Z])(\|DJ=|\|g\()', txt):
            errs.append((sn, ln, "Integrity",
                f"Stray '{m.group(1)}' before {m.group(2)}: {extract(txt, m.start())}",
                f"Remove '{m.group(1)}'", "Stray character"))

        # Missing space after ) before word
        for m in re.finditer(r'\)([a-z])', txt):
            errs.append((sn, ln, "Missing-Space",
                f"'){m.group(1)}': {extract(txt, m.start())}",
                f"') {m.group(1)}'", "Missing space after )"))

        # g.s; missing period
        if re.search(r'\bg\.s;', txt):
            errs.append((sn, ln, "Punctuation",
                f"'g.s;'", "'g.s.;' or 'g.s. ;'", "Missing period in abbreviation"))

        # de-exciting vs deexciting consistency
        if re.search(r'\bde-exciting\b', txt):
            errs.append((sn, ln, "Consistency",
                "de-exciting", "deexciting", "File uses deexcite elsewhere"))

        # "striped" vs "stripped" (fully ionized)
        for m in re.finditer(r'\bstriped\b', txt, re.IGNORECASE):
            errs.append((sn, ln, "Spelling",
                "'striped'", "'stripped'", "Ions stripped, not striped"))

    return errs

def main():
    all_e = []
    for fp in FILES:
        if os.path.exists(fp):
            all_e.extend(scan_file(fp))
    # dedupe
    seen = set()
    uniq = []
    for e in all_e:
        k = (e[0], e[1], e[2], e[3][:35])
        if k not in seen:
            seen.add(k)
            uniq.append(e)
    uniq.sort(key=lambda x: (x[0], x[1]))
    print(f"Files: {len(FILES)}, Substantive findings: {len(uniq)}\n")
    print("| File | Line | Category | Current Text | Recommended | Rationale |")
    print("|------|------|----------|-------------|-------------|-----------|")
    for e in uniq:
        f, l, cat, curr, rec, rat = e
        es = lambda s: s.replace('|','\\|').replace('\n',' ')[:80]
        print(f"| {f} | {l} | {cat} | {es(curr)} | {es(rec)[:60]} | {es(rat)[:60]} |")

if __name__ == '__main__':
    main()
