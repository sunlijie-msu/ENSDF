L=open(r"A34\S34\new\S34_adopted.ens",encoding="ascii",errors="replace").read().split("\n")
for n in (364,370,376,504,726,732,1055,811,837):
    s=L[n-1].rstrip("\n")
    tail=[(i+1,ch) for i,ch in enumerate(s) if i>=62 and ch!=" "]
    print(n,"len=%d"%len(s),"tail(nonblank cols>=63):",[(c,repr(ch)) for c,ch in tail], "|col77=%r col78=%r col79=%r col80=%r"%(s[76:77],s[77:78],s[78:79],s[79:80]))
