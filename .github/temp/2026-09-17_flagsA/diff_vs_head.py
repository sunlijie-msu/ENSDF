"""Compare col-77 flags in working file vs HEAD for all L-records (check-only)."""
import subprocess

P = r"A34/S34/new/S34_adopted.ens"
cur = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
head = subprocess.run(["git", "show", f"HEAD:{P}"], capture_output=True, text=True,
                      encoding="utf-8", errors="replace").stdout.replace("\r\n", "\n").split("\n")


def lmap(lines):
    m = {}
    for ln in lines:
        if len(ln) >= 80 and ln[6:7] == " " and ln[7:8] == "L":
            m.setdefault(ln[9:19].strip(), []).append(ln)
    return m


cm, hm = lmap(cur), lmap(head)
print("current L-records:", sum(len(v) for v in cm.values()),
      " HEAD L-records:", sum(len(v) for v in hm.values()))
print("--- col77/78-80 differences vs HEAD (E: head_flag -> cur_flag) ---")
n = 0
for e in cm:
    h = hm.get(e)
    if not h:
        print(f"{e:10s} (not in HEAD)")
        continue
    hf = h[0][76:80]
    cf = cm[e][0][76:80]
    if hf != cf:
        n += 1
        print(f"{e:10s} HEAD {hf!r} -> CURRENT {cf!r}")
print("total flag-field diffs:", n)
print("--- full-line hash diffs count ---")
hc = {e: h[0] for e in hm for h in hm[e]}
cc = {e: c[0] for e in cm for c in cm[e]}
sameline = sum(1 for e in cm if e in hc and hc[e] != cc[e])
print("L-lines differing from HEAD (any part):", sameline)
