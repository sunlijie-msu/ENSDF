import sys
from pathlib import Path

# ENSDF fixed columns (1-based indexing in docs; convert to 0-based here)
E_START = 9   # column 10
E_END = 19    # inclusive, so slice end index is 19 (0-based exclusive: 19)
DE_START = 19 # columns 20-21
DE_END = 21   # exclusive
LINE_LEN = 80

PREFIXES = (" L ", " G ")  # record type markers at col 8


def round_energy_field(line: str) -> str:
    # Ensure line length at least LINE_LEN (pad if short)
    if len(line) < LINE_LEN:
        line = line.rstrip("\n")
        line = line + " " * (LINE_LEN - len(line))
    else:
        line = line[:LINE_LEN]

    # Check record type
    # NUCID is cols 1-5; TYPE at col 8 should be 'L' or 'G'
    if not (len(line) >= 9 and line[7] in ("L", "G")):
        return line

    # Extract energy field
    e_field = line[E_START:E_END]
    e_str = e_field.strip()
    if not e_str:
        return line

    # Parse as float if possible
    try:
        e_val = float(e_str)
    except ValueError:
        # If cannot parse, leave unchanged
        return line

    # Round to nearest integer
    e_int = int(round(e_val))
    new_e = str(e_int)
    # Left-justify within E field width
    e_width = E_END - E_START
    new_e_field = new_e.ljust(e_width)

    # Blank out DE field (columns 20-21)
    de_width = DE_END - DE_START
    new_de_field = " " * de_width

    # Reconstruct line
    new_line = (
        line[:E_START] + new_e_field + line[E_END:DE_START] + new_de_field + line[DE_END:]
    )

    # Ensure exact 80 chars
    if len(new_line) < LINE_LEN:
        new_line = new_line + " " * (LINE_LEN - len(new_line))
    else:
        new_line = new_line[:LINE_LEN]

    return new_line


def process_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        # Only modify data records that are L or G
        if len(line) >= 8 and line[7] in ("L", "G"):
            new_lines.append(round_energy_field(line))
        else:
            # Preserve non-data records (comments, headers) unchanged
            # Do not enforce 80 cols for comments
            new_lines.append(line)
    path.write_text("\n".join(new_lines) + ("\n" if lines and lines[-1].endswith("\n") else ""), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 2026-01-18_edit_energy_fields.py <file.ens>")
        sys.exit(1)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"ERROR: File not found: {target}")
        sys.exit(1)
    process_file(target)
    print(f"Updated energy fields (rounded) and blanked DE in: {target}")
