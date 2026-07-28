"""Systematic editorial review sweeps for ENSDF file."""
import re

with open(r'A34\Cl34\new\Cl34_34ar_ec_decay_0.84646_s.ens','r',encoding='utf-8') as f:
    lines = f.readlines()

issues = []

# 1. Non-ASCII characters
for i,l in enumerate(lines):
    for j,c in enumerate(l):
        if ord(c) > 127 and c not in '\r\n':
            issues.append(('Unicode',i+1,repr(c),'pos '+str(j)))

# 2. Plain isotope tokens (no {+} braces)
for i,l in enumerate(lines):
    for m in re.finditer(r'(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b', l):
        token = m.group()
        next_chars = l[m.end():m.end()+5]
        if '|' in next_chars: continue
        if token in ['34CL','34AR','34Si','34S']: continue
        # Skip if it's an NSR key
        if re.match(r'\d{4}[A-Z][a-z]\d{2}', token): continue
        ctx = l[max(0,m.start()-15):m.end()+15].strip()
        issues.append(('IsotopeToken',i+1,token,ctx))

# 3. Extra space after $
for i,l in enumerate(lines):
    for m in re.finditer(r'\$\s', l):
        ctx = l[max(0,m.start()-10):m.end()+10].strip()
        issues.append(('dollar+space',i+1,'$ ',ctx))

# 4. Extra space after = plus number
for i,l in enumerate(lines):
    for m in re.finditer(r'=\s[0-9]', l):
        # Skip S-field records (L record S=)
        if i>0 and lines[i-1].strip().startswith('34CL') and 'L ' in l[7:9]:
            continue
        ctx = l[max(0,m.start()-10):m.end()+10].strip()
        issues.append(('=+space+number',i+1,m.group(),ctx))

# 5. Dittography
for i,l in enumerate(lines):
    for m in re.finditer(r'\b(\w+)\s+\1\b', l):
        ctx = l[max(0,m.start()-10):m.end()+10].strip()
        issues.append(('Dittography',i+1,m.group(),ctx))

# 6. Missing {I} on uncertainties in comment lines
for i,l in enumerate(lines):
    if len(l)<8: continue
    is_cL = (l[6]=='c' or l[7]=='c') and 'c' in l[6:8]
    if not is_cL: continue
    # Check for bare unc numbers after value+unit  
    for m in re.finditer(r'([\d.]+)\s+(EV|KEV|MEV)\s+(\d+)', l):
        issues.append(('BareUnc',i+1,m.group(3),m.group(1)+' '+m.group(2)+' '+m.group(3)))

# 7. Check for 'I' prefix without braces
for i,l in enumerate(lines):
    if len(l)<8: continue
    is_cL = (l[6]=='c' or l[7]=='c') and 'c' in l[6:8]
    if not is_cL: continue
    for m in re.finditer(r'\bI(\d{1,3})\b', l):
        issues.append(('BareIprefix',i+1,'I'+m.group(1),l[9:].strip()[:60]))

# 8. Check cL/cG/cB capitalization
first_data_idx = None
for i,l in enumerate(lines):
    if len(l)>=10 and l[7] in ('L','G','E','B','P','N') and l[8]==' ':
        first_data_idx = i
        break

for i,l in enumerate(lines):
    if len(l)<8: continue
    is_comment = (l[6]=='c' or l[7]=='c')
    if not is_comment: continue
    if first_data_idx is not None and i > first_data_idx:
        # Record-specific cL: extract text after prefix
        t = l[9:].strip() if len(l)>9 else ''
        if '$' in t:
            # Has identifier: cL J$text  or cG RI$text
            dollar_pos = t.index('$')
            after_id = t[dollar_pos+1:].strip()
            if after_id and after_id[0].isupper() and not after_id[0].isdigit():
                # Check first word is not a numeral or symbol
                issues.append(('Capitalization-rec',i+1,after_id[:20],t[:50]))

# 9. Hyphenation check
for i,l in enumerate(lines):
    # Check for gamma-ray (should be |g-ray)
    for m in re.finditer(r'\bgamma', l, re.IGNORECASE):
        ctx = l[max(0,m.start()-5):m.end()+5].strip()
        issues.append(('Greek-text',i+1,m.group(),ctx))

# Print report
print('=== EDITORIAL REVIEW REPORT ===')
print(f'File: Cl34_34ar_ec_decay_0.84646_s.ens\n')

cats = sorted(set(x[0] for x in issues))
for cat in cats:
    ci = [x for x in issues if x[0]==cat]
    print(f'--- {cat} ({len(ci)}) ---')
    for item in ci:
        print(f"  L{item[1]}: {item[2]}  | {item[3]}")
    print()
