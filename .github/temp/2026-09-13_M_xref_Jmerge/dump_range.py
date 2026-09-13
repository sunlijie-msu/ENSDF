"""Read-only range dumper: prints line no, length, repr for a range of the adopted file."""
import sys

PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"


def main():
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for i in range(start - 1, min(end, len(lines))):
        flag = "" if len(lines[i]) == 80 else "   <<< NOT-80"
        print(i + 1, len(lines[i]), repr(lines[i]) + flag)


if __name__ == "__main__":
    main()
