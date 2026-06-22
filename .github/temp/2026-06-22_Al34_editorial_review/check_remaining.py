"""Check remaining issues like S(A)$ and L$ standalone patterns."""
import re

# Check S(A)$ in pb file
lines_to_check = {
    "Al34_pb_35al_34alng.ens": [
        '34AL cL S(A)$Sum |s for g.s.+ 46 isomer.',
    ],
    "Al34_adopted.ens": [
        '34AL cL $%|b{+-}n: weighted average of 22 {I5}',
        '34AL cL $Strong absorption r{-0}{+2}=1.187 fm{+2}',
    ],
}

for fname, lines in lines_to_check.items():
    print("--- %s ---" % fname)
    for line in lines:
        comment_part = line[7:]  # skip NUCID + continuation + 'c'
        
        # Check for field identifier (with parentheses support)
        m = re.match(r'[LGBENPQ]?\s*([A-Z][A-Z,()]*)\$(.+)', comment_part)
        if m:
            field_id = m.group(1)
            text = m.group(2)
            first_word = text.lstrip()
            fw = first_word.split()[0] if first_word.split() else ''
            print("  Field ID: '%s', text: '%s', first word: '%s'" % (field_id, text[:40], fw))
            if fw and fw[0].isupper():
                is_exception = (
                    fw[0].isdigit() or
                    fw.startswith('{') or
                    fw.startswith('|') or
                    fw.startswith('(') or
                    fw.startswith('[') or
                    fw == 'I'
                )
                if is_exception:
                    print("    -> Exception, OK")
                else:
                    print("    -> ISSUE: should be lowercase")
        else:
            print("  No field match for: %s" % comment_part[:50])
