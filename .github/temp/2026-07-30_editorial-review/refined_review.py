#!/usr/bin/env python3
"""
Refined editorial review of comment records in 58Ca/58Sc/58Ti/58V/58Cr datasets.
Manual verification pass against raw file content. Produces final report table.
"""

import re
import os

FILES = {
    "Ca58_adopted.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Ca58\old\Ca58_adopted.ens",
    "Ca58_1h_59sc_2pg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Ca58\old\Ca58_1h_59sc_2pg.ens",
    "Sc58_adopted.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Sc58\old\Sc58_adopted.ens",
    "Sc58_9be_70zn_xg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Sc58\old\Sc58_9be_70zn_xg.ens",
    "Sc58_9be_238u_fg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Sc58\old\Sc58_9be_238u_fg.ens",
    "Ti58_adopted.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_adopted.ens",
    "Ti58_beta_decay_12_ms.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_beta_decay_12_ms.ens",
    "Ti58_9be_61v_58tig.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_9be_61v_58tig.ens",
    "Ti58_1h_58ti_58tiPg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Ti58\old\Ti58_1h_58ti_58tiPg.ens",
    "V58_adopted.ens": r"d:\X\ND\ENSDF\XUNDL\A58\V58\old\V58_adopted.ens",
    "V58_beta_decay_58_ms.ens": r"d:\X\ND\ENSDF\XUNDL\A58\V58\old\V58_beta_decay_58_ms.ens",
    "Cr58_adopted.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_adopted.ens",
    "Cr58_coulex.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_coulex.ens",
    "Cr58_beta_decay_191_ms.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_beta_decay_191_ms.ens",
    "Cr58_9be_59mn_58crg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_9be_59mn_58crg.ens",
    "Cr58_238u_64ni_xg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_238u_64ni_xg.ens",
    "Cr58_238u_48ca_xg_208pb_48ca_xg.ens": r"d:\X\ND\ENSDF\XUNDL\A58\Cr58\old\Cr58_238u_48ca_xg_208pb_48ca_xg.ens",
}

# Known acronyms/abbreviations allowed as uppercase
ACRONYMS = {'E1','E2','E3','E4','E5','E6','M1','M2','M3','M4','M5','M6',
            'E0','M0','D','Q','O','B(E2)','B(M2)','R(anisotropy)','RUL',
            'VS-IMSRG','CC','RDDS','B(E2)|^','BM2','BE2W','BE2','BM2W',
            'NSR','ECIS97','LNPS','GXPFIA','GXPF1B','A3DA'}

def get_first_data_record_line(lines):
    """Find line number (0-based) of first L/G/E/B/DP/PN record."""
    for i, line in enumerate(lines):
        if len(line) < 9:
            continue
        col8 = line[7] if len(line) > 7 else ' '
        if col8 in ('L', 'G', 'E', 'B', 'D', 'P', 'N'):
            # Check it's a data record (col7 space, col8 record type)
            col7 = line[6] if len(line) > 6 else ' '
            if col7 == ' ':
                # But skip header H records and XREF records
                col9 = line[8] if len(line) > 8 else ' '
                # PN is a data record (parent normalization)
                if col8 == 'P' and col9 == 'N':
                    return i
                if col8 in ('L', 'G', 'E', 'B'):
                    return i
                if col8 == 'D' and col9 == 'P':
                    return i
                if col8 == 'N':
                    return i
    return len(lines)

def is_comment_line(line):
    if len(line) < 8:
        return False
    return line[6] == 'c' if len(line) > 6 else False

def get_comment_field(line):
    """Extract field identifier like E$, J$, T$, RI$, M$, etc. from comment."""
    # Pattern: text after col 9, look for $something$
    text = line[9:] if len(line) > 9 else ''
    m = re.match(r'^\s*\$?([A-Za-z0-9_(),]+)\$(.*)', text)
    if m:
        return m.group(1), m.group(2)
    # No field identifier - general comment
    return None, text

def extract_context(text, pos, width=30):
    start = max(0, pos - width)
    end = min(len(text), pos + width)
    ctx = text[start:end]
    if start > 0:
        ctx = '...' + ctx
    if end < len(text):
        ctx = ctx + '...'
    return ctx

