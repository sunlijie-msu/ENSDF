"""Read-only: print context around given line numbers of the adopted file."""
import sys

PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"


def main():
    targets = [int(a) for a in sys.argv[1:]]
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for t in targets:
        print("===== around line", t, "=====")
        for i in range(max(0, t - 5), min(len(lines), t + 3)):
            print(i + 1, repr(lines[i].rstrip()))
        print()


if __name__ == "__main__":
    main()
