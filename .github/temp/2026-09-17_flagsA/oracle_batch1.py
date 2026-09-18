"""Oracle: validate my literal edit strings against the file BEFORE sending them.

If a literal is wrong, the script prints the exact deviation
(length, run counts, first mismatch offset) so the literal can be fixed here.
"""
P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")

SUF = "\n 34S X L XREF=L         "

CASES = {}
def add(digits, old_run, new_run):
    CASES[digits] = (" 34S   L " + digits + "     5" + old_run + "A   " + SUF,
                     " 34S   L " + digits + "     5" + new_run + SUF)

# runs: old pre-A = 56 spaces, tail = A + 3 spaces; new pre-A = 60 spaces
R56 = "          " * 5 + "      "          # 56
R60 = "          " * 6                      # 60
for d in ["10447", "10528", "10617", "10869", "10895", "10917", "11180", "11194", "11289"]:
    add(d, R56, R60)

for d, (old, new) in CASES.items():
    c_old, c_new = raw.count(old), raw.count(new)
    ok = c_old == 1 and c_new == 0
    print(f"{d}: old-count={c_old} new-count={c_new} {'OK' if ok else '--> CHECK'}")
    if not ok:
        # find the actual line and report diagnostics
        target = " 34S   L " + d
        for ln in raw.split("\n"):
            if ln.startswith(target):
                a_my = old.index("A")
                a_file = ln.index("A")
                print(f"    my old len={len(old)}  a-my={a_my}  a-file={a_file}")
                print(f"    my old repr: {old[:90]!r}")
                print(f"    file repr  : {(ln + chr(10) + ' 34S X L XREF=L         ')[:90]!r}")
                mm = next((k for k in range(min(len(old), 90)) if old[k] != (ln + "\n")[k]), None)
                print(f"    first mismatch at offset: {mm}")
                break
