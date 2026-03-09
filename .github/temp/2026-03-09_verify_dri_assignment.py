from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import random
import math

FILE = Path(r"d:\X\ND\ENSDF\A34\Cl34\raw\1977DA02.ens")
START_MARKER = " 34CL  L 6134"
SEED = 20260309


def round_half_up_decimal(value: Decimal, quantum: str) -> Decimal:
    return value.quantize(Decimal(quantum), rounding=ROUND_HALF_UP)


def expected_values(ri_text: str, dri_text: str):
    if dri_text in {"LT", "GT"}:
        return ri_text, dri_text

    ri = Decimal(ri_text)
    if "." not in ri_text:
        ri_text = f"{int(ri)}.0"

    uncertainty = ri * (Decimal("0.5") if ri <= Decimal("5") else Decimal("0.1"))
    decimals = len(ri_text.split(".")[1]) if "." in ri_text else 0
    quantum = "1" if decimals == 0 else "0." + ("0" * (decimals - 1)) + "1"
    dri_value = round_half_up_decimal(uncertainty, quantum)
    scale = 10 ** decimals
    dri_digits = int((dri_value * scale).to_integral_value(rounding=ROUND_HALF_UP))
    return ri_text, str(dri_digits)


def main():
    lines = FILE.read_text().splitlines()
    in_block = False
    records = []
    current_level = None

    for idx, line in enumerate(lines, start=1):
        normalized_line = line if line.startswith(" ") else " " + line
        if normalized_line.startswith(START_MARKER):
            in_block = True
        if not in_block:
            continue
        if len(normalized_line) > 7 and normalized_line[7] == "L":
            current_level = normalized_line[9:19].strip()
            continue
        if len(normalized_line) > 7 and normalized_line[7] == "G":
            ri_text = normalized_line[22:29].strip()
            dri_text = normalized_line[29:31].strip()
            if not ri_text:
                continue
            exp_ri, exp_dri = expected_values(ri_text, dri_text)
            records.append({
                "line": idx,
                "level": current_level,
                "eg": normalized_line[9:19].strip(),
                "ri": ri_text,
                "dri": dri_text,
                "exp_ri": exp_ri,
                "exp_dri": exp_dri,
                "pass": ri_text == exp_ri and dri_text == exp_dri,
            })

    checked = [record for record in records if record["dri"] not in {"LT", "GT"}]
    failures = [record for record in checked if not record["pass"]]

    print(f"TOTAL_CHECKED={len(checked)}")
    print(f"FAILURES={len(failures)}")

    if not checked:
        print("SAMPLE_SIZE=0")
        return

    sample_size = min(len(checked), max(5, math.ceil(0.05 * len(checked))))
    random.seed(SEED)
    sample = random.sample(checked, sample_size)
    print(f"SEED={SEED}")
    print(f"SAMPLE_SIZE={sample_size}")
    for record in sorted(sample, key=lambda item: item["line"]):
        print(
            f"SAMPLE line={record['line']} Ei={record['level']} Eg={record['eg']} "
            f"RI={record['ri']} DRI={record['dri']} EXPECTED_RI={record['exp_ri']} EXPECTED_DRI={record['exp_dri']} PASS={record['pass']}"
        )

    if failures:
        for record in failures[:20]:
            print(
                f"FAIL line={record['line']} Ei={record['level']} Eg={record['eg']} "
                f"RI={record['ri']} DRI={record['dri']} EXPECTED_RI={record['exp_ri']} EXPECTED_DRI={record['exp_dri']}"
            )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
