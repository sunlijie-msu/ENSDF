"""Read-only: content lengths and text for all lines involved in the WIDTHG0 conversion."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

NEEDED = {
    "7781.22": [691, 692, 693, 694, 695, 696, 697],
    "8185.46": [763, 764, 765, 766, 767],
    "8385.41": [808, 809, 810, 811, 812, 813, 814, 815, 816],
    "8506.77": [837, 838, 839, 840, 841, 842, 843, 844],
    "9640": [1017, 1018, 1019, 1020, 1021],
    "9707": [1028, 1029, 1030, 1031, 1032, 1033, 1034],
    "9868": [1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058],
    "10170": [1123, 1124, 1125, 1126, 1127, 1128],
    "10790": [1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298],
    "10803": [1310, 1311, 1312, 1313, 1314],
    "11024.95": [1357, 1358, 1359],
}

for tag, nums in NEEDED.items():
    print(f"\n--- {tag} ---")
    for n in nums:
        s = lines[n - 1]
        c = s.rstrip()
        print(f"{n:5d} len={len(s):3d} clen={len(c):3d} pad={len(s) - len(c):3d}")
        print(f"      {c!r}")
