"""Editorial review: all Cl34/new/*.ens files. Scan-only, report table."""
import re, os, glob

DIR = r'A34\Cl34\new'
files = glob.glob(os.path.join(DIR, '*.ens'))

def is_comment(l):
    return len(l)>=8 and (l[6]=='c' or l[7]=='c')

def comment_text(l):
    return l[9:].strip() if len(l)>=10 else ''

def nucid(l):
    return l[:5] if len(l)>=5 else ''

results = []

for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    for i, l in enumerate(lines):
        if not is_comment(l): continue
        t = comment_text(l)
        if not t: continue
        ln = i+1
        
        # --- 1. Unicode leakage ---
        for j, c in enumerate(l):
            if ord(c) > 127 and c not in '\r\n':
                ctx = l[max(0,j-5):j+5].strip()
                results.append((fname, ln, 'Unicode', repr(c), ctx, ''))
        
        # --- 2. Plain isotope tokens (no {+}) --- 
        for m in re.finditer(r'(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b', t):
            token = m.group()
            if re.match(r'\d{4}[A-Z][a-z]\d{2}', token): continue
            if '|' in l[m.end()-1:m.end()+5]: continue
            if token in ['34CL','34Ar','34Ar'] and nucid(l) in [' 34CL',' 34Ar']: continue
            # Skip numbers like 3He if it's part of file content
            ctx = t[max(0,m.start()-10):m.end()+10]
            results.append((fname, ln, f'IsotopeToken', token, ctx, 'wrap in {+}'))
        
        # --- 3. Extra space after $ ---
        for m in re.finditer(r'\$\s', t):
            # Skip header records (H record)
            if l[7] == 'H': continue
            ctx = t[max(0,m.start()-5):m.end()+5]
            results.append((fname, ln, 'dollar+space', '$ ', ctx, 'remove space'))
        
        # --- 4. Extra space after = number ---
        for m in re.finditer(r'=\s[0-9]', t):
            # Skip data-record-like continuation records (S GI, S E, etc.)
            if l[6] in ('S','B','2','3','4'): continue
            ctx = t[max(0,m.start()-10):m.end()+10]
            results.append((fname, ln, '=+space+num', m.group(), ctx, 'remove space'))
        
        # --- 5. Dittography ---
        for m in re.finditer(r'\b(\w+)\s+\1\b', t):
            # Skip number patterns like "0 0", "4 4" from data records
            if m.group(1).isdigit(): continue
            results.append((fname, ln, 'Dittography', m.group(), t[:60], ''))
        
        # --- 6. Greek-text leakage ---
        for greek_word in ['gamma','beta','alpha','mu ']:
            if greek_word in t.lower() and not t.lower().startswith(greek_word):
                # Skip proper names like "Gammas" (dataset)
                if greek_word == 'gamma' and 'Gammas' in t: continue
                ctx = t[:50]
                results.append((fname, ln, 'Greek-text', greek_word, ctx, 'use |g, |b, |a, |m'))
        
        # --- 7. Missing {I} on bare uncertainties in comments ---
        # Pattern: value + space + unit + space + digit(s) where digits are uncertainty
        if 'cL' in l[6:9] or 'cG' in l[6:9] or 'cB' in l[6:9] or 'cE' in l[6:9]:
            for m in re.finditer(r'([\d.]+)\s+(EV|KEV|MEV)\s+(\d+)', t):
                val, unit, unc = m.group(1), m.group(2), m.group(3)
                results.append((fname, ln, 'BareUnc', f'{val} {unit} {unc}', t[:50], f'use {{I{unc}}}'))
        
        # --- 8. Spelling ---
        spell_checks = {
            'deexiting': 'deexciting',
            'multiporities': 'multipolarities',
            'grand-daughter': 'granddaughter',
            'ohter': 'other', 'usign': 'using',
            'stoped': 'stopped', 'striped': 'stripped',
            'coeffcient': 'coefficient',
        }
        for wrong, correct in spell_checks.items():
            if wrong in t.lower():
                results.append((fname, ln, 'Spelling', wrong, t[:50], correct))
        
        # --- 9. Chemical formulas ---
        # Check CD{-2} vs Cd{-2}
        for m in re.finditer(r'\bC[Dd]\{-\d+\}', t):
            results.append((fname, ln, 'ChemFormula', m.group(), t[:50], 'verify CD vs Cd'))
        
        # --- 10. Subject-verb: NSR key + verb ---
        for m in re.finditer(r'(\d{4}[A-Z][a-z]\d{2})\s+(\w+)\b', t):
            key, verb = m.group(1), m.group(2)
            if verb.endswith('s') and not verb.endswith('es') and not verb.endswith('ss'):
                results.append((fname, ln, 'VerbAgr', f'{key} {verb}', t[:50], f'Singular verb needed'))

# Print report
print(f'# Editorial Review Report: Cl34 datasets')
print(f'\nChecked {len(files)} files, {len(results)} issues found.\n')

categories = {}
for fname, ln, cat, val, ctx, rcm in results:
    if cat not in categories: categories[cat] = []
    categories[cat].append((fname, ln, val, ctx, rcm))

for cat in sorted(categories.keys()):
    items = categories[cat]
    print(f'\n## {cat} ({len(items)} issues)')
    print('| File | Line | Current | Context | Recommended |')
    print('|------|------|---------|---------|-------------|')
    for fname, ln, val, ctx, rcm in items:
        print(f'| {fname} | {ln} | `{val}` | {ctx[:50]} | {rcm} |')
