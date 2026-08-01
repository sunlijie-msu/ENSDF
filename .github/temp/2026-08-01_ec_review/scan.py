"""Editorial review regex sweeps for S34_34cl_ec_decay_1.5266_s.ens."""
import re

with open(r'A34\S34\new\S34_34cl_ec_decay_1.5266_s.ens', 'r') as f:
    lines = f.readlines()

comment_prefixes = ['c', '2c', '3c', '4c', '5c', '6c', '7c', 'd', '2d', 'cL', 'cG', 'cB', 'cE', 'cN', 'cP', 'cQ']

def is_comment(line):
    if len(line) < 9:
        return False
    # Check cols 6-8 for comment identifiers
    tag = line[5:8].strip()
    # c at col 7, or 2c/3c/... at cols 6-7, or d at col 6
    if line[6] in 'cd' and line[6:8].strip() in ['c', 'd']:
        return True
    if line[5:7] in ['2c', '3c', '4c', '5c', '6c', '7c']:
        return True
    if line[5:7] == '2d':
        return True
    return False

print('=== Isotope tokens (plain) ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    # Find plain isotope tokens: 1-3 digits + element symbol
    matches = re.findall(r'(?<!\{)\b(\d{1,3})([A-Z][a-z]?)\b(?![\}|a-z])', text)
    for num, elem in matches:
        # Skip units
        if elem in ['MeV', 'keV', 'eV', 'PS', 'FS', 'NS', 'MS', 'S', 'H', 'D', 'M', 'Y', 'GT', 'LT', 'GE', 'LE']:
            continue
        # Skip if preceded by {+
        idx = text.find(num + elem)
        if idx >= 3 and text[idx-3:idx] == '{+ ':
            continue
        if idx >= 2 and text[idx-2:idx] == '{-':
            continue
        ctx_start = max(0, idx - 20)
        ctx_end = min(len(text), idx + len(num+elem) + 20)
        print(f'  Line {i+1}: [{num}{elem}] in: ...{text[ctx_start:ctx_end]}...')

print()
print('=== cm2 / unit issues ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    if 'cm2' in text and 'cm{+2}' not in text:
        idx = text.find('cm2')
        print(f'  Line {i+1}: cm2 at pos {idx}: ...{text[max(0,idx-20):idx+25]}...')

print()
print('=== Dittography ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    matches = re.findall(r'\b(\w+)\s+\1\b', text, re.IGNORECASE)
    for m in matches:
        print(f'  Line {i+1}: [{m} {m}]')

print()
print('=== Extra space after $ ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    for m in re.finditer(r'\$\s', text):
        idx = m.start()
        print(f'  Line {i+1}: extra space after $: ...{text[max(0,idx-10):idx+15]}...')

print()
print('=== Unicode / non-ASCII ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    for j, ch in enumerate(text):
        if ord(ch) > 127:
            print(f'  Line {i+1}: non-ASCII [{ch}] U+{ord(ch):04X} at col {j+10}')

print()
print('=== Subject-verb agreement (NSR keys) ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    # NSR key followed by verb - should be singular
    matches = re.findall(r'(\d{4}[A-Z][a-z][A-Z]{2})\s+(report|assign|suggest|indicate|give|measure|observe|deduce|find|state|note|determine|conclude)\b', text)
    for nsr, verb in matches:
        print(f'  Line {i+1}: [{nsr} {verb}] - NSR+plural verb')

print()
print('=== Missing {I} uncertainty ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    # Bare I pattern
    matches = re.findall(r'\bI\d{1,3}\b', text)
    for m in matches:
        idx = text.find(m)
        # Check if already in braces
        if idx > 0 and text[idx-1] == '{':
            continue
        print(f'  Line {i+1}: bare I: [{m}] in: ...{text[max(0,idx-15):idx+len(m)+15]}...')

print()
print('=== Leaked record tags ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    matches = re.findall(r'\s(cL|cG|\bL\b|\bG\b)\s', text)
    for m in matches:
        print(f'  Line {i+1}: leaked tag [{m.strip()}]')

print()
print('=== Capitalization check (record-specific cL/cG/cE with field ID) ===')
for i, line in enumerate(lines):
    if not is_comment(line):
        continue
    text = line[9:].rstrip()
    # Check if this comment has a field identifier like E$, J$, T$, RI$, M$, MR$, TI$, etc.
    m = re.match(r'[A-Z]+[,\$]+[A-Z]*\$', text)
    if m:
        # Get text after the identifier
        rest = text[m.end():].strip()
        if rest:
            first_char = rest[0]
            # Check if first token is lowercase when it should be lowercase
            # Record-specific comments with field ID should be lowercase (unless numeral/symbol/acronym)
            print(f'  Line {i+1}: field-ID comment: [{text[:40]}...] first token after $: [{rest[:20]}]')
