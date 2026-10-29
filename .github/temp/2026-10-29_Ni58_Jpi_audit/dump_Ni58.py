import sys, io, re

path = r"d:\X\ND\ENSDF\XUNDL\A58\Ni58\new\Ni58_adopted.ens"
with open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = [l.rstrip("\n") for l in f]

def report():
    out = io.StringIO()
    cur = None
    for i, l in enumerate(lines, 1):
        l = l.ljust(80)
        rtype = l[7]
        cont = l[5]
        if rtype == "L" and cont in (" ", "X"):
            cur = (i, l[9:19].strip(), l[21:39].rstrip(), l[39:49].rstrip(), l[49:55].rstrip(),
                   l[55:64].strip(), l[76], l[77:79], l[79], l[6])
            out.write(f"L{i:>5} E={cur[1]:<10} J={cur[2]:<18} T={cur[3]:<9} DT={cur[4]:<6} L={cur[5]:<8} C={cur[6]} MS={cur[7]:<3} Q={cur[8]} flagcol6={cur[9]}\n")
        elif rtype == "G" and cont == " ":
            out.write(f"  G{i:>5} E={l[9:19].strip():<10} RI={l[22:29].strip():<8} DRI={l[29:31].strip():<3} M={l[31:41].strip():<12} MR={l[41:49].strip():<8} DMR={l[49:55].rstrip():<7} CC={l[55:62].strip():<10} TI={l[64:74].strip():<8} FLAG={l[76]}{l[77:80]}\n")
        elif l[6] == "c" and l[7] in ("L", " ") and ("J" in l[9:12] or "BAND" in l[9:20] or l[8] == " " and l[9:10] in "JABCDEFGHKMNOPQRSTUVXYZ"):
            out.write(f"{'c'}{i:>5} {l[5]}{l[6]}{l[7]}| {l[9:].rstrip()}\n")
    return out.getvalue()

txt = report()
with open(r"d:\X\ND\ENSDF\.github\temp\2026-10-29_Ni58_Jpi_audit\dump.txt", "w", encoding="utf-8") as f:
    f.write(txt)
print(len(txt.splitlines()), "lines written")
