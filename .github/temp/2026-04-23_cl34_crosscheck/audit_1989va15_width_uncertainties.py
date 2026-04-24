from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import random
import re

SOURCE = Path(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_p_resonances.ens")
SPOTCHECK_SEED = 34023
TIME_RE = re.compile(r"^([0-9]+(?:\.[0-9]+)?)\s*([A-Z]+)$")


@dataclass
class Level:
    line: int
    energy_text: str
    energy: Decimal | None
    j: str
    t_text: str
    dt_text: str
    comments: list[tuple[int, str]]


def parse_energy(text: str) -> Decimal | None:
    text = text.strip()
    if not text:
        return None
    try:
        return Decimal(text)
    except Exception:
        return None


def is_l_record(line: str) -> bool:
    return len(line) >= 9 and line[5] == " " and line[6] == " " and line[7] == "L" and line[8] == " "


def parse_levels() -> list[Level]:
    levels: list[Level] = []
    current: Level | None = None
    for idx, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1):
        if is_l_record(line):
            current = Level(
                line=idx,
                energy_text=line[9:19].strip(),
                energy=parse_energy(line[9:19]),
                j=line[22:39].rstrip(),
                t_text=line[39:49].rstrip(),
                dt_text=line[49:55].strip(),
                comments=[],
            )
            levels.append(current)
            continue
        if current is None:
            continue
        if len(line) >= 8 and line[6] == "c" and line[7] == "L":
            current.comments.append((idx, line.rstrip()))
    return levels


def uses_1977da03_t(level: Level) -> bool:
    for _, line in level.comments:
        if "E,J,T,S$from 1977Da03" in line:
            return True
        if "T$" in line and "1977Da03" in line:
            return True
    return False


def parse_t(level: Level):
    match = TIME_RE.match(level.t_text.strip())
    if not match:
        return None
    value_text, unit = match.groups()
    decimals = len(value_text.split(".")[1]) if "." in value_text else 0
    return {
        "value_text": value_text,
        "value": Decimal(value_text),
        "unit": unit,
        "decimals": decimals,
        "dt": int(level.dt_text),
    }


