#!/usr/bin/env python3
"""
Editorial review of comment records in 58Ca, 58Sc, 58Ti, 58V, 58Cr datasets.
Implements error classes from .github/skills/editorial-review-guidelines/SKILL.md
Check-Only. Report findings.
"""

import re
import os
import sys

# Files to scan
FILES = [
    # 58Ca
    r"d:\X\ND\ENSDF\XUNDL\A58\Ca58\old\Ca58_adopted.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Ca58\old\Ca58_1h_59sc_2pg.ens",
    # 58Sc
    r"d:\X\ND\ENSDF\XUNDL\A58\Sc58\old\Sc58_adopted.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Sc58\old\Sc58_9be_70zn_xg.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Sc58\old\Sc58_9be_238u_fg.ens",
    # 58Ti
    r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_adopted.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_beta_decay_12_ms.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_9be_61v_58tig.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_1h_58ti_58tiPg.ens",
    # 58V
    r"d:\X\ND\ENSDF\XUNDL\A58\V58\old\V58_adopted.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\V58\old\V58_beta_decay_58_ms.ens",
    # 58Cr
    r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_adopted.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_coulex.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_beta_decay_191_ms.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_9be_59mn_58crg.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_238u_64ni_xg.ens",
    r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_238u_48ca_xg_208pb_48ca_xg.ens",
]

# Only comment records: c, cL, cG, cB, cE, cN, cP, cQ and their continuations (2c, 3c, etc.)
COMMENT_PREFIX_RE = re.compile(r'^.{6}([0-9]*)c[LGBENPQ]?\s')

# Allowed element symbols for isotope detection (1-3 chars, first uppercase rest lowercase)
ELEMENT_SYMBOLS = {
    'H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar',
    'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
    'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
    'Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu',
    'Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn',
    'Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr',
    'Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og',
}

# Valid ENSDF prefix symbols - context-dependent, not errors if preceded by |
VALID_ENSDF_SYMBOLS = {'|a','|b','|g','|d','|e','|f','|h','|i','|j','|k','|l','|m','|n',
    '|p','|q','|r','|s','|t','|u','|v','|w','|x','|y','|z',
    '|C','|D','|F','|G','|H','|J','|L','|P','|Q','|R','|S','|U','|V','|W','|X','|Y',
    '|0','|1','|2','|3','|4','|5','|7','|8','|9',
    '|*','|?','|<','|>',"|'",'|+','|-','|=','|@','|^','|_','|&','|(','|)','|.','||',
    '~h','~#',
    '|m','|b','|g','|d','|q'}


def is_comment_line(line):
    """Check if line is a comment record (c, cL, cG, cB, cE, cN, cP, cQ or continuation)."""
    if len(line) < 8:
        return False
    col7 = line[6] if len(line) > 6 else ''
    col8 = line[7] if len(line) > 7 else ''
    # Col 7 = 'c' for comments; with optional continuation prefix in col 6
    # Pattern: col6 can be digit(s) or blank, col7 is 'c'
    # But we need to check: columns 1-5 NUCID, col6 continuation, col7 = 'c', col8 = type
    if col7 == 'c':
        return True
    return False


def get_comment_type(line):
    """Return comment type: cL, cG, cB, cE, cN, cP, cQ, or c (general)."""
    if len(line) < 8:
        return 'c'
    col8 = line[7] if len(line) > 7 else ' '
    comment_types = {'L': 'cL', 'G': 'cG', 'B': 'cB', 'E': 'cE', 'N': 'cN', 'P': 'cP', 'Q': 'cQ'}
    if col8 in comment_types:
        return comment_types[col8]
    # If col8 is space or continuation of comment text
    if col8 == ' ' or col8.isdigit() or col8.isalpha():
        # continuation of a c line - but we need to check col6
        col6 = line[6] if len(line) > 6 else ' '
        if col6 in '0123456789':
            # Could be continuation comment like "2cL" or "2c "
            if len(line) > 7:
                second_char = line[7]
                if second_char in comment_types:
                    return f'c{second_char}'
        return 'c'  # general c or continuation
    return 'c'


def extract_fields(line):
    """Extract meaningful text from cols 10-80 of comment line, stripping NUCID prefix."""
    if len(line) < 10:
        return ""
    return line[9:].rstrip('\n')


