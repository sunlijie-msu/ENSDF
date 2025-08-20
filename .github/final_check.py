import json

with open('1984CA14_final_corrected.json', 'r') as f:
    data = json.load(f)

# Critical entries verification
critical_entries = [
    '431.2(6)',    # Should be blank
    '435.4(1)',    # Should be 3/2- (A) 
    '636.5(6)',    # Should be blank
    '34.03(1)',    # Should have l = 2 (E)
    '118.30(1)',   # Should be 3/2- (A)
    '1314.5(4)',   # Should be 5/2+ (A)
    '1325.7(4)'    # Should be (1/2-) (B)
]

print('Critical entries final verification:')
for entry in data:
    if entry['En_keV'] in critical_entries:
        en = entry['En_keV']
        jp = entry.get('Jp')
        lt = entry.get('l_transfer')
        print(f'  {en}: Jp="{jp}", l_transfer="{lt}"')