def round_unc_digit(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def round_4_up_to_int(value: Decimal) -> int:
    integer = int(value)
    fraction = value - Decimal(integer)
    return integer + 1 if fraction >= Decimal("0.4") else integer


def relative_fraction(info: dict) -> Decimal:
    if info["unit"] == "KEV" and info["value"] >= Decimal("10"):
        return Decimal("0.20")
    return Decimal("0.10")


def expected_for_decimals(expected_abs: Decimal, decimals: int) -> int:
    scale = Decimal(10) ** decimals
    return round_unc_digit(expected_abs * scale)


def represented_abs(dt: int, decimals: int) -> Decimal:
    return Decimal(dt) / (Decimal(10) ** decimals)


def strict_uncertainty_model(expected_abs: Decimal) -> dict:
    adjusted = expected_abs.adjusted()
    scaled_for_leading = expected_abs.scaleb(-adjusted)
    leading_two = int((scaled_for_leading * Decimal(10)).to_integral_value(rounding=ROUND_HALF_UP))
    sigfigs = 2 if 10 <= leading_two <= 34 else 1
    scale_exp = sigfigs - 1 - adjusted
    scaled = expected_abs.scaleb(scale_exp)
    rounded_digits = round_4_up_to_int(scaled)
    rounded_unc = Decimal(rounded_digits).scaleb(-scale_exp)
    decimals_needed = max(0, scale_exp)
    return {
        "leading_two": leading_two,
        "sigfigs": sigfigs,
        "rounded_digits": rounded_digits,
        "rounded_unc": rounded_unc,
        "decimals_needed": decimals_needed,
    }


def recommended_value_text(value: Decimal, decimals: int) -> str:
    quantum = Decimal("1") if decimals == 0 else Decimal("1." + ("0" * decimals))
    rounded = value.quantize(quantum)
    text = format(rounded, "f")
    if decimals == 0:
        return text.split(".")[0]
    whole, frac = text.split(".")
    return f"{whole}.{frac.ljust(decimals, '0')}"


def classify(level: Level) -> dict | None:
    if not level.t_text.strip() or not level.dt_text.strip():
        return None
    if uses_1977da03_t(level):
        return None
    info = parse_t(level)
    if info is None:
        return None

    rel = relative_fraction(info)
    expected_abs = info["value"] * rel
    actual_abs = represented_abs(info["dt"], info["decimals"])
    strict = strict_uncertainty_model(expected_abs)
    ideal_dt = strict["rounded_digits"]
    ideal_decimals = strict["decimals_needed"]
    ideal_value_text = recommended_value_text(info["value"], ideal_decimals)

    if info["dt"] == ideal_dt and info["decimals"] == ideal_decimals and info["value_text"] == ideal_value_text:
        return None

    trailing_match = None
    for extra in range(1, 5):
        test_decimals = info["decimals"] + extra
        if ideal_dt == info["dt"] and test_decimals == ideal_decimals:
            trailing_match = test_decimals
            break

    strong_trailing_zero_issue = (
        trailing_match is not None
        and actual_abs == expected_abs * Decimal(10)
    )

    return {
        "line": level.line,
        "energy": level.energy_text,
        "j": level.j.strip(),
        "current_t": level.t_text,
        "current_dt": level.dt_text,
        "unit": info["unit"],
        "value": str(info["value"]),
        "decimals": info["decimals"],
        "rule": "20%" if rel == Decimal("0.20") else "10%",
        "expected_abs": str(expected_abs.normalize()),
        "actual_abs": str(actual_abs.normalize()),
        "leading_two": strict["leading_two"],
        "sigfigs": strict["sigfigs"],
        "ideal_dt": str(ideal_dt),
        "ideal_decimals": ideal_decimals,
        "classification": "trailing_zeros_needed" if trailing_match is not None else "strict_rounding_mismatch",
        "strong_issue": strong_trailing_zero_issue,
        "recommended_decimals": trailing_match,
        "recommended_value_text": ideal_value_text,
        "recommended_dt": str(ideal_dt),
        "comments": [line for _, line in level.comments if "T$" in line or "E,J,T,S$" in line],
    }


def main() -> None:
    levels = parse_levels()
    candidates = []
    mismatches = []
    for level in levels:
        if not level.t_text.strip() or not level.dt_text.strip():
            continue
        if uses_1977da03_t(level):
            continue
        info = parse_t(level)
        if info is None:
            continue
        candidates.append(level)
        item = classify(level)
        if item is not None:
            mismatches.append(item)

    indexed = []
    total = len(candidates)
    for idx, level in enumerate(candidates, 1):
        reverse_idx = total - idx + 1
        indexed.append((idx, reverse_idx, level))

    mismatch_lookup = {item["line"]: item for item in mismatches}

    print("SUMMARY")
    print({
        "candidate_count": total,
        "strict_mismatch_count": len(mismatches),
        "trailing_zeros_needed": sum(item["classification"] == "trailing_zeros_needed" for item in mismatches),
        "strict_rounding_mismatch": sum(item["classification"] == "strict_rounding_mismatch" for item in mismatches),
        "strong_trailing_zero_issues": sum(item["strong_issue"] for item in mismatches),
        "excluded_1977Da03_levels": sum(1 for level in levels if level.t_text.strip() and uses_1977da03_t(level)),
        "assumption": "10% for widths <10 keV or any eV value; 20% for widths >=10 keV",
    })
    print("MISMATCHES")
    for forward_idx, reverse_idx, level in indexed:
        item = mismatch_lookup.get(level.line)
        if item is None:
            continue
        row = dict(item)
        row["forward_index"] = forward_idx
        row["reverse_index"] = reverse_idx
        print(row)

    sample_size = max(10, -(-total * 15 // 100))
    random.seed(SPOTCHECK_SEED)
    sample = random.sample(indexed, sample_size)
    print("SPOTCHECK")
    print({"sample_size": sample_size, "seed": SPOTCHECK_SEED})
    failures = []
    for sample_idx, (forward_idx, reverse_idx, level) in enumerate(sample, 1):
        info = parse_t(level)
        if info is None:
            failures.append({"sample": sample_idx, "line": level.line, "reason": "parse_failed"})
            continue
        result = {
            "sample": sample_idx,
            "line": level.line,
            "forward_index": forward_idx,
            "reverse_index": reverse_idx,
            "energy": level.energy_text,
            "t": level.t_text,
            "dt": level.dt_text,
            "excluded_1977Da03": uses_1977da03_t(level),
            "classification": mismatch_lookup.get(level.line, {}).get("classification", "ok"),
        }
        print(result)
    print({"spotcheck_failures": len(failures)})


if __name__ == "__main__":
    main()