def find_errors_in_file(filepath):
    """Scan a single ENSDF file for comment errors."""
    errors = []
    short_name = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [(short_name, 1, "File-Read", f"Cannot read file: {e}", "", "")]
    
    for i, line in enumerate(lines):
        linenum = i + 1
        raw = line.rstrip('\n\r')
        
        if not is_comment_line(raw):
            continue
        
        ctype = get_comment_type(raw)
        text = extract_fields(raw)
        
        # --- Error Class 1: ENSDF Notation ---
        
        # 1a. Plain isotope tokens (not wrapped in {+n})
        # Scan for digit+element sequences not preceded by {+
        for m in re.finditer(r'(?<!\{\+)\b(\d{1,3})([A-Z][a-z]?)\b', text):
            num, elem = m.group(1), m.group(2)
            if elem in ELEMENT_SYMBOLS:
                # Check it's not a token followed by | (e.g., 2I|g)
                start = m.start()
                after = text[m.end():m.end()+1] if m.end() < len(text) else ''
                if after != '|':
                    context_start = max(0, start - 10)
                    context_end = min(len(text), m.end() + 10)
                    ctx = text[context_start:context_end]
                    errors.append((short_name, linenum, "Isotope-Notation",
                        f"Plain isotope token '{m.group()}' in: ...{ctx}...",
                        f"`{{{'+'}{num}}}{elem}`",
                        "Isotope tokens need {+n} wrapping"))
        
        # 1b. Unicode leakage - scan for non-ASCII
        for j, ch in enumerate(raw):
            if ord(ch) > 127:
                pos = max(0, j-20)
                ctx = raw[pos:min(len(raw), j+20)]
                errors.append((short_name, linenum, "Unicode-Leakage",
                    f"Non-ASCII char U+{ord(ch):04X} at col {j+1}: ...{ctx}...",
                    "Use ENSDF | escape sequences",
                    "Raw Unicode glyphs not allowed"))
                break  # one per line to avoid spam
        
        # 1c. Mixed symbol-text - Greek/mu symbols as raw text
        # Common patterns: gamma-ray, μm, β-delayed, ug/cm2
        mixed_patterns = [
            (r'\bgamma[- ]ray', "'gamma-ray'", "|g-ray"),
            (r'\b[μu]m\b', "μm or um", "|mm"),
            (r'\bβ[- ]', "β-", "|b-"),
            (r'\bug\b', "μg", "|mg"),
        ]
        for pat, wrong, correct in mixed_patterns:
            if re.search(pat, text, re.IGNORECASE):
                errors.append((short_name, linenum, "Symbol-Text-Mix",
                    f"Mixed symbol-text: matches '{wrong}' in: ...{text[:50]}...",
                    f"`{correct}`",
                    "Use ENSDF | escape for symbols"))
        
        # 1d. Missing {I} on uncertainties
        # Pattern: bare I\d+ near values
        for m in re.finditer(r'\bI(\d{1,3})\b', text):
            # Check not already {I...}
            pre = text[max(0, m.start()-3):m.start()]
            if '{' not in pre:
                ctx = text[max(0, m.start()-15):min(len(text), m.end()+15)]
                errors.append((short_name, linenum, "Missing-{I}",
                    f"Bare I{m.group(1)} in: ...{ctx}...",
                    f"`{{I{m.group(1)}}}`",
                    "Uncertainty needs {I} braces"))
        
        # 1e. Non-ENSDF unit spellings
        unit_patterns = [
            (r'\bcm2\b', "cm2", "cm{+2}"),
            (r'\bmg/cm2\b', "mg/cm2", "mg/cm{+2}"),
            (r'\bg/cm2\b', "g/cm2", "g/cm{+2}"),
        ]
        for pat, wrong, correct in unit_patterns:
            if re.search(pat, text):
                errors.append((short_name, linenum, "Non-ENSDF-Units",
                    f"Unit spelling '{wrong}' in: ...{text[:60]}...",
                    f"`{correct}`",
                    "Use superscript notation"))
        
        # 1f. Extra space after $ sign
        if re.search(r'\$\s', text) and '$' in text:
            # Find $ followed by space
            for m in re.finditer(r'\$ +', text):
                ctx = text[max(0, m.start()-5):min(len(text), m.end()+10)]
                errors.append((short_name, linenum, "Extra-Space-After-$",
                    f"Space after $: ...{ctx}...",
                    "Remove space after $",
                    "`$ ` should be `$`"))
        
        # 1g. Extra space after =
        if re.search(r'=\s\d', text):
            for m in re.finditer(r'=\s+(\d)', text):
                errors.append((short_name, linenum, "Extra-Space-After-=",
                    f"Space after = before number: ...{text[max(0,m.start()-5):m.end()+10]}...",
                    f"=`{m.group(1)}...",
                    "No space between = and value"))
        
        # --- Error Class 2: Grammar and Style ---
        
        # 2a. Capitalization for record-specific comments with field identifier
        # cL E$, cL J$, cL T$, cL S$, cG E$, cG RI$, cG M$, cG MR$, cB IB$, etc.
        # Should be lowercase after the field identifier, unless first token is numeral/symbol
        field_id_match = re.match(r'^(\s*)([A-Z]+)\(?\)?\$(.*)', text)
        if field_id_match:
            field = field_id_match.group(2)
            rest = field_id_match.group(3).strip()
            if rest and len(rest) > 0:
                first_char = rest[0]
                # Check if starts uppercase when it should be lowercase
                if first_char.isupper() and field in ('E','J','T','S','RI','M','MR','IB',
                    'LOGFT','EAV','QP','IP','BE2','BM2','BM2W','BR','NR','X'):
                    # Exceptions: numeral, symbol, isotope token, acronym
                    is_exception = False
                    if rest.startswith(('{', '|')):  # ENSDF symbol
                        is_exception = True
                    elif rest[0].isdigit():
                        is_exception = True
                    # Common acronyms
                    acronyms_start = ['R(anisotropy)', 'B(M2)', 'B(E2)', 'From', 'VS-IMSRG']
                    for a in acronyms_start:
                        if rest.startswith(a):
                            is_exception = True
                            break
                    if not is_exception:
                        errors.append((short_name, linenum, "Capitalization",
                            f"c... ${field}$ comment starts uppercase: '{rest[:30]}...'",
                            "Lowercase after field identifier",
                            "Record-specific comments with $field$ should be lowercase"))
        
        # 2b. NUCID case on comment lines (cols 1-5 should be uppercase)
        nucid = raw[:5]
        if nucid != nucid.upper():
            errors.append((short_name, linenum, "NUCID-Case",
                f"NUCID '{nucid}' not uppercase",
                f"'{nucid.upper()}'",
                "NUCID must be uppercase on comment lines"))
        
        # 2c. Dittography (repeated words)
        for m in re.finditer(r'\b(\w+)\s+\1\b', text, re.IGNORECASE):
            if len(m.group(1)) > 2:  # Skip short words like "a a"
                errors.append((short_name, linenum, "Dittography",
                    f"Repeated word '{m.group(1)} {m.group(1)}' in: ...{text[max(0,m.start()-10):m.end()+20]}...",
                    f"Remove duplicate '{m.group(1)}'",
                    "Duplicated word error"))
        
        # --- Error Class 3: Punctuation and Lists ---
        
        # 3. Oxford comma check for lists of 3+
        if re.search(r',\s*and\s+.*,\s*and\s+', text):
            errors.append((short_name, linenum, "Oxford-Comma",
                f"Multiple 'and' in list: ...{text[:60]}...",
                "Use Oxford comma with single 'and'",
                "Lists of 3+ need Oxford comma, only one 'and'"))
        
        # --- Error Class 4: Hyphenation ---
        
        # 4a. Always-hyphenated terms
        if re.search(r'\bhalf life\b', text, re.IGNORECASE) and not re.search(r'\bhalf-life\b', text):
            errors.append((short_name, linenum, "Hyphenation",
                "'half life' without hyphen",
                "'half-life'",
                "Always hyphenate 'half-life'"))
        
        if re.search(r'\bL transfer\b', text, re.IGNORECASE) and not re.search(r'\bL-transfer\b', text):
            errors.append((short_name, linenum, "Hyphenation",
                "'L transfer' without hyphen",
                "'L-transfer'",
                "Always hyphenate 'L-transfer'"))
        
        # --- Error Class 5: Terminology and Spelling ---
        
        # Common misspellings
        spelling_errors = {
            'deexiting': 'deexciting',
            'deexcite': 'deexcite',
            'multiporities': 'multipolarities',
            'multipority': 'multipolarity',
            'grand-daughter': 'granddaughter',
            'grand daughter': 'granddaughter',
            'ohter': 'other',
            'usign': 'using',
            'stoped': 'stopped',
            'striped': 'stripped',  # "striped" ions -> "stripped" ions
            'coeffcients': 'coefficients',
            'novelly designed': 'newly designed',
            'Van der Graaff': 'Van de Graaff',
            'Van de Graaf': 'Van de Graaff',
            'Van der Graaf': 'Van de Graaff',
            'Van de Craaff': 'Van de Graaff',
            'Cockroft-Walton': 'Cockcroft-Walton',
            'superseeds': 'supersedes',
            'superseed': 'supersede',
        }
        for wrong, correct in spelling_errors.items():
            if wrong in text.lower():
                # case-insensitive search
                if wrong.lower() in text.lower():
                    # Find actual occurrence 
                    for m in re.finditer(re.escape(wrong), text, re.IGNORECASE):
                        ctx = text[max(0, m.start()-10):min(len(text), m.end()+10)]
                        errors.append((short_name, linenum, "Spelling",
                            f"'{m.group()}' in: ...{ctx}...",
                            f"'{correct}'",
                            "Misspelling"))
        
        # --- Error Class 6: Text and Number Integrity ---
        
        # 6a. Space within number (likely a missing digit error)
        # E{-p}(lab)=54 6 -> likely 546
        for m in re.finditer(r'=\d+\s+\d', text):
            ctx = text[max(0, m.start()-10):min(len(text), m.end()+10)]
            errors.append((short_name, linenum, "Space-In-Number",
                f"Possible space within number: ...{ctx}...",
                "Verify correct digit",
                "Space within number may indicate missing digit"))
        
        # 6b. Field cross-contamination
        # Energy values in RI$ comments or RI values in E$ comments
        if '$RI$' in text and re.search(r'\d{4}\.\d', text):
            # RI comment with what looks like an energy
            # Only flag if the number is >2000 (energies typically 4 digits)
            for m in re.finditer(r'\b(1\d{3}\.\d|\d{4,}\.?\d*)', text):
                val = float(m.group())
                if 500 < val < 20000 and re.search(r'\$RI\$', text):
                    errors.append((short_name, linenum, "Field-Contamination",
                        f"Possible energy value in RI$ comment: {m.group()}",
                        "Verify value belongs in RI$",
                        "RI$ comment should contain intensity, not energy"))
        
        if '$E$' in text and re.search(r'\b\d+\.?\d*\s*%', text):
            errors.append((short_name, linenum, "Field-Contamination",
                f"Possible intensity in E$ comment: ...{text[:50]}...",
                "Verify value belongs in E$",
                "E$ comment should contain energy, not intensity"))
        
        # --- Logical Clarity (Class 7) would need more context ---
        # Flag contradictory claims
        # (would need multi-line analysis - skip for automated scan)
    
    return errors


