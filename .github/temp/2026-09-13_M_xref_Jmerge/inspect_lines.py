"""Read-only inspector: dump exact line length + repr for adopted-file regions to be edited."""
import sys

PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"

RANGES = [
    (98, 106),    # 3304.212 level
    (126, 134),   # 3916.407 level
    (140, 152),   # 4074.666 level
    (162, 170),   # 4114.81 level
    (182, 189),   # 4624.404 level
    (203, 209),   # 4688.97 level
    (217, 224),   # 4876.842 level
    (238, 246),   # 4889.76 level
    (252, 266),   # 5228.175 / 5318.8 / 5322.514
    (274, 280),   # 5380.99 level
    (286, 291),   # 5679.928 level
    (306, 316),   # 5690.8 level
]

def main():
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    seen = set()
    for start, end in RANGES:
        for i in range(start, end):
            if i in seen:
                continue
            seen.add(i)
            print(i + 1, len(lines[i]), repr(lines[i]))
    print("TOTAL_LINES", len(lines))

if __name__ == "__main__":
    sys.exit(main())
