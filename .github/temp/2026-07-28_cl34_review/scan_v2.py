"""Scan Cl34/*.ens for real editorial issues only."""
import re, os, glob

DIR = r'A34\Cl34\new'
files = sorted(glob.glob(os.path.join(DIR, '*.ens')))

def ct(l):
    return l[9:].strip() if len(l)>=10 else '' if len(l)>=8 and (l[6]=='c' or l[7]=='c') else None

issues = []

for fp in files:
    fn = os.path.basename(fp)
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        ls = f.readlines()
    for i,l in enumerate(ls):
        if not (len(l)>=8 and (l[6]=='c' or l[7]=='c')): continue
        t = ct(l)
        if t is None: continue
        ln = i+1
        
        # 1. Dittography (the the, of of, a a)
        for m in re.finditer(r'\b(\w+)\s+\1\b', t):
            if not m.group(1).isdigit():
                issues.append((fn,ln,'Dittography',m.group(),t[:50],''))
        
        # 2. Raw Greek letters
        if 'gamma' in t.lower() and 'Gammas' not in t:
            issues.append((fn,ln,'Greek-text','gamma',t[:50],'use |g'))
        if 'beta' in t.lower() and 'betatron' not in t.lower() and 'BetaShape' not in t:
            issues.append((fn,ln,'Greek-text','beta',t[:50],'use |b'))
        
        # 3. cm2, mg/cm2, ug/cm2 without superscript
        for m in re.finditer(r'\b(cm2|mg/cm2|ug/cm2)\b', t):
            issues.append((fn,ln,'UnitExp',m.group(),t[:50],'use cm{+2} etc'))
        
        # 4. Extra space after = before number (in comments only)
        for m in re.finditer(r'=\s[0-9]', t):
            # Skip if this looks like a data record (S, 2, B continuation)
            if l[6] in ('S','B','2','3','4'): continue
            # Skip if it's part of a weight/range expression
            if '=' in t[:20]: pass  # allow if it's after a property=
            issues.append((fn,ln,'=+space+num',m.group(),t[:50],'remove space'))
        
        # 5. Extra space after $
        for m in re.finditer(r'\$\s', t):
            if l[7] == 'H': continue  # skip header
            # Don't flag if it's end of text
            issues.append((fn,ln,'dollar+space','$ ',t[:40],'remove space'))
        
        # 6. Spelling
        for w,c in [('deexiting','deexciting'),('ohter','other'),('usign','using'),
                     ('stoped','stopped'),('multiporities','multipolarities')]:
            if w in t.lower():
                issues.append((fn,ln,'Spelling',w,t[:50],c))
        
        # 7. Non-ASCII
        for j,c in enumerate(l):
            if ord(c) > 127 and c not in '\r\n':
                issues.append((fn,ln,'Unicode',repr(c),'','use ENSDF symbol'))

print(f'= Cl34 Editorial Review Report =')
print(f'{len(files)} files, {len(issues)} real issues\n')
cats = {}
for fn,ln,cat,val,ctx,rcm in issues:
    cat_key = cat
    if cat_key not in cats: cats[cat_key] = []
    cats[cat_key].append((fn,ln,val,ctx,rcm))

for cat in sorted(cats.keys()):
    items = cats[cat]
    print(f'\n## {cat} ({len(items)})')
    print('| File | Line | Current | Context | Fix |')
    print('|------|------|---------|---------|-----|')
    for fn,ln,val,ctx,rcm in items:
        print(f'| {fn} | {ln} | `{val}` | {ctx[:50]} | {rcm} |')
