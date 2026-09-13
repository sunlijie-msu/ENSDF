"""Print target vague T$ lines and the next 3 lines with exact pads, to build unique anchors."""
PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"

TARGETS = [384, 462, 476, 525, 547, 566, 602, 635, 728, 902]


def main():
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for t in TARGETS:
        print("===== target line", t, "=====")
        for i in range(t - 1, min(len(lines), t + 3)):
            ln = lines[i]
            print("  %d len=%d pad=%d %s" % (i + 1, len(ln), len(ln) - len(ln.rstrip()), repr(ln.rstrip())))
        print()


if __name__ == "__main__":
    main()
