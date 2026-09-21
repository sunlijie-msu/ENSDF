import re
rulers=("1234567890"*8)
for f,ln in ((r"A33_2025Ch07.ens",10351),(r"A33_2025Ch07.ens",3526),(r"A32_2025Ch19.ens",2133),(r"A34\P34\new\P34_adopted.ens",127),(r"A34\S34\new\S34_adopted.ens",326)):
    L=open(f,encoding="ascii",errors="replace").read().split("\n")
    # find the G record nearest: search backwards for a line with col8 G
    for j in range(ln-1,max(0,ln-40),-1):
        s=L[j]
        if len(s)>8 and s[5]==" " and s[7]=="G":
            print(f.split("\\")[-1], "line",j+1,"len",len(s.rstrip("\r")))
            print("   ones:",rulers[:80])
            print("   line:",s.rstrip("\r").ljust(80))
            break
