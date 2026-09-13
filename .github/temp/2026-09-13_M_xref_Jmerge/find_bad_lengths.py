"""Read-only: report any line whose length is not 80 characters."""
import sys

PATH = r"D:/X/ND/ENSDF/A34/S34/new/S34_adopted.ens"


def main():
    with open(PATH, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.split("\n")
    bad = 0
    for i, line in enumerate(lines):
        if len(line) != 80 and not (i == len(lines) - 1 and line == ""):
            bad += 1
            print(i + 1, len(line), repr(line.rstrip()))
    print("BAD_LINES", bad, "TOTAL", len(lines))


if __name__ == "__main__":
    sys.exit(main())
