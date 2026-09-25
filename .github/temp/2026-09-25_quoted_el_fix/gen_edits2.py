"""Generate unique, non-overlapping, byte-exact edit strings for every stale quoted level energy.

Read-only: prints proposed oldString/newString pairs (python repr) for manual application.
"""
import io
import os

PAIRS = [
    ("2127.558", "2127.561"),
    ("3304.207", "3304.210"),
    ("4074.657", "4074.662"),
    ("4624.401", "4624.404"),
    ("4876.839", "4876.842"),
    ("5690.61", "5690.62"),
    ("5755.871", "5755.873"),
    ("5847.517", "5847.521"),
    ("6251.72", "6251.73"),
    ("6342.51", "6342.52"),
    ("6478.765", "6478.768"),
    ("7110.447", "7110.450"),
    ("7629.903", "7629.906"),
    ("5679.925", "5679.928"),
]
FILES = [
    r"A34\S34\new\S34_adopted.ens",
    r"A34\S34\new\S34_30si_a_g_a_n_resonances.ens",
    r"A34\S34\new\S34_28si_34s_34sPg.ens",
    r"A34\S34\new\S34_206pb_34s_34sPg.ens",
    r"A34\S34\new\S34_208pb_34s_34sP.ens",
]


def find_occ(text):
    occ = []
    for old, new in PAIRS:
        pos = 0
        while True:
            k = text.find(old, pos)
            if k < 0:
                break
            if k and text[k - 1].isdigit():
                pos = k + 1
                continue
            if k + len(old) < len(text) and text[k + len(old)].isdigit():
                pos = k + 1
                continue
            occ.append((k, len(old), old, new))
            pos = k + 1
    occ.sort()
    return occ


def window(text, k, ln, prev_end, next_start):
    """Unique window for token at k (length ln), kept away from neighbouring tokens."""
    for pad in (10, 14, 20, 26, 30):
        s = max(0, k - pad, prev_end)
        e = min(len(text), k + ln + pad, next_start)
        if text.count(text[s:e]) == 1:
            break
    else:
        # fall back to the whole line (plus following line if needed)
        ls = text.rfind("\n", 0, k) + 1
        le = text.find("\n", k + ln)
        if le < 0:
            le = len(text)
        if text.count(text[ls:le]) == 1:
            s, e = ls, le
        else:
            nl = text.find("\n", le + 1)
            if nl < 0:
                nl = len(text)
            if text.count(text[ls:nl]) == 1:
                s, e = ls, nl
            else:
                raise RuntimeError("no unique window")
    # trim trailing spaces (avoids transcribing padding) while uniqueness holds
    while e > k + ln and text[e - 1] == " " and text.count(text[s:e - 1]) == 1:
        e -= 1
    # trim leading spaces after the previous boundary
    while s < k and (text[s] == " " or text[s] == "\n") and text.count(text[s + 1:e]) == 1:
        s += 1
    return s, e


for rel in FILES:
    with io.open(rel, newline="") as fh:
        text = fh.read().replace("\r\n", "\n")
    occ = find_occ(text)
    if not occ:
        continue
    print("### %s   (%d edits)" % (os.path.basename(rel), len(occ)))
    for i, (k, ln, old, new) in enumerate(occ):
        prev_end = occ[i - 1][0] + occ[i - 1][1] if i else 0
        next_start = occ[i + 1][0] if i + 1 < len(occ) else len(text)
        s, e = window(text, k, ln, prev_end, next_start)
        seg = text[s:e]
        assert seg.count(old) == 1
        print("  # line %d : %s -> %s" % (text[:k].count("\n") + 1, old, new))
        print("  O: %r" % seg)
        print("  N: %r" % seg.replace(old, new, 1))
    print()
