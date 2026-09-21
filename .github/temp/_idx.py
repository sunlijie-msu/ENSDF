for f,ln in ((r"A33_2025Ch07.ens",10351),(r"A34\S34\new\S34_adopted.ens",326),(r"A34\P34\new\P34_adopted.ens",126)):
    L=open(f,encoding="ascii",errors="replace").read().split("\n")
    s=L[ln-1].rstrip("\r")
    print(f.split("\\")[-1],ln,repr(s))
    print("  col32:",repr(s[31:32]),"col33:",repr(s[32:33]),"field33-41:",repr(s[32:41]))
