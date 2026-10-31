def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")
COL = [l.rstrip("\n").ljust(80) for l in open(r"XUNDL/A58/Co58/new/Co58_60ni_d_a_pol_d_a.ens", encoding="utf-8", errors="replace")]
CAD = [l.rstrip("\n").ljust(80) for l in open(r"XUNDL/A58/Co58/new/Co58_adopted.ens", encoding="utf-8", errors="replace")]

def show(src, idx, tag):
    l = src[idx-1]
    print(f"  {tag:<4} line {idx:>5}: E={l[9:19].strip():>9} DE={l[19:21].strip()!r:<5} J={l[22:39].strip()!r:<10} L={l[55:64].strip()!r} S={l[64:74].strip()!r}")

print("### Ni-58 case 1: 6460-6480 (letter C = 58Ni(p,p'))")
for n in (472, 473, 477, 479): show(C, n, "ds")
for n in (844, 847, 852): show(AD, n, "ad")
print("  adopted XREF lines: :845", AD[844][9:80].rstrip(), "| :848", AD[847][9:80].rstrip(), "| :853", AD[852][9:80].rstrip())

print("\n### Ni-58 case 2: 6835-6865")
for n in (511, 513): show(C, n, "ds")
for n in (923, 928): show(AD, n, "ad")
print("  adopted XREF lines: :924", AD[923][9:80].rstrip(), "| :929", AD[928][9:80].rstrip())

print("\n### Ni-58 case 3: 7550-7625")
for n in (565, 567, 568): show(C, n, "ds")
for n in (1074, 1081, 1083, 1087): show(AD, n, "ad")
print("  adopted XREF lines: :1075", AD[1074][9:80].rstrip(), "| :1082", AD[1081][9:80].rstrip(),
      "| :1084", AD[1083][9:80].rstrip(), "| :1088", AD[1087][9:80].rstrip())

print("\n### Ni-58 case 4: 9450-9465")
for n in (700, 701): show(C, n, "ds")
for n in (1425, 1429): show(AD, n, "ad")
print("  adopted XREF lines: :1426", AD[1425][9:80].rstrip(), "| :1430", AD[1429][9:80].rstrip())

print("\n### Ni-58 case 5: 9625-9640")
for n in (711, 712): show(C, n, "ds")
for n in (1454, 1460): show(AD, n, "ad")
print("  adopted XREF lines: :1455", AD[1454][9:80].rstrip(), "| :1461", AD[1460][9:80].rstrip())

print("\n### Ni-58 case 6: 11030-11085")
for n in (816, 818, 820): show(C, n, "ds")
for n in (1737, 1740, 1743): show(AD, n, "ad")
print("  adopted XREF lines: :1738", AD[1737][9:80].rstrip(), "| :1741", AD[1740][9:80].rstrip(),
      "| :1744", AD[1743][9:80].rstrip())

print("\n### Co-58: (d,a) = letter S, window 2820-2870")
for n in (75, 76): show(COL, n, "ds")
for n in (723, 725, 728): show(CAD, n, "ad")
print("  adopted XREF lines: :724", CAD[723][9:80].rstrip(), "| :726", CAD[725][9:80].rstrip(),
      "| :729", CAD[728][9:80].rstrip())