def main():
    all_errors = []
    for filepath in FILES:
        if not os.path.exists(filepath):
            all_errors.append((os.path.basename(filepath), 0, "File-Not-Found",
                f"File does not exist: {filepath}", "", ""))
            continue
        fe = find_errors_in_file(filepath)
        all_errors.extend(fe)
    
    # Sort by file, then line number
    all_errors.sort(key=lambda x: (x[0], x[1]))
    
    # Print report
    print("=" * 120)
    print("EDITORIAL REVIEW REPORT - 58Ca, 58Sc, 58Ti, 58V, 58Cr Datasets")
    print("=" * 120)
    
    if not all_errors:
        print("\nNo issues found.")
        return
    
    # Group by file
    current_file = None
    for err in all_errors:
        fname, line, cat, curr, rec, rationale = err
        if fname != current_file:
            current_file = fname
            print(f"\n{'─' * 80}")
            print(f"  File: {fname}")
            print(f"{'─' * 80}")
        print(f"  L{line:4d} | {cat:25s} | {curr[:70]}")
    
    print(f"\n{'=' * 120}")
    print(f"Total findings: {len(all_errors)}")
    print(f"{'=' * 120}")
    
    # Print markdown table
    print("\n\n## Markdown Report Table\n")
    print("| File | Line | Category | Current Text | Recommended | Rationale |")
    print("|------|------|----------|-------------|-------------|-----------|")
    for err in all_errors:
        fname, line, cat, curr, rec, rationale = err
        # Escape pipe chars in text
        curr_esc = curr.replace('|', '\\|').replace('\n', ' ')
        rec_esc = rec.replace('|', '\\|').replace('\n', ' ')
        rat_esc = rationale.replace('|', '\\|').replace('\n', ' ')
        print(f"| {fname} | {line} | {cat} | {curr_esc[:80]} | {rec_esc[:60]} | {rat_esc[:60]} |")


if __name__ == '__main__':
    main()
