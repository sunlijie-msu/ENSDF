"""Generate unique, byte-exact oldString/newString pairs for every stale quoted level energy.

Read-only: prints proposed edit strings (printer form) for manual application.
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


def uniq_window(text, start, end, kind="expand"):
    """Return a (s, e) window around text[start:end] that occurs exactly once in text."""
    for pad in (12, 20, 30, 45, 60, 80, 120, 200):
        s = max(0, start - pad)
        e = min(len(text), end + pad)
        if text.count(text[s:e]) == 1:
            return s, e
    raise RuntimeError("cannot make unique window")


for rel in FILES:
    with io.open(rel, newline="") as fh:
        raw = fh.read()
    text = raw.replace("\r\n", "\n")
    items = []
    for old, new in PAIRS:
        pos = 0
        while True:
            k = text.find(old, pos)
            if k < 0:
                break
            if k >= 1 and text[k - 1].isdigit():
                pos = k + 1
                continue
            if k + len(old) < len(text) and text[k + len(old)].isdigit():
                pos = k + 1
                continue
            items.append((k, old, new))
            pos = k + 1
    if not items:
        continue
    print("### %s  (%d edits)" % (os.path.basename(rel), len(items)))
    for k, old, new in items:
        s, e = uniq_window(text, k, k + len(old))
        seg = text[s:e]
        assert seg.count(old) == 1, (rel, old, k)
        ln = text[:k].count("\n") + 1
        print("  # line %d  %s -> %s" % (ln, old, new))
        print("  O: %r" % seg)
        print("  N: %r" % seg.replace(old, new, 1))
    print()
