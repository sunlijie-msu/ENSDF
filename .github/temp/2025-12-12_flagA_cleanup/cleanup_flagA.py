from __future__ import annotations

import argparse
from pathlib import Path


def is_flag_a_line(line80: str) -> bool:
    # NUCID cols 1-5, continuation col 6, blank col 7, record type col 8
    return (
        len(line80) == 80
        and line80[5] == "F"
        and line80[7] == "L"
        and "FLAG=A" in line80
    )


def is_level_record(line80: str) -> bool:
    # True L-record: continuation label (col 6), blank (col 7), type 'L' (col 8), blank (col 9)
    # This excludes cL comment lines where col 7 is 'c' and col 8 is 'L'.
    return (
        len(line80) == 80
        and line80[6] == " "
        and line80[7] == "L"
        and line80[8] == " "
        and bool(line80[9:19].strip())
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Delete 'F L FLAG=A' marker lines and clear DE (cols 20-21) on unflagged L-records."
        )
    )
    ap.add_argument("file", type=Path, help="Path to .ens file (edited in place)")
    args = ap.parse_args()

    path: Path = args.file
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        raw = f.read()
    lines = raw.splitlines(True)

    out: list[str] = []
    flag_next = False
    removed_flag_lines = 0
    cleared_de = 0
    cleared_examples: list[tuple[int, str]] = []

    for idx, s in enumerate(lines, start=1):
        base = s.rstrip("\r\n")
        nl = s[len(base) :]

        # Delete FLAG lines; treat as applying to the immediately following L-record
        if is_flag_a_line(base):
            removed_flag_lines += 1
            flag_next = True
            continue

        if is_level_record(base):
            if flag_next:
                flag_next = False
            else:
                # Clear DE field cols 20-21 (1-based). Zero-based slice [19:21].
                if base[19:21].strip():
                    base = base[:19] + "  " + base[21:]
                    cleared_de += 1
                    cleared_examples.append((idx, base[9:19].rstrip()))

        out.append(base + nl)

    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("".join(out))

    print(f"Removed FLAG=A lines: {removed_flag_lines}")
    print(f"Cleared DE on L-records: {cleared_de}")
    if cleared_examples:
        show = cleared_examples[:10]
        suffix = "" if len(cleared_examples) <= 10 else f" (+{len(cleared_examples) - 10} more)"
        print("Examples (line, E field):")
        for ln, efield in show:
            print(f"  {ln:>4d}  {efield}")
        if suffix:
            print(suffix)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
