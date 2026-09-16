"""Final structural check of the WIDTHG0 -> cL comment conversion."""
from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()

LEV = {
    "7781.22": "0.57",
    "8185.46": "0.78",
    "8385.41": "0.49",
    "8506.77": "0.52",
    "9640": "3.6",
    "9707": "0.50",
    "9868": "0.60",
    "10170": "1.06",
    "10790": "0.75",
    "10803": "0.60",
}

for lev, val in LEV.items():
    for i, s in enumerate(L, 1):
        if s[7:8] == "L" and s[9:19].strip() == lev:
            # inspect the block up to the first G/F/S record
            blk = []
            j = i + 1
            while j <= len(L) and len(L[j - 1]) > 7 and L[j - 1][7:8] not in ("G", "F", "S"):
                blk.append((j, L[j - 1]))
                j += 1
            has = any(f"|G{{-|g0}}={val}" in t for _, t in blk)
            print(f"{lev:9s} L-line {i:5d} len={len(s):3d} T={s[39:49]!r} DT={s[49:55]!r} comment={has} blocklines={len(blk)}")
            break

print("\nWIDTHG0 remaining:", [i for i, s in enumerate(L, 1) if "WIDTHG0" in s])
print("WIDTHG=3 EV kept:", any("WIDTHG=3 EV" in s for s in L))
print("total lines:", len(L))
