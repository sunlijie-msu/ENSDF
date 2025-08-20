import json

# Complete PNG data extraction - line by line verification
# From PNG Table 1 (first page) and Table 2 (second page)

png_data = [
    # Page 1 data
    {"En_keV": "34.03(1)", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "89.40(3)", "Jp": None, "l_transfer": None},
    {"En_keV": "91.12(4)", "Jp": None, "l_transfer": None},
    {"En_keV": "115.2(3)", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "117.4(2)", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "118.30(1)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "162.1(1)", "Jp": None, "l_transfer": None},
    {"En_keV": "231.25(2)", "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "239.0(4)", "Jp": None, "l_transfer": None},
    {"En_keV": "255.5(5)", "Jp": None, "l_transfer": None},
    {"En_keV": "261.5(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "275.3(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "298.70(3)", "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "(302)", "Jp": None, "l_transfer": None},
    {"En_keV": "313.0(8)", "Jp": None, "l_transfer": None},
    {"En_keV": "317.51(5)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "355.41(2)", "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "362.8(2)", "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "368.7(2)", "Jp": None, "l_transfer": None},
    {"En_keV": "372.1(5)", "Jp": None, "l_transfer": None},
    {"En_keV": "372.8(5)", "Jp": None, "l_transfer": None},
    {"En_keV": "379.0(5)", "Jp": None, "l_transfer": None},
    {"En_keV": "382.8(5)", "Jp": None, "l_transfer": None},
    {"En_keV": "396.14(4)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "(397.6)", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "422.3(6)", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "431.2(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "435.4(1)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "438.35(5)", "Jp": None, "l_transfer": None},
    {"En_keV": "443.45(1)", "Jp": None, "l_transfer": None},
    {"En_keV": "456.4(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "461.01(2)", "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "463.9(4)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "469.85(2)", "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "490.5(6)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "510.02(4)", "Jp": None, "l_transfer": None},
    {"En_keV": "523.8(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "573.0(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "636.5(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "641.93(3)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "682.7(6)", "Jp": None, "l_transfer": None},
    {"En_keV": "689.7(6)", "Jp": None, "l_transfer": None},
    
    # Page 2 data
    {"En_keV": "698.2(1)", "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "713.0(7)", "Jp": None, "l_transfer": None},
    {"En_keV": "767.3(7)", "Jp": None, "l_transfer": None},
    {"En_keV": "786.5(4)", "Jp": None, "l_transfer": None},
    {"En_keV": "798.65(6)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "813.8(1)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "836.27(8)", "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "850.94(6)", "Jp": "3/2+ (A)", "l_transfer": None},
    {"En_keV": "893.17(6)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "902.0(12)", "Jp": None, "l_transfer": None},
    {"En_keV": "921.5(12)", "Jp": None, "l_transfer": None},
    {"En_keV": "930.0(12)", "Jp": None, "l_transfer": None},
    {"En_keV": "935.78(6)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "941.0(3)", "Jp": None, "l_transfer": None},
    {"En_keV": "976.4(15)", "Jp": None, "l_transfer": None},
    {"En_keV": "982.0(15)", "Jp": None, "l_transfer": None},
    {"En_keV": "997.9(1)", "Jp": "3/2- (C)", "l_transfer": None},
    {"En_keV": "1017.7(1)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1064.4(2)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1086.7(2)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1123.0(2)", "Jp": None, "l_transfer": "l = 2"},
    {"En_keV": "1124.5(3)", "Jp": None, "l_transfer": "l = 2"},
    {"En_keV": "1140.0(5)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "1192.2(2)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1237.0(3)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "1261.8(3)", "Jp": None, "l_transfer": None},
    {"En_keV": "1275.1(4)", "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "1279.4(4)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1295.5(3)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1308.2(2)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1314.5(4)", "Jp": "5/2+ (A)", "l_transfer": None},
    {"En_keV": "1325.7(4)", "Jp": "(1/2-) (B)", "l_transfer": None},
    {"En_keV": "1351.4(3)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1388.0(4)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1390.1(4)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1447.2(4)", "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1449.6(3)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1462.9(3)", "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1475.5(4)", "Jp": None, "l_transfer": "l = 2 (B)"}
]

print(f"PNG data extracted: {len(png_data)} entries")

# Load current JSON
with open('1984CA14_final_corrected.json', 'r') as f:
    current_data = json.load(f)

print(f"Current JSON: {len(current_data)} entries")

# Compare Jp and l_transfer fields only
mismatches = []
for i, png_entry in enumerate(png_data):
    if i < len(current_data):
        current_entry = current_data[i]
        en = png_entry["En_keV"]
        
        # Check energy match first
        if current_entry["En_keV"] != en:
            mismatches.append(f"Energy mismatch at index {i}: PNG={en}, JSON={current_entry['En_keV']}")
            continue
            
        # Check Jp field
        png_jp = png_entry["Jp"]
        current_jp = current_entry.get("Jp")
        if png_jp != current_jp:
            mismatches.append(f"{en}: Jp mismatch - PNG='{png_jp}', JSON='{current_jp}'")
            
        # Check l_transfer field  
        png_lt = png_entry["l_transfer"]
        current_lt = current_entry.get("l_transfer")
        if png_lt != current_lt:
            mismatches.append(f"{en}: l_transfer mismatch - PNG='{png_lt}', JSON='{current_lt}'")

if mismatches:
    print(f"\nFound {len(mismatches)} mismatches:")
    for mismatch in mismatches:
        print(f"  {mismatch}")
else:
    print("\n✅ ALL Jp and l_transfer fields match perfectly!")

# Update JSON with PNG data to ensure 100% accuracy
print("\nUpdating JSON with PNG-verified data...")
for i, png_entry in enumerate(png_data):
    if i < len(current_data):
        current_data[i]["Jp"] = png_entry["Jp"]
        current_data[i]["l_transfer"] = png_entry["l_transfer"]

# Save the final corrected JSON
with open('1984CA14_final_corrected.json', 'w') as f:
    json.dump(current_data, f, indent=2)

print("✅ Final corrected JSON saved!")

# Verification summary
jp_count = sum(1 for entry in current_data if entry.get('Jp'))
lt_count = sum(1 for entry in current_data if entry.get('l_transfer'))
blank_count = sum(1 for entry in current_data if not entry.get('Jp') and not entry.get('l_transfer'))

print(f"\nFinal verification:")
print(f"  Entries with Jp assignments: {jp_count}")
print(f"  Entries with l_transfer assignments: {lt_count}")  
print(f"  Entries with neither (blank): {blank_count}")
print(f"  Total entries: {len(current_data)}")
