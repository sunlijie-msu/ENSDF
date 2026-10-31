import io, sys, runpy
p = r".github/temp/2026-10-30_Ni58_match/pp_md.md"
f = io.open(p, "w", encoding="utf-8")
sys.stdout = f
runpy.run_path(r".github/temp/2026-10-30_Ni58_match/pp_md.py", run_name="__main__")
f.close()
sys.stdout = sys.__stdout__
print("wrote", p)
