"""Verify flag column for all B1 lines + count remaining targets."""
raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
check = ["8979", "7837", "9013", "11140", "7860", "9036", "11163", "7915", "9091",
         "11218", "7928", "9104", "11231", "9143", "8010", "9186", "11313", "8018",
         "9194", "11321"]
bad = 0
for g in check:
    hit = None
    for ln in lines:
        if ln.startswith(" 34S   G " + g + " "):
            hit = ln
            break
    if hit is None:
        print("MISSING", g); bad += 1; continue
    ok = len(hit) == 80 and hit[76] == "A"
    if not ok:
        bad += 1
    print(("OK  " if ok else "BAD ") + f"G {g}: len={len(hit)} col77={hit[76]!r}")
print("bad:", bad)
