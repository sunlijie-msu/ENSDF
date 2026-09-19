lines=[
" 34S   L 11020     10 1+                                                    E   ",
" 34S X L XREF=T"+" "*48,
" 34S  d"+" "*73,
" 34S   L 11024.95  11 1-                                                    A   "]
print([len(x) for x in lines])
open(r".github\temp\2026-09-18_T-consistency\scratch2.txt","w",encoding="ascii",newline="\r\n").write("\n".join(lines)+"\n")
