import pathlib
p = pathlib.Path(".github/temp/ws_test.txt")
lines = [" 36S  cG RI$from 1972Sa09.  other: 51 {I2} for a doublet sum (1971Ol02).        ",
         " 36S  cG M,MR$+0.05 {I13}"]
p.write_bytes(("\n".join(lines) + "\n").encode())
print(repr(p.read_bytes().decode()))
