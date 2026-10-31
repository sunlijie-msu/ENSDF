import io, sys
src = io.open(r".github/temp/2026-10-31_xref2/xref_ownership2.py", encoding="utf-8").read()
old = 'd > max(a["s"] + P[i]["s"], 0.5)'
assert old in src
src = src.replace(old, 'd > a["s"] + 1e-9')
sys.argv = ["x", "XUNDL/A58/Ni58/new/", "Ni58_adopted.ens", ".github/temp/2026-10-31_xref2/report_literal.md"]
exec(compile(src, "xref_literal", "exec"))
