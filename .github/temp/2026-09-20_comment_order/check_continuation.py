"""Check comment-unit integrity: within each cL/cG unit the column-6 continuation
markers must ascend from blank (first line) through 2, 3, 4... (letters allowed after
digits, e.g. "B").  A unit that starts at 3cL after a reorder means the unit was split.
"""
import sys

KINDS = {"L": "cL", "G": "cG"}


def main(path):
    units = []
    cur = None
    for n, raw in enumerate(open(path, encoding="ascii", errors="ignore"), 1):
        line = raw.rstrip("\r\n").rstrip()
        if len(line) > 7 and line[6] in "cd" and line[7] in "LG":
            mark = line[5] if len(line) > 5 else " "
            body = line[8:]
            starts = mark in (" ", "", "0") and "$" in body[:45]
            if starts or cur is None or cur["kind"] != line[7] or cur["last"] + 1 != n:
                if cur:
                    units.append(cur)
                cur = {"kind": line[7], "start": n, "last": n, "marks": [mark], "text": [line]}
            else:
                cur["last"] = n
                cur["marks"].append(mark)
                cur["text"].append(line)
        else:
            if cur:
                units.append(cur)
                cur = None
    if cur:
        units.append(cur)
    bad = 0
    for u in units:
        digits = [m for m in u["marks"][1:] if m.isdigit()]
        if digits and digits != [str(i) for i in range(2, 2 + len(digits))]:
            bad += 1
            print("[X]", u["kind"], "line", u["start"], u["marks"])
            for t in u["text"]:
                print("    ", repr(t[:78]))
        elif not digits and len(u["marks"]) > 1:
            # multi-line unit without digit continuations: letters are legitimate
            pass
    print("units checked:", len(units), "| broken continuation sequences:", bad)


if __name__ == "__main__":
    main(sys.argv[1])
