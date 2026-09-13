"""Print given line numbers +/-2 with exact pads (read-only)."""
import sys

PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"


def main():
    targets = [int(a) for a in sys.argv[1:]]
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for t in targets:
        print("===== around", t, "=====")
        for i in range(max(0, t - 3), min(len(lines), t + 2)):
            ln = lines[i]
            print("  %d len=%d pad=%d %s" % (i + 1, len(ln), len(ln) - len(ln.rstrip()), repr(ln.rstrip())))
        print()


if __name__ == "__main__":
    main()
