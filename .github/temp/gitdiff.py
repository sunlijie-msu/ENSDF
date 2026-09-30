import subprocess, collections
d = subprocess.run(["git", "--no-pager", "diff", "-U0", "--", "A36/S36/new/S36_34s_t_pg.ens"], capture_output=True, text=True, encoding="utf-8").stdout
adds = [l[1:] for l in d.split("\n") if l.startswith("+") and not l.startswith("+++")]
dels = [l[1:] for l in d.split("\n") if l.startswith("-") and not l.startswith("---")]
print("added", len(adds), "deleted", len(dels))
c = collections.Counter(l[6] if len(l) > 6 else "?" for l in adds + dels)
print("col7 chars:", dict(c))
print("non-comment added:", [l[:60] for l in adds if len(l) > 6 and l[6] != "c"])
print("non-comment deleted:", [l[:60] for l in dels if len(l) > 6 and l[6] != "c"])
