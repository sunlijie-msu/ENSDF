import pathlib, re
out = pathlib.Path(".github/temp/lifetimes.txt")
lines_out = []
for f in sorted(pathlib.Path("A36/S36/new").glob("*.ens")):
    ls = f.read_text(encoding="utf-8", errors="replace").split("\n")
    cur = None
    for i, l in enumerate(ls, 1):
        if len(l) > 9 and l[7:8] == "L":
            cur = (i, l[9:19].strip() or l[9:19])
        if len(l) > 9 and l[6] == "c" and l[8:9] == "L":
            body = l[9:].rstrip()
            if "T$" in l[9:13] or "lifetime" in body.lower() or "|t" in body:
                lines_out.append(f'{f.name} | L {cur[0] if cur else "?"} E={cur[1] if cur else "?"} | line {i} | {body}')
for x in lines_out:
    print(x)
print("total:", len(lines_out))
