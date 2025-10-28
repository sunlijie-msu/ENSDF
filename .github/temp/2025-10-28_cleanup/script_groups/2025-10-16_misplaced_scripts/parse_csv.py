#!/usr/bin/env python3
"""Parse 2001VO24 CSV to extract gamma transitions"""

csv_data = """
,Ep,,832,1212,1510,1891,1900,2070,2176,2597,2611,2791,
,,,,,,,,,,,,,
,Exi,5645,7179,7547,7838,8207,8216,8381,8484,8893,8907,9081,
Exf,0,,38,,21,78,45,2,4,1,,60,0
Exf,1219,,17,,37,3,,,,,,,1219
Exf,1763,6,,,2,14,1,34,46,19,69,16,1763
Exf,2646,,,1,,,,5,3,,,1,2646
Exf,2694,,4,,,1,3,1,20,37,,2,2694
Exf,3003,80,,2,4,1,5,25,7,,,,3003
Exf,3163,,,95,,,41,,,29,,6,3163
Exf,3918,,3,,,,,24,5,,,9,3918
Exf,3943,,,,1,,,,,4,15,,3943
Exf,3968,,9,,,,,,1,,,,3968
Exf,4059,,22,,2,2,,,,,,,4059
Exf,4113,,,,,,,7,,9,,,4113
Exf,4173,,1,,3,,,,,,,2,4173
Exf,4178,,,,28,,3,,,,,2,4178
Exf,4624,,,,,,,1,1,,,,4624
Exf,477,,,1,,,1,1,,,6,,477
Exf,4839,,2,,,1,,,,,,,4839
Exf,4881,,,,,1,,,7,,,1,4881
Exf,5216,,,,1,,,,,,,,5216
Exf,5586,,,,,,,,,,4,,5586
Exf,5599,,,,1,,,,,1,,,5599
Exf,5646,,,1,,,,,,,2,,5646
Exf,5654,,,,,1,1,,6,,4,,5654
Exf,5724,,,,,,,,,,,1,5724
Exf,6181,,,,1,,,,,,,,6181
,Exi,5645,7179,7547,7838,8207,8216,8381,8484,8893,8907,9081,
"""

lines = csv_data.strip().split('\n')
header_line = lines[2]  # Exi line
headers = header_line.split(',')[2:]  # Skip first two empty cols

print("CSV Headers (Exi values):", headers)

# Find column for Exi=7547
col_idx = headers.index('7547')
print(f"Column index for Exi=7547: {col_idx}\n")

print("2001VO24 L 7547 gamma transitions from CSV:")
print("=" * 60)
print(f"{'Exf (keV)':<12} {'Egamma (keV)':<15} {'RI':<5}")
print("-" * 60)

for i in range(3, len(lines) - 1):
    row = lines[i].split(',')
    exf_label = row[0]
    if exf_label.startswith('Exf'):
        exf_value = row[1]
        # Data starts from column 2, so column col_idx corresponds to index col_idx + 2
        value = row[col_idx + 2] if col_idx + 2 < len(row) else ""
        if value and value.strip():
            egamma = int(7547) - int(exf_value)
            print(f"{exf_value:<12} {egamma:<15} {value:<5}")

print("\n" + "=" * 60)
print("Summary: These are the gamma transitions from L 7547 in CSV")