def scan_file(filepath, short_name):
    """Scan a single file for comment errors."""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    first_data_line = get_first_data_record_line(lines)
    
    for i, line in enumerate(lines):
        linenum = i + 1
        raw = line.rstrip('\n\r')
        
        if not is_comment_line(raw):
            continue
        
        is_top_block = i < first_data_line
        text = raw[9:] if len(raw) > 9 else ''
        col8 = raw[7] if len(raw) > 7 else ' '
        col6 = raw[6] if len(raw) > 6 else ' '
        comment_type = f"c{col8}" if col8 != ' ' else 'c'
        
        # ===== 1. ENSDF Notation =====
        
        # 1a. Plain isotope tokens not wrapped in {+n}
        for m in re.finditer(r'(?<!\{\+)\b(\d{1,3})([A-Z][a-z]?)\b', text):
            num, elem = m.group(1), m.group(2)
            # Valid element symbols
            valid_elements = {
                'H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P',
                'S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu',
                'Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc',
                'Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La',
                'Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu',
                'Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At',
                'Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es',
                'Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh',
                'Fl','Mc','Lv','Ts','Og','Be'}
            if elem in valid_elements:
                after = text[m.end():m.end()+1] if m.end() < len(text) else ''
                if after != '|' and after != ',':
                    ctx = extract_context(text, m.start(), 25)
                    if f'{{{char}+{num}}}{elem}' not in text[max(0,m.start()-5):m.end()+5]:
                        errors.append((short_name, linenum, "Isotope-Notation",
                            f"Plain isotope '{num}{elem}' in: {ctx}",
                            f"{{+{num}}}{elem}",
                            "Isotope tokens need {+n} wrapping"))
        
        # 1b. Unicode leakage
        for j, ch in enumerate(raw):
            if ord(ch) > 127:
                ctx = extract_context(raw, j, 20)
                errors.append((short_name, linenum, "Unicode-Leakage",
                    f"Non-ASCII U+{ord(ch):04X}: {ctx}",
                    "Use ENSDF | escape",
                    "Raw Unicode glyphs not allowed"))
                break
        
        # 1c. Non-ENSDF unit spellings (with superscript exponents)
        unit_checks = [
            (r'(?<!\|)\bcm2\b(?!\})', 'cm2', 'cm{+2}'),
            (r'(?<!\|)\bmg/cm2\b(?!\})', 'mg/cm2', 'mg/cm{+2}'),
            (r'(?<!\|)\bg/cm2\b(?!\})', 'g/cm2', 'g/cm{+2}'),
        ]
        for pat, wrong, correct in unit_checks:
            for m in re.finditer(pat, text):
                ctx = extract_context(text, m.start(), 20)
                errors.append((short_name, linenum, "Non-ENSDF-Units",
                    f"'{wrong}' in: {ctx}",
                    f"{correct}",
                    "Use superscript notation for units"))
        
        # 1d. Missing {I} on uncertainty (bare I\d+ not in braces)
        # Only flag bare I\d+ that appear to be uncertainties near values
        for m in re.finditer(r'(?<![{=])I(\d{1,3})\b', text):
            pre = text[max(0, m.start()-5):m.start()]
            if re.search(r'[=±\s]', pre) and '{' not in pre:
                ctx = extract_context(text, m.start(), 20)
                errors.append((short_name, linenum, "Missing-{I}",
                    f"Bare I{m.group(1)} in: {ctx}",
                    f"{{I{m.group(1)}}}",
                    "Uncertainty needs {I} braces"))
        
        # 1e. Mixed symbol-text (only actual Greek letters, not spelled-out)
        # Check for raw Greek letters or mu symbol in text
        greek_patterns = [
            (r'(?<!\|)[γμ](?![+\-}\d])', 'γ or μ character', '|g or |m'),
        ]
        for pat, wrong, correct in greek_patterns:
            if re.search(pat, text):
                ctx = extract_context(text, re.search(pat, text).start(), 15)
                errors.append((short_name, linenum, "Symbol-Text-Mix",
                    f"Raw '{wrong}' in: {ctx}",
                    f"Use '{correct}'",
                    "Use ENSDF | escape for symbols"))
        
        # 1f. Inconsistent subscripts (A6= pattern without {-6})
        for m in re.finditer(r'\b([A-Z])(\d+)=', text):
            letter, digits = m.group(1), m.group(2)
            if len(digits) > 0 and letter.isupper():
                # Check if this letter-digit pattern has proper subscript
                pre = text[max(0, m.start()-15):m.start()]
                if f'{{-{digits}}}' not in pre and f'{{+{digits}}}' not in pre:
                    ctx = extract_context(text, m.start(), 20)
                    if not text[m.start()-2:m.start()] in ('{', '}'):
                        errors.append((short_name, linenum, "Subscript-Notation",
                            f"'{letter}{digits}=' without subscript in: {ctx}",
                            f"({letter}{{-{digits}}}=?) or verify",
                            "Subscript notation needed for indexed variables"))
        
        # ===== 2. Grammar and Style =====
        
        # 2a. Capitalization
        field_id, field_text = get_comment_field(raw)
        if field_id and field_text:
            stripped = field_text.strip()
            if stripped and stripped[0].isupper() and not is_top_block:
                # Check exceptions
                first_word = stripped.split()[0] if stripped.split() else ''
                is_exception = False
                # Numeral start
                if first_word[0].isdigit():
                    is_exception = True
                # Symbol/ENSDF start
                elif first_word.startswith(('{', '|')):
                    is_exception = True
                # Acronym check
                for acr in ACRONYMS:
                    if first_word.startswith(acr) or first_word == acr:
                        is_exception = True
                        break
                # Check if it's a cN or cP comment (always uppercase)
                if comment_type in ('cN', 'cP'):
                    is_exception = True
                
                if not is_exception:
                    ctx = stripped[:50]
                    errors.append((short_name, linenum, "Capitalization",
                        f"c{col8} {field_id}$ starts uppercase: '{ctx}'",
                        f"Lowercase first word after {field_id}$",
                        "Record-specific comments with $field$ lowercase"))
        
        # 2b. NUCID case
        nucid = raw[:5]
        if nucid != nucid.upper() and re.search(r'[a-z]', nucid):
            errors.append((short_name, linenum, "NUCID-Case",
                f"NUCID '{nucid}' not uppercase",
                f"'{nucid.upper()}'",
                "NUCID must be uppercase on comment lines"))
        
        # 2c. Dittography
        for m in re.finditer(r'\b(\w+)\s+\1\b', text, re.IGNORECASE):
            if len(m.group(1)) > 2:
                ctx = extract_context(text, m.start(), 20)
                errors.append((short_name, linenum, "Dittography",
                    f"Repeated '{m.group(1)}' in: {ctx}",
                    f"Remove duplicate '{m.group(1)}'",
                    "Duplicated word error"))
        
        # 2d. Extra space after $
        # Only flag $<space> where $ is a field delimiter followed by content
        for m in re.finditer(r'\$\s+(.)', text):
            char_after = m.group(1)
            # Skip if this is in a general comment ($ text) where space is fine
            # Check if $ is a field identifier end (e.g., J$ text)
            pre = text[max(0, m.start()-5):m.start()]
            if re.search(r'[A-Z][a-z]?\$$', pre) or re.search(r'[A-Z]+\([^)]*\)\$$', pre):
                ctx = extract_context(text, m.start(), 20)
                errors.append((short_name, linenum, "Extra-Space-After-$",
                    f"Space after $ in: {ctx}",
                    "Remove space after $",
                    "`$ ` should be `$`"))
        
        # ===== 3. Punctuation =====
        
        # 3a. Multiple 'and' in list (Oxford comma issue)
        and_count = len(re.findall(r'\band\b', text))
        comma_count = len(re.findall(r',', text))
        if and_count > 1 and comma_count >= and_count:
            errors.append((short_name, linenum, "Oxford-Comma",
                f"Multiple 'and' with commas in: {text[:60]}",
                "Use Oxford comma with single 'and'",
                "Lists of 3+ need one 'and'"))
        
        # ===== 4. Hyphenation =====
        
        # 4a. half-life
        if re.search(r'\bhalf life\b', text, re.IGNORECASE):
            errors.append((short_name, linenum, "Hyphenation",
                "'half life' without hyphen",
                "'half-life'",
                "Always hyphenate 'half-life'"))
        
        # 4b. L-transfer
        if re.search(r'\bL transfer\b', text, re.IGNORECASE):
            errors.append((short_name, linenum, "Hyphenation",
                "'L transfer' without hyphen",
                "'L-transfer'",
                "Always hyphenate 'L-transfer'"))
        
        # 4c. gamma rays as noun (should not be hyphenated)
        for m in re.finditer(r'\b(Gamma|gamma)[-\s]rays?\b', text):
            ctx = extract_context(text, m.start(), 15)
            hyphen = '-' in m.group()
            if hyphen:
                errors.append((short_name, linenum, "Hyphenation",
                    f"'{m.group()}' in: {ctx}",
                    f"{m.group(1)} rays'",
                    "Noun 'gamma rays' no hyphen"))
        
        # ===== 5. Terminology and Spelling =====
        
        spelling_errors = {
            'deexiting': 'deexciting',
            'deexite': 'deexcite',
            'deexcitation': 'deexcitation',  # already correct
            'multiporities': 'multipolarities',
            'multipority': 'multipolarity',
            'grand-daughter': 'granddaughter',
            'grand daughter': 'granddaughter',
            'ohter': 'other',
            'usign': 'using',
            'stoped': 'stopped',
            'coeffcients': 'coefficients',
            'novelly designed': 'newly designed',
            'superseeds': 'supersedes',
            'superseed': 'supersede',
            'evaluatord': 'evaluators',
            'neutrom': 'neutron',
        }
        for wrong, correct in spelling_errors.items():
            if wrong in text.lower():
                for m in re.finditer(re.escape(wrong), text, re.IGNORECASE):
                    ctx = extract_context(text, m.start(), 15)
                    errors.append((short_name, linenum, "Spelling",
                        f"'{m.group()}' in: {ctx}",
                        f"'{correct}'",
                        "Misspelling"))
        
        # ===== 6. Text and Number Integrity =====
        
        # 6a. Extra space after =
        for m in re.finditer(r'=\s+(\d)', text):
            ctx = extract_context(text, m.start(), 15)
            errors.append((short_name, linenum, "Extra-Space-After-=",
                f"Space after = before digit: {ctx}",
                f"=value (no space)",
                "No space between = and value"))
        
        # 6b. Missing space after {I...} before next word
        for m in re.finditer(r'\{I[^}]+\}([a-zA-Z])', text):
            ctx = extract_context(text, m.start(), 20)
            errors.append((short_name, linenum, "Missing-Space",
                f"No space after {m.group()}: {ctx}",
                f"{m.group()} {m.group(1)}",
                "Space needed after uncertainty notation"))
        
        # 6c. Space within number (likely error)
        for m in re.finditer(r'=\d{2,3}\s+\d{2,3}\b', text):
            ctx = extract_context(text, m.start(), 15)
            errors.append((short_name, linenum, "Space-In-Number",
                f"Possible number split: {ctx}",
                "Verify correct digit",
                "Space within number may indicate missing digit"))
    
    return errors


