import subprocess, collections
d = subprocess.run(["git", "--no-pager", "diff", "-U0", "--", "A36/S36/new/S36_34s_t_pg.ens"], capture_output=True, text=True, encoding="utf-8").stdout
adds = [l[1:] for l in d.split("\n") if l.startswith("+") and not l.startswith("+++")]
dels = [l[1:] for l in d.split("\n") if l.startswith("-") and not l.startswith("---")]
print("added", len(adds), "deleted", len(dels))
print("non-comment:", [l[:70] for l in adds + dels if len(l) > 6 and l[6] != "c"])
