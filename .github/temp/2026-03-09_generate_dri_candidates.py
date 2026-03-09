from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import os
import subprocess
import sys

FILE = Path(r"d:\X\ND\ENSDF\A34\Cl34\raw\1977DA02.ens")
START_MARKER = " 34CL  L 6134"
OUTPUT_BLOCK = Path(r"d:\X\ND\ENSDF\.github\temp\2026-03-09_unbound_block_with_dri.txt")


def round_half_up_decimal(value: Decimal, quantum: str) -> Decimal:
    return value.quantize(Decimal(quantum), rounding=ROUND_HALF_UP)


def encode_uncertainty(ri_text: str):
    ri = Decimal(ri_text)

    # Revised rule from user:
    # - RI <= 5 : about 50%
    # - RI > 5  : about 10%
    # - Integer RI values should use one decimal place so DRI can encode tenths.
    if "." not in ri_text:
        ri_text = f"{int(ri)}.0"

    uncertainty = ri * (Decimal("0.5") if ri <= Decimal("5") else Decimal("0.1"))

    decimals = len(ri_text.split(".")[1]) if "." in ri_text else 0
    quantum = "1" if decimals == 0 else "0." + ("0" * (decimals - 1)) + "1"
    dri_value = round_half_up_decimal(uncertainty, quantum)
    scale = 10 ** decimals
    dri_digits = int((dri_value * scale).to_integral_value(rounding=ROUND_HALF_UP))
    return ri_text, str(dri_digits)


def replace_dri(line: str):
    line = line.rstrip("\n")
    if not line.startswith(" "):
        line = " " + line
    ri_field = line[22:29]
    dri_field = line[29:31]
    ri_text = ri_field.strip()
    dri_text = dri_field.strip()

    if not ri_text:
        return None
    if dri_text in {"LT", "GT"}:
        return None

    new_ri, new_dri = encode_uncertainty(ri_text)
    new_line = line[:22] + new_ri.ljust(7) + new_dri.ljust(2) + line[31:]
    return new_line


def main():
    lines = FILE.read_text().splitlines()
    in_block = False
    changed = []
    block_lines = []

    for idx, line in enumerate(lines, start=1):
        normalized_line = line if line.startswith(" ") else " " + line
        if normalized_line.startswith(START_MARKER):
            in_block = True
            block_lines.append(normalized_line)
            continue
        if not in_block:
            continue
        if len(normalized_line) > 7 and normalized_line[7] == "L":
            block_lines.append(normalized_line)
        if len(normalized_line) > 7 and normalized_line[7] == "G":
            candidate = replace_dri(normalized_line)
            if candidate and candidate != normalized_line:
                changed.append((idx, normalized_line, candidate))
                block_lines.append(candidate)
            else:
                block_lines.append(normalized_line)

    print(f"CHANGED_LINES={len(changed)}")
    for idx, old, new in changed:
        print(f"LINE={idx}\nOLD={old}\nNEW={new}")

    failures = []
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    for idx, _, new in changed:
        result = subprocess.run(
            [sys.executable, ".github/scripts/ensdf_1line_ruler.py", "--line", new],
            capture_output=True,
            text=True,
            cwd=FILE.parents[3],
            env=env,
        )
        if result.returncode != 0:
            failures.append((idx, new, result.stdout, result.stderr))

    OUTPUT_BLOCK.write_text("\n".join(block_lines) + "\n")
    print(f"OUTPUT_BLOCK={OUTPUT_BLOCK}")
    print(f"RULER_FAILURES={len(failures)}")
    for idx, new, stdout, stderr in failures:
        print(f"FAIL_LINE={idx}\n{new}\nSTDOUT={stdout}\nSTDERR={stderr}")


if __name__ == "__main__":
    main()
