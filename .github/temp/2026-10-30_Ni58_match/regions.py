import re
D=r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/"
def lines(p): return [l.ljust(80) for l in open(p,encoding="utf-8",errors="replace").read().split("\n")]
AD=lines(D+"Ni58_adopted.ens")
def show(lo,hi):
    print(f"\n--- adopted levels {lo}-{hi} ---")
    for i,l in enumerate(AD,1):
        try: v=float(l[9:19])
        except: continue
        if l[5]==" " and l[6]==" " and l[7]=="L" and lo<=v<=hi:
            x=AD[i][9:80].rstrip() if (i<len(AD) and AD[i][5]=="X") else "(no XREF next line)"
            print(f"  L{i}: E={l[9:19].strip()} ± {l[19:21].strip()!r} J={l[22:39].strip()!r}")
            print(f"        {x}")
show(6450,6490); show(6830,6870); show(7550,7660); show(9440,9480); show(9610,9650); show(11020,11100)
