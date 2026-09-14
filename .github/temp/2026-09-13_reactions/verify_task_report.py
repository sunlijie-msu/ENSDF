import subprocess, sys, collections

PATH = "A34/S34/new/S34_adopted.ens"
REPO = r"d:\X\ND\ENSDF"

def git_show():
    p = subprocess.run(["git","show","HEAD:"+PATH], cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        print("GIT ERROR:", p.stderr.decode()); sys.exit(1)
    return p.stdout

def load(b):
    lines = b.split(b"\n")
    # drop trailing empty element caused by final newline
    if lines and lines[-1] == b"":
        lines.pop()
    return [ln[:-1] if ln.endswith(b"\r") else ln for ln in lines]

head = load(git_show())
with open(REPO + "\\" + PATH.replace("/", "\\"), "rb") as f:
    wt = load(f.read())

print("HEAD lines:", len(head), " WT lines:", len(wt))

def cls(line):
    if len(line) < 7:
        return "SHORT"
    c7 = line[6:7]
    if c7 == b" ":
        return "data"
    return "comment"

data_changed, comment_changed, trail_only = [], [], []
len_changed_content_same = []
n = max(len(head), len(wt))
for i in range(n):
    h = head[i] if i < len(head) else None
    w = wt[i] if i < len(wt) else None
    if h == w:
        continue
    hh = h if h is not None else b"<MISSING>"
    ww = w if w is not None else b"<MISSING>"
    rec = (i+1, cls(hh), cls(ww), len(hh), len(ww), hh, ww)
    if h is not None and w is not None and h.rstrip() == w.rstrip():
        trail_only.append(rec)
        continue
    (data_changed if cls(hh) == "data" else comment_changed).append(rec)
    if h is not None and w is not None:
        if len(h) != len(w) and h.strip() == w.strip():
            len_changed_content_same.append(rec)

print("\n=== COUNTS ===")
print("changed DATA-record lines :", len(data_changed))
print("changed COMMENT lines     :", len(comment_changed))
print("trailing-space-only lines :", len(trail_only))

print("\n=== DATA RECORDS: char-level diffs ===")
for (ln, ch, cw, lh, lw, hh, ww) in data_changed:
    diffs = [(j+1, chr(hh[j]) if j < len(hh) else "<none>",
              chr(ww[j]) if j < len(ww) else "<none>")
             for j in range(max(len(hh), len(ww)))
             if (hh[j:j+1] or b"") != (ww[j:j+1] or b"")]
    only77 = all(d[0] == 77 for d in diffs)
    print(f"L{ln}: cls={ch} len {lh}->{lw} len80_wt={lw==80} diffs={diffs} only_col77={only77}")

print("\n=== COMMENT RECORDS ===")
for (ln, ch, cw, lh, lw, hh, ww) in comment_changed:
    print(f"L{ln}: len {lh}->{lw}")
    print("   HEAD:", repr(hh.decode('ascii','replace')))
    print("   WT  :", repr(ww.decode('ascii','replace')))

print("\n=== TRAILING-SPACE-ONLY (length-change collateral) ===")
for (ln, ch, cw, lh, lw, hh, ww) in trail_only:
    tag = "LENGTH-CHANGE+content-same" if (hh.strip() != ww.strip() or len(hh) != len(ww)) else "same-len"
    flag = "*** CONTENT-IDENTICAL-EXCEPT-TRAILING ***" if hh.strip() == ww.strip() else ""
    print(f"L{ln}: cls={ch} len {lh}->{lw} {flag}")
    print("   HEAD:", repr(hh.decode('ascii','replace')))
    print("   WT  :", repr(ww.decode('ascii','replace')))

print("\n=== LENGTH-CHANGED BUT CONTENT(minus trailing) IDENTICAL ===")
for (ln, ch, cw, lh, lw, hh, ww) in len_changed_content_same:
    print(f"L{ln}: cls={ch} len {lh}->{lw}  HEAD.strip={hh.strip()!r}")

# item 2: ten flagged gammas
ENERGIES = ["1856","2043","3428","4604","2176","2242","4737","3809","4985","7111"]
print("\n=== ITEM 2: flagged G records ===")
gidx = [i for i, l in enumerate(wt) if len(l) >= 8 and l[7:8] == b"G"]
for e in ENERGIES:
    hits = [i for i in gidx if wt[i][9:19].split() and wt[i][9:19].split()[0].decode() == e]
    print(f"E={e}: G-record occurrences={len(hits)}")
    for i in hits:
        L = wt[i]
        nxt = wt[i+1] if i+1 < len(wt) else b""
        print(f"   line {i+1}: len={len(L)} col77={L[76:77]!r} col78={L[77:78]!r} col80={L[79:80]!r} energy_field={L[9:19]!r}")
        print(f"      NEXT: {nxt.decode('ascii','replace')!r}")

print("\n=== ITEM 2b: residual 'E,RI$from {+31}P' or 'RI$from {+31}P(|a,p|g).' ===")
for i, L in enumerate(wt):
    s = L.decode("ascii", "replace")
    if "E,RI$from {+31}P" in s or "RI$from {+31}P(|a,p|g)." in s:
        print(f"  L{i+1}: {s!r}")
print("  (none printed above = clean)")
