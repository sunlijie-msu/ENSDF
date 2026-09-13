"""For each target vague T$ line, find the minimal number of following lines needed for a unique anchor."""
PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"
TARGETS = [384, 462, 476, 525, 547, 566, 602, 635, 728, 902]


def main():
    with open(PATH, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.split("\n")
    for t in TARGETS:
        base = t - 1
        for k in range(1, 5):
            block = "\n".join(lines[base:base + k])
            n = text.count(block)
            print("target %4d  k=%d  occurrences=%d  last=%r" % (t, k, n, lines[base + k - 1].rstrip()[:60]))
        print()


if __name__ == "__main__":
    main()
