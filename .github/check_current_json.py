import json

# Load and check the current 1984CA14_final_corrected.json
with open('1984CA14_final_corrected.json', 'r') as f:
    current_data = json.load(f)

print("🔍 CHECKING CURRENT 1984CA14_final_corrected.json")
print("=" * 60)

# Check the critical entries that were problematic
critical_cases = ['463.9(4)', '490.5(6)', '510.02(4)']

print("Critical cases verification:")
for en_kev in critical_cases:
    entry = next((e for e in current_data if e['En_keV'] == en_kev), None)
    if entry:
        jp = entry.get('Jp')
        lt = entry.get('l_transfer')
        print(f"  {en_kev}: Jp={jp}, l_transfer={lt}")
    else:
        print(f"  ❌ {en_kev}: NOT FOUND!")

# Check if this matches our expected corrections
expected_corrections = {
    '463.9(4)': {'Jp': None, 'l_transfer': 'l = 1,2 (D)'},
    '490.5(6)': {'Jp': None, 'l_transfer': None},
    '510.02(4)': {'Jp': '1/2- (B)', 'l_transfer': None}
}

print("\n✅ VERIFICATION AGAINST EXPECTED CORRECTIONS:")
all_correct = True
for en_kev, expected in expected_corrections.items():
    entry = next((e for e in current_data if e['En_keV'] == en_kev), None)
    if entry:
        actual_jp = entry.get('Jp')
        actual_lt = entry.get('l_transfer')
        expected_jp = expected['Jp']
        expected_lt = expected['l_transfer']
        
        jp_correct = actual_jp == expected_jp
        lt_correct = actual_lt == expected_lt
        
        status = "✅" if (jp_correct and lt_correct) else "❌"
        print(f"  {status} {en_kev}:")
        print(f"    Jp: Expected={expected_jp}, Actual={actual_jp} {'✅' if jp_correct else '❌'}")
        print(f"    l_transfer: Expected={expected_lt}, Actual={actual_lt} {'✅' if lt_correct else '❌'}")
        
        if not (jp_correct and lt_correct):
            all_correct = False
    else:
        print(f"  ❌ {en_kev}: Entry not found!")
        all_correct = False

print(f"\n🎯 OVERALL STATUS: {'✅ ALL CORRECTIONS APPLIED' if all_correct else '❌ CORRECTIONS NOT APPLIED'}")

# Also check total entries
print(f"\n📊 File Statistics:")
print(f"  Total entries: {len(current_data)}")
with_jp = sum(1 for e in current_data if e.get('Jp'))
with_lt = sum(1 for e in current_data if e.get('l_transfer'))
blank = sum(1 for e in current_data if not e.get('Jp') and not e.get('l_transfer'))
print(f"  With Jp: {with_jp}")
print(f"  With l_transfer: {with_lt}")
print(f"  Blank: {blank}")
