"""Read-only: list lines matching a regex with line no, length, content length (pad = trailing spaces)."""
import re
import sys

PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"


def main():
    pat = sys.argv[1]
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    rx = re.compile(pat)
    for i in range(lo - 1, min(hi, len(lines))):
        if rx.search(lines[i]):
            print(i + 1, "len=%d" % len(lines[i]), "pad=%d" % (len(lines[i]) - len(lines[i].rstrip())), repr(lines[i].rstrip()))


if __name__ == "__main__":
    main()
