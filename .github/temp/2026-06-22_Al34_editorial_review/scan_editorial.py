"""Scan all Al34 .ens files for editorial review issues."""
import os, re, sys

AL34_DIR = r"d:\X\ND\ENSDF\A34\Al34\new"
files = sorted([f for f in os.listdir(AL34_DIR) if f.endswith('.ens')])

print("=== SCANNING ALL Al34 FILES FOR EDITORIAL ISSUES ===\n")

for fname in files:
    fpath = os.path.join(AL34_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    
    for i, line in enumerate(lines):
        ln = i + 1
        stripped = line.rstrip('\n')
        
        # Only check comment lines: col 7 (index 6) should contain 'c'
        if len(stripped) >= 7 and stripped[6] == 'c':
            comment_part = stripped[7:] if len(stripped) > 7 else ''
            
            # Determine record type (L, G, B, E, N, P, Q, or blank)
            rec_type = stripped[7] if len(stripped) > 7 else ''
            
            # --- Check for field identifier pattern (e.g., E$, J$, T$, E,RI$) ---
            # Pattern: optional record type letter, optional spaces, field ID(s), $
            field_match = re.match(r'[LGBENPQ]?\s*([A-Z][A-Z,]*)\$(.+)', comment_part)
            
            if field_match:
                field_id = field_match.group(1)
                text_after_dollar = field_match.group(2)
                
                # cP and cN always uppercase - skip
                if rec_type in ('P', 'N'):
                    continue
                
                # Record-specific comments with field identifier => lowercase
                # Exception: first token is numeral, symbol, isotope token, or acronym
                first_word = text_after_dollar.lstrip()
                if first_word and first_word[0].isupper():
                    # Check exceptions
                    is_exception = (
                        first_word[0].isdigit() or
                        first_word.startswith('{') or
                        first_word.startswith('|') or
                        first_word.startswith('(') or
                        first_word.startswith('[') or
                        first_word == 'I' or
                        first_word == 'II'  # Roman numerals
                    )
                    if not is_exception:
                        issues.append(
                            "Capitalization: %s%s$%s starts uppercase '%s'" % (
                                rec_type, field_id, text_after_dollar[:10],
                                first_word.split()[0] if first_word.split() else ''
                            )
                        )
            
            # --- Check for standalone $ (no field identifier) ---
            dollar_no_field = re.match(r'[LGBENPQ]?\s*\$(.+)', comment_part)
            if dollar_no_field:
                text_after = dollar_no_field.group(1)
                first_char = text_after.lstrip()[:1] if text_after.lstrip() else ''
                if first_char and first_char.islower():
                    issues.append(
                        "Standalone comment starts lowercase: '%s'" % text_after.strip()[:50]
                    )
            
            # --- Check for extra space after $ ---
            if re.search(r'\$\s', stripped):
                issues.append("Extra space after $")
            
            # --- Check for bare {I} notation ---
            # Look for I\d+ not in braces
            for m in re.finditer(r'(?<!\{)I(\d{1,3})(?!\})', stripped[7:]):
                val = m.group(1)
                pos = stripped[7:].find('I' + val) + 7
                context_before = stripped[max(0,pos-8):pos]
                # Filter: skip if part of |I (like I|g, I|b) or if it's clearly a word
                if '|' in context_before[-2:]:
                    continue
                if re.match(r'[A-Za-z]', stripped[pos-1:pos]):
                    continue
                issues.append("Bare I (missing braces): '...%s...'" % stripped[max(0,pos-5):pos+5].strip())
    
    # --- Check for dittography ---
    for i, line in enumerate(lines):
        ln = i + 1
        stripped = line.rstrip('\n')
        if len(stripped) >= 7 and stripped[6] == 'c':
            for m in re.finditer(r'\b(\w{3,})\s+\1\b', stripped):
                issues.append("Dittography: '%s'" % m.group())
    
    # --- Check for non-ASCII ---
    for i, line in enumerate(lines):
        ln = i + 1
        stripped = line.rstrip('\n')
        for j, c in enumerate(stripped):
            if ord(c) > 127:
                issues.append("Non-ASCII char U+%04X at col %d: '%s'" % (ord(c), j+1, c))
                break
    
    if issues:
        print("\n--- %s ---" % fname)
        for desc in issues:
            print("  L??: %s" % desc)
    else:
        print("\n--- %s --- (clean)" % fname)

print("\n=== SCAN COMPLETE ===")
