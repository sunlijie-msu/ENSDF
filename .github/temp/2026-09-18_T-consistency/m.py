p=r".github\temp\2026-09-18_T-consistency\scratch.txt"
for i,l in enumerate(open(p,"r",encoding="utf-8").read().splitlines()):
    print("%d | len=%d | %r"%(i+1,len(l),l))
