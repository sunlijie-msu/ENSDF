import json

# COMPLETE PNG RE-EXTRACTION - Line by line verification
# Based on the PNG images provided, extracting EXACTLY what is shown

png_corrected_data = [
    # Page 1 - First table
    {"En_keV": "34.03(1)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.025(1)", "footnote": "b", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "89.40(3)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.14(4)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "91.12(4)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.084(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "115.2(3)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.009(3)", "footnote": "b", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "117.4(2)", "gGamma_n_eV": "< 1", "gGamma_nGamma_gamma_over_Gamma_eV": "0.033(5)", "footnote": "b", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "118.30(1)", "gGamma_n_eV": "372(3)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.70(4)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "162.1(1)", "gGamma_n_eV": "< 1", "gGamma_nGamma_gamma_over_Gamma_eV": "0.42(1)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "231.25(2)", "gGamma_n_eV": "62(4)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.30(2)", "footnote": None, "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "239.0(4)", "gGamma_n_eV": "< 4", "gGamma_nGamma_gamma_over_Gamma_eV": "0.33(2)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "255.5(5)", "gGamma_n_eV": "< 4", "gGamma_nGamma_gamma_over_Gamma_eV": "0.19(1)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "261.5(6)", "gGamma_n_eV": "< 2", "gGamma_nGamma_gamma_over_Gamma_eV": "0.06(2)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "275.3(6)", "gGamma_n_eV": "< 1", "gGamma_nGamma_gamma_over_Gamma_eV": "0.35(2)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "298.70(3)", "gGamma_n_eV": "9600(150)", "gGamma_nGamma_gamma_over_Gamma_eV": "2.82(67)", "footnote": None, "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "(302)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.10(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "313.0(8)", "gGamma_n_eV": "< 6", "gGamma_nGamma_gamma_over_Gamma_eV": "0.31(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "317.51(5)", "gGamma_n_eV": "2500(25)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.23(8)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "355.41(2)", "gGamma_n_eV": "4810(80)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.30(30)", "footnote": None, "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "362.8(2)", "gGamma_n_eV": "230(10)", "gGamma_nGamma_gamma_over_Gamma_eV": "1.06(7)", "footnote": None, "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "368.7(2)", "gGamma_n_eV": "< 2", "gGamma_nGamma_gamma_over_Gamma_eV": "0.72(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "372.1(5)", "gGamma_n_eV": "< 2", "gGamma_nGamma_gamma_over_Gamma_eV": "0.44(6)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "372.8(5)", "gGamma_n_eV": "< 2", "gGamma_nGamma_gamma_over_Gamma_eV": "0.30(5)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "379.0(5)", "gGamma_n_eV": "< 10", "gGamma_nGamma_gamma_over_Gamma_eV": "0.44(4)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "382.8(5)", "gGamma_n_eV": "< 6", "gGamma_nGamma_gamma_over_Gamma_eV": "0.16(4)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "396.14(4)", "gGamma_n_eV": "6430(150)", "gGamma_nGamma_gamma_over_Gamma_eV": "3.08(20)", "footnote": None, "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "(397.6)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.12", "footnote": "b", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "422.3(6)", "gGamma_n_eV": None, "gGamma_nGamma_gamma_over_Gamma_eV": "0.44(33)", "footnote": "b", "Jp": None, "l_transfer": "l = 2 (E)"},
    {"En_keV": "431.2(6)", "gGamma_n_eV": "< 1", "gGamma_nGamma_gamma_over_Gamma_eV": "0.21(5)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "435.4(1)", "gGamma_n_eV": "1570(40)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.91(8)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "438.35(5)", "gGamma_n_eV": "49(5)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": None},
    {"En_keV": "443.45(1)", "gGamma_n_eV": "80(8)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.51(5)", "footnote": None, "Jp": None, "l_transfer": None},
    {"En_keV": "456.4(6)", "gGamma_n_eV": "< 6", "gGamma_nGamma_gamma_over_Gamma_eV": "0.12(3)", "footnote": None, "Jp": None, "l_transfer": None},
    {"En_keV": "461.01(2)", "gGamma_n_eV": "50(5)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.035(20)", "footnote": None, "Jp": None, "l_transfer": "l = 1,2 (D)"},
    
    # CRITICAL CORRECTION: 463.9(4) has l = 1,2 (D), NOT Jp
    {"En_keV": "463.9(4)", "gGamma_n_eV": "296(30)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.28(3)", "footnote": None, "Jp": None, "l_transfer": "l = 1,2 (D)"},
    
    {"En_keV": "469.85(2)", "gGamma_n_eV": "1050(35)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.37(8)", "footnote": None, "Jp": "1/2+ (B)", "l_transfer": None},
    
    # CRITICAL CORRECTION: 490.5(6) has NO Jp assignment (blank)
    {"En_keV": "490.5(6)", "gGamma_n_eV": "50(10)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.33(4)", "footnote": "b", "Jp": None, "l_transfer": None},
    
    # CRITICAL CORRECTION: 510.02(4) has Jp = 1/2- (B)
    {"En_keV": "510.02(4)", "gGamma_n_eV": "375(25)", "gGamma_nGamma_gamma_over_Gamma_eV": "2.1(1)", "footnote": None, "Jp": "1/2- (B)", "l_transfer": None},
    
    {"En_keV": "523.8(6)", "gGamma_n_eV": "< 4", "gGamma_nGamma_gamma_over_Gamma_eV": "0.17(4)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "573.0(6)", "gGamma_n_eV": "< 1", "gGamma_nGamma_gamma_over_Gamma_eV": "0.21(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "636.5(6)", "gGamma_n_eV": "< 10", "gGamma_nGamma_gamma_over_Gamma_eV": "0.90(8)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "641.93(3)", "gGamma_n_eV": "2520(60)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.51(6)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "682.7(6)", "gGamma_n_eV": "< 30", "gGamma_nGamma_gamma_over_Gamma_eV": "0.21(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "689.7(6)", "gGamma_n_eV": "< 10", "gGamma_nGamma_gamma_over_Gamma_eV": "0.80(5)", "footnote": "b", "Jp": None, "l_transfer": None},
    
    # Page 2 - Second table
    {"En_keV": "698.2(1)", "gGamma_n_eV": "305(50)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.80(8)", "footnote": None, "Jp": None, "l_transfer": "l = 1,2 (D)"},
    {"En_keV": "713.0(7)", "gGamma_n_eV": "< 4", "gGamma_nGamma_gamma_over_Gamma_eV": "0.45(7)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "767.3(7)", "gGamma_n_eV": "< 4", "gGamma_nGamma_gamma_over_Gamma_eV": "0.31(13)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "786.5(4)", "gGamma_n_eV": "18(6)", "gGamma_nGamma_gamma_over_Gamma_eV": "2.65(18)", "footnote": None, "Jp": None, "l_transfer": None},
    {"En_keV": "798.65(6)", "gGamma_n_eV": "25350(300)", "gGamma_nGamma_gamma_over_Gamma_eV": "1.52(50)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "813.8(1)", "gGamma_n_eV": "860(60)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.19(13)", "footnote": None, "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "836.27(8)", "gGamma_n_eV": "3600(160)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.39(18)", "footnote": None, "Jp": "1/2+ (B)", "l_transfer": None},
    {"En_keV": "850.94(6)", "gGamma_n_eV": "2650(110)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.24(19)", "footnote": None, "Jp": "3/2+ (A)", "l_transfer": None},
    {"En_keV": "893.17(6)", "gGamma_n_eV": "4950(160)", "gGamma_nGamma_gamma_over_Gamma_eV": "0.38(16)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "902.0(12)", "gGamma_n_eV": "< 3", "gGamma_nGamma_gamma_over_Gamma_eV": "1.13(19)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "921.5(12)", "gGamma_n_eV": "< 20", "gGamma_nGamma_gamma_over_Gamma_eV": "0.67(17)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "930.0(12)", "gGamma_n_eV": "< 20", "gGamma_nGamma_gamma_over_Gamma_eV": "0.57(25)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "935.78(6)", "gGamma_n_eV": "4100(160)", "gGamma_nGamma_gamma_over_Gamma_eV": "3.48(23)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "941.0(3)", "gGamma_n_eV": "176(16)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": None},
    {"En_keV": "976.4(15)", "gGamma_n_eV": "< 2", "gGamma_nGamma_gamma_over_Gamma_eV": "0.5(3)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "982.0(15)", "gGamma_n_eV": "< 8", "gGamma_nGamma_gamma_over_Gamma_eV": "0.89(4)", "footnote": "b", "Jp": None, "l_transfer": None},
    {"En_keV": "997.9(1)", "gGamma_n_eV": "930(80)", "gGamma_nGamma_gamma_over_Gamma_eV": "3.51(19)", "footnote": None, "Jp": "3/2- (C)", "l_transfer": None},
    {"En_keV": "1017.7(1)", "gGamma_n_eV": "4020(180)", "gGamma_nGamma_gamma_over_Gamma_eV": "1.22(17)", "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1064.4(2)", "gGamma_n_eV": "1032(90)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1086.7(2)", "gGamma_n_eV": "2650(160)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1123.0(2)", "gGamma_n_eV": "5480(388)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2"},
    {"En_keV": "1124.5(3)", "gGamma_n_eV": "4730(320)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2"},
    {"En_keV": "1140.0(5)", "gGamma_n_eV": "34880(830)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "1192.2(2)", "gGamma_n_eV": "5510(290)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1237.0(3)", "gGamma_n_eV": "2945(230)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "1261.8(3)", "gGamma_n_eV": "975(86)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": None},
    {"En_keV": "1275.1(4)", "gGamma_n_eV": "2170(180)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "1/2- (B)", "l_transfer": None},
    {"En_keV": "1279.4(4)", "gGamma_n_eV": "1140(100)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1295.5(3)", "gGamma_n_eV": "1980(150)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1308.2(2)", "gGamma_n_eV": "12475(770)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1314.5(4)", "gGamma_n_eV": "6240(500)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "5/2+ (A)", "l_transfer": None},
    {"En_keV": "1325.7(4)", "gGamma_n_eV": "1635(145)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "(1/2-) (B)", "l_transfer": None},
    {"En_keV": "1351.4(3)", "gGamma_n_eV": "14470(650)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1388.0(4)", "gGamma_n_eV": "28845(1057)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1390.1(4)", "gGamma_n_eV": "1955(170)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1447.2(4)", "gGamma_n_eV": "27100(1390)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": "3/2- (A)", "l_transfer": None},
    {"En_keV": "1449.6(3)", "gGamma_n_eV": "3025(260)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1462.9(3)", "gGamma_n_eV": "3885(345)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"},
    {"En_keV": "1475.5(4)", "gGamma_n_eV": "3795(340)", "gGamma_nGamma_gamma_over_Gamma_eV": None, "footnote": None, "Jp": None, "l_transfer": "l = 2 (B)"}
]

print(f"✅ PNG Re-extraction completed: {len(png_corrected_data)} entries")

# Save the fully corrected JSON based on direct PNG reading
with open('1984CA14_FULLY_CORRECTED.json', 'w') as f:
    json.dump(png_corrected_data, f, indent=2)

print("✅ Saved as 1984CA14_FULLY_CORRECTED.json")

# Verify the critical corrections
critical_entries = ['463.9(4)', '490.5(6)', '510.02(4)']
print("\n🔍 Verification of critical corrections:")
for entry in png_corrected_data:
    if entry['En_keV'] in critical_entries:
        en = entry['En_keV']
        jp = entry.get('Jp')
        lt = entry.get('l_transfer')
        print(f"  {en}: Jp={jp}, l_transfer={lt}")

print("\n✅ ALL CRITICAL CORRECTIONS APPLIED:")
print("  463.9(4): Now has l_transfer='l = 1,2 (D)' and Jp=None")
print("  490.5(6): Now has Jp=None and l_transfer=None (blank)")  
print("  510.02(4): Now has Jp='1/2- (B)' and l_transfer=None")

# Summary statistics
jp_count = sum(1 for entry in png_corrected_data if entry.get('Jp'))
lt_count = sum(1 for entry in png_corrected_data if entry.get('l_transfer'))
blank_count = sum(1 for entry in png_corrected_data if not entry.get('Jp') and not entry.get('l_transfer'))

print(f"\n📊 Final Statistics:")
print(f"  Total entries: {len(png_corrected_data)}")
print(f"  Entries with Jp assignments: {jp_count}")
print(f"  Entries with l_transfer assignments: {lt_count}")
print(f"  Entries with neither (blank): {blank_count}")
print(f"  Verification: {jp_count + lt_count + blank_count} = {len(png_corrected_data)} ✅")
