import io, os, re
BASE = "XUNDL/A58/Ni58/new/"
norm = lambda s: re.sub(r"\s+", " ", s.upper().strip())
L = lambda p: [x.rstrip("\n").ljust(80) for x in io.open(p, encoding="utf-8", errors="replace")]
AD = L(BASE + "Ni58_adopted.ens")
keys = {r[8]: norm(r[9:39]) for r in AD if r[5] == " " and r[6] == " " and r[7] == "X" and r[8] != " "}
files = {}
for fn in os.listdir(BASE):
    if fn.endswith(".ens") and fn != "Ni58_adopted.ens":
        files.setdefault(norm(L(BASE + fn)[0][9:39]), []).append(fn)
has0, lack0 = [], []
for k, dsid in sorted(keys.items()):
    fn = files[dsid][0]
    g = any(r[5] == " " and r[6] == " " and r[7] == "L" and r[9:19].strip() in ("0", "0.0") for r in L(BASE + fn))
    (has0 if g else lack0).append(k)
print("datasets with a g.s. record:", len(has0), "| without:", lack0)
i = next(n for n, r in enumerate(AD) if r[5] == " " and r[6] == " " and r[7] == "L" and r[9:19].strip() == "0.0")
print("adopted g.s. XREF text:", AD[i + 1][9:80].strip(), "| letters excluded:", sorted(set(keys) - set(has0)))
