"""Wrap formatted 1994Pe08 method text into ENSDF comment continuation lines."""
TEXT = ("Magnetic (M) character established because longitudinal electric "
        "contributions vanish at 180|' back-scattering, confirmed by agreement of "
        "forward-angle measurements at matched momentum transfer q with the 180|' "
        "data. M1 versus M2 assignments from least-squares fits of the reduced "
        "transition probability B(M|L,q) versus q{+2} for |L=1 and 2, selecting "
        "the multipolarity that produced both a linear low-q dependence and a "
        "physically reasonable transition radius R{-tr} near the ground-state rms "
        "charge radius.")

LABELS = ["8", "9", "A", "B", "C", "D", "E", "F"]
WIDTH = 71  # text columns 10-80

words = TEXT.split(" ")
lines = []
cur = ""
for w in words:
    cand = w if not cur else cur + " " + w
    if len(cand) <= WIDTH:
        cur = cand
    else:
        lines.append(cur)
        cur = w
if cur:
    lines.append(cur)

print("text chars:", len(TEXT), " lines:", len(lines))
for label, body in zip(LABELS, lines):
    full = " 34S " + label + "c  " + body
    padded = full.ljust(80)
    ok = (len(full) <= 80 and all(ord(ch) < 128 for ch in padded))
    print(f"{label}: content={len(full):3d} pad={len(padded):3d} {ok} |{padded}|")
if len(lines) > len(LABELS):
    print("!! more lines than labels")
# reassembled text sanity check
rebuilt = " ".join(" ".join(line.split()) for line in lines)
print("roundtrip equal:", rebuilt == TEXT)
