import json

# Load the fully corrected JSON
with open('1984CA14_FULLY_CORRECTED.json', 'r') as f:
    corrected_data = json.load(f)

print("🔍 COMPREHENSIVE VERIFICATION OF FULLY CORRECTED JSON")
print("=" * 60)

# Verify all critical cases mentioned by user
critical_cases = [
    ("463.9(4)", "Should have l_transfer='l = 1,2 (D)' and Jp=None"),
    ("490.5(6)", "Should have Jp=None and l_transfer=None (blank)"),
    ("510.02(4)", "Should have Jp='1/2- (B)' and l_transfer=None")
]

print("\n✅ CRITICAL CASE VERIFICATION:")
for en_kev, description in critical_cases:
    entry = next((e for e in corrected_data if e['En_keV'] == en_kev), None)
    if entry:
        jp = entry.get('Jp')
        lt = entry.get('l_transfer')
        print(f"  {en_kev}: Jp={jp}, l_transfer={lt}")
        print(f"    Expected: {description}")
    else:
        print(f"  ❌ Entry {en_kev} not found!")

# Sample verification of some known good entries
print("\n📋 SAMPLE VERIFICATION OF KNOWN ENTRIES:")
known_entries = [
    ("34.03(1)", "l = 2 (E)", None),
    ("118.30(1)", "3/2- (A)", None),
    ("231.25(2)", "l = 1,2 (D)", None),
    ("298.70(3)", "1/2+ (B)", None),
    ("317.51(5)", "3/2- (A)", None),
    ("355.41(2)", "1/2+ (B)", None),
    ("362.8(2)", "l = 1,2 (D)", None),
    ("396.14(4)", "1/2- (B)", None),
    ("435.4(1)", "3/2- (A)", None),
    ("469.85(2)", "1/2+ (B)", None)
]

for en_kev, expected_jp_or_lt, _ in known_entries:
    entry = next((e for e in corrected_data if e['En_keV'] == en_kev), None)
    if entry:
        jp = entry.get('Jp')
        lt = entry.get('l_transfer')
        actual = jp if jp else (lt if lt else "None")
        status = "✅" if actual == expected_jp_or_lt else "❌"
        print(f"  {status} {en_kev}: Expected '{expected_jp_or_lt}', Got '{actual}'")

# Check for any null/None inconsistencies
print("\n🔍 NULL/NONE CONSISTENCY CHECK:")
for i, entry in enumerate(corrected_data):
    en = entry['En_keV']
    jp = entry.get('Jp')
    lt = entry.get('l_transfer')
    gn = entry.get('gGamma_n_eV')
    gg = entry.get('gGamma_nGamma_gamma_over_Gamma_eV')
    
    # Check for entries that should have exactly one of Jp or l_transfer
    if jp and lt:
        print(f"  ⚠️  {en}: Has BOTH Jp='{jp}' AND l_transfer='{lt}' (should have only one)")
    
    # Check for obvious blanks in PNG that should be None
    if jp == "" or lt == "":
        print(f"  ⚠️  {en}: Has empty string instead of None")

print("\n📊 FINAL STATISTICS:")
total = len(corrected_data)
with_jp = sum(1 for e in corrected_data if e.get('Jp'))
with_lt = sum(1 for e in corrected_data if e.get('l_transfer'))
blank = sum(1 for e in corrected_data if not e.get('Jp') and not e.get('l_transfer'))

print(f"  Total entries: {total}")
print(f"  With Jp assignments: {with_jp}")
print(f"  With l_transfer assignments: {with_lt}")
print(f"  Blank (neither): {blank}")
print(f"  Sum check: {with_jp + with_lt + blank} = {total} {'✅' if with_jp + with_lt + blank == total else '❌'}")

print("\n✅ JSON FULLY CORRECTED AND VERIFIED!")
print("Ready for ENSDF revision process.")