def main():
    all_errors = []
    
    for short_name, filepath in sorted(FILES.items()):
        if not os.path.exists(filepath):
            print(f"WARNING: {filepath} not found!")
            continue
        fe = scan_file(filepath, short_name)
        all_errors.extend(fe)
    
    # Sort
    all_errors.sort(key=lambda x: (x[0], x[1]))
    
    # Deduplicate
    seen = set()
    unique_errors = []
    for err in all_errors:
        key = (err[0], err[1], err[2], err[3][:40])
        if key not in seen:
            seen.add(key)
            unique_errors.append(err)
    
    # Print markdown table
    print("# Editorial Review Report: 58Ca, 58Sc, 58Ti, 58V, 58Cr\n")
    print("*Check-only. No edits applied.*\n")
    print(f"Total findings: {len(unique_errors)}\n")
    print("| File | Line | Category | Current Text | Recommended | Rationale |")
    print("|------|------|----------|-------------|-------------|-----------|")
    for err in unique_errors:
        fname, line, cat, curr, rec, rationale = err
        curr_esc = curr.replace('|', '\\|').replace('\n', ' ')[:90]
        rec_esc = rec.replace('|', '\\|').replace('\n', ' ')[:70]
        rat_esc = rationale.replace('|', '\\|').replace('\n', ' ')[:60]
        print(f"| {fname} | {line} | {cat} | {curr_esc} | {rec_esc} | {rat_esc} |")

if __name__ == '__main__':
    main()
