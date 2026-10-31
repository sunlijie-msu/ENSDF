import runpy, sys, io
# reuse the same module code by exec with modification: print n<=6
src = open(r"d:/X/ND/ENSDF/.github/temp/2026-10-30_Ni58_reaudit/deduce2.py", encoding="utf-8").read()
src = src.replace("if 0 < n <= 3 and used:", "if 0 < n <= 6 and used:")
src = src.replace('for label, use in (("STRICT (measured M only)", False), ("WITH D-or-E2 ASSUMPTION for blank M", True)):',
                  'for label, use in (("STRICT", False), ("WITH", True)):')
ns = {"__name__": "__main__"}
exec(compile(src, "mod", "exec"), ns)
