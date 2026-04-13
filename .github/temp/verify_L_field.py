"""
Verify all L-field assignments in S35_36s_p_d.ens match physics.
"""
JP_TO_L = {
    '1/2+': ('0', False), '3/2+': ('2', False), '5/2+': ('2', False),
    '7/2-': ('3', False), '1/2-': ('1', False), '3/2-': ('1', False),
    '7/2+': ('4', False), '1/2-,3/2-': ('1', False), '3/2+,5/2+': ('2', False),
    '(1/2+)': ('0', True), '(3/2+)': ('2', True), '(5/2+)': ('2', True),
    '(7/2-)': ('3', True), '(1/2-)': ('1', True), '(3/2-)': ('1', True),
    '(7/2+)': ('4', True), '(1/2-,3/2-)': ('1', True), '(3/2+,5/2+)': ('2', True),
}

def expected_L_field(digit, tentative):
    if tentative:
        return '(' + digit + ')' + '      '  # 3+6 = 9 chars
    else:
        return digit + '        '  # 1+8 = 9 chars

filepath = r'D:\X\ND\ENSDF\A35\S35\new\S35_36s_p_d.ens'
with open(filepath, 'r') as f:
    lines = [l.rstrip('\n') for l in f.readlines()]

ok = 0
fail = 0
skip = 0

for line in lines:
    if len(line) != 80 or line[7] != 'L' or line[5] != ' ':
        continue
    jp = line[22:39].strip()
    if jp not in JP_TO_L:
        skip += 1
        continue
    digit, tentative = JP_TO_L[jp]
    exp = expected_L_field(digit, tentative)
    actual = line[55:64]  # cols 56-64 (0-indexed 55-63)
    assert len(exp) == 9, f"exp len {len(exp)}"
    assert len(actual) == 9, f"actual len {len(actual)}"
    if actual == exp:
        ok += 1
    else:
        fail += 1
        print(f"FAIL: E={line[9:19].strip():<12} Jpi={jp:<17} got|{actual}| exp|{exp}|")

print(f"\n97-record exhaustive check: {ok} PASS, {fail} FAIL, {skip} SKIPPED")
if fail == 0 and ok == 97:
    print("SUCCESS: All 97 L-field assignments are correct!")
else:
    print("ERROR: Some L-field assignments are wrong or count mismatch!")
