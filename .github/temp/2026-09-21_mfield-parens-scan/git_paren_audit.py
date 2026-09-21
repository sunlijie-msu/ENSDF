"""Read-only history audit: for every commit whose diff changed a G-record M field,
report the old/new M field AND whether the record's comment block (in the PREVIOUS
revision) cited RUL or POL.  Uses `git show rev:path` (no checkout, no restore)."""
import subprocess

REPO = r"d:\X\ND\ENSDF"
PATH = "A34/S34/new/S34_adopted.ens"
OUT = r"d:\X\ND\ENSDF\.github\temp\2026-09-21_mfield-parens-scan\git_paren_audit.txt"


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout


def recs(lines):
    """map energy (E field) -> (lineidx, M field, comment list) for G records"""
    out = []
    cur = None
    for i, s in enumerate(lines):
        if len(s) < 8:
            continue
        cont = s[5:6] != " "
        kind = s[7:8]
        if s[6:7] == "c":
            if cur is not None:
                cur["c"].append(s[9:].rstrip())
            continue
        if kind == "G" and not cont:
            cur = dict(idx=i, e=s[9:19].strip(), m=s[32:41].strip(), c=[])
            out.append(cur)
    return out


log = git("log", "--reverse", "--format=%H|%ad|%s", "--date=short", "--", PATH)
commits = [l.split("|", 2) for l in log.strip().split("\n") if l]

out = []
prev = None
for h, d, subj in commits:
    text = git("show", h + ":" + PATH)
    lines = text.split("\n")
    cur = recs(lines)
    if prev is not None:
        pm = {r["e"]: r for r in prev}
        changed = []
        for r in cur:
            p = pm.get(r["e"])
            if p is None:
                continue
            if p["m"] != r["m"]:
                changed.append((r, p))
        for r, p in changed:
            txt = " ".join(p["c"])
            rul = "RUL" in txt
            pol = "POL" in txt
            flag = "  <<< RUL-CITING" if (rul or pol) else ""
            out.append("%s %s %s%s" % (h[:8], d, subj[:60], flag))
            out.append("    E=%-10s  M: %-11s -> %-11s  (new line %d)"
                       % (r["e"], p["m"], r["m"], r["idx"] + 1))
            if p["m"].find("(") < 0 and r["m"].find("(") >= 0:
                out.append("        firm->paren; prior comment: %s"
                           % (txt[:150] if txt else "(none)"))
    prev = cur

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("lines:", len(out), "->", OUT)
