from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import re
import sys

SOURCE = Path(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_p_resonances.ens")
TARGET = Path(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens")
ENERGY_MIN = Decimal("6321.2")
TIME_RE = re.compile(r"^([0-9]+(?:\.[0-9]+)?)\s*([A-Z]+)$")


@dataclass
class Level:
    line: int
    energy_text: str
    energy: Decimal | None
    de: str
    j: str
    t_text: str
    dt_text: str
    raw: str
    xref: str | None
    comments: list[tuple[int, str]]


@dataclass
class WidthFix:
    line: int
    energy_text: str
    old_line: str
    new_line: str
    old_t: str
    old_dt: str
    new_t: str
    new_dt: str
    rule: str


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


def parse_levels(path: Path, require_xref_with_l: bool = False) -> list[Level]:
    levels: list[Level] = []
    current: Level | None = None
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if is_l_record(line):
            current = Level(
                line=idx,
                energy_text=line[9:19].strip(),
                energy=parse_energy(line[9:19]),
                de=line[19:21].strip(),
                j=line[22:39].rstrip(),
                t_text=line[39:49].rstrip(),
                dt_text=line[49:55].rstrip(),
                raw=line,
                xref=None,
                comments=[],
            )
            levels.append(current)
            continue
        if current is None:
            continue
        if len(line) >= 9 and line[5] == "X" and line[6] == " " and line[7] == "L" and line[8] == " ":
            current.xref = line[9:].rstrip()
        elif len(line) >= 8 and line[6] == "c" and line[7] == "L":
            current.comments.append((idx, line.rstrip()))
    scoped: list[Level] = []
    for level in levels:
        if level.energy is None or level.energy < ENERGY_MIN:
            continue
        if require_xref_with_l and (level.xref is None or "L" not in level.xref):
            continue
        scoped.append(level)
    return scoped


def uses_1977da03_t(level: Level) -> bool:
    for _, line in level.comments:
        if "E,J,T,S$from 1977Da03" in line:
            return True
        if "T$" in line and "1977Da03" in line:
            return True
    return False


def parse_t_fields(level: Level):
    match = TIME_RE.match(level.t_text.strip())
    if not match or not level.dt_text.strip():
        return None
    value_text, unit = match.groups()
    decimals = len(value_text.split(".")[1]) if "." in value_text else 0
    return {
        "value_text": value_text,
        "value": Decimal(value_text),
        "unit": unit,
        "decimals": decimals,
        "dt": level.dt_text.strip(),
    }


def round_4_up_to_int(value: Decimal) -> int:
    integer = int(value)
    fraction = value - Decimal(integer)
    return integer + 1 if fraction >= Decimal("0.4") else integer


def relative_fraction(value: Decimal, unit: str) -> Decimal:
    if unit == "KEV" and value >= Decimal("10"):
        return Decimal("0.20")
    return Decimal("0.10")


def strict_uncertainty_model(expected_abs: Decimal) -> dict:
    adjusted = expected_abs.adjusted()
    scaled_for_leading = expected_abs.scaleb(-adjusted)
    leading_two = int((scaled_for_leading * Decimal(10)).to_integral_value(rounding=ROUND_HALF_UP))
    sigfigs = 2 if 10 <= leading_two <= 34 else 1
    scale_exp = sigfigs - 1 - adjusted
    scaled = expected_abs.scaleb(scale_exp)
    rounded_digits = round_4_up_to_int(scaled)
    decimals_needed = max(0, scale_exp)
    return {
        "leading_two": leading_two,
        "sigfigs": sigfigs,
        "rounded_digits": rounded_digits,
        "decimals_needed": decimals_needed,
    }


def format_value(value: Decimal, decimals: int) -> str:
    quantum = Decimal("1") if decimals == 0 else Decimal("1." + ("0" * decimals))
    rounded = value.quantize(quantum)
    text = format(rounded, "f")
    if decimals == 0:
        return text.split(".")[0]
    whole, frac = text.split(".")
    return f"{whole}.{frac.ljust(decimals, '0')}"


def build_line_with_new_t_dt(line: str, new_t: str, new_dt: str) -> str:
    return f"{line[:39]}{new_t.ljust(10)}{new_dt.ljust(6)}{line[55:]}"


def ideal_width_fix(level: Level) -> WidthFix | None:
    if uses_1977da03_t(level):
        return None
    parsed = parse_t_fields(level)
    if parsed is None:
        return None
    rel = relative_fraction(parsed["value"], parsed["unit"])
    expected_abs = parsed["value"] * rel
    strict = strict_uncertainty_model(expected_abs)
    new_value_text = format_value(parsed["value"], strict["decimals_needed"])
    new_t = f"{new_value_text} {parsed['unit']}"
    new_dt = str(strict["rounded_digits"])
    if level.t_text.strip() == new_t and level.dt_text.strip() == new_dt:
        return None
    new_line = build_line_with_new_t_dt(level.raw, new_t, new_dt)
    return WidthFix(
        line=level.line,
        energy_text=level.energy_text,
        old_line=level.raw,
        new_line=new_line,
        old_t=level.t_text.strip(),
        old_dt=level.dt_text.strip(),
        new_t=new_t,
        new_dt=new_dt,
        rule="20%" if rel == Decimal("0.20") else "10%",
    )


def main() -> None:
    source_levels = parse_levels(SOURCE)
    target_levels = parse_levels(TARGET, require_xref_with_l=True)
    if len(source_levels) != len(target_levels):
        raise SystemExit(f"Count mismatch: source={len(source_levels)} target={len(target_levels)}")

    source_fixes = [fix for level in source_levels if (fix := ideal_width_fix(level)) is not None]
    source_fix_map = {fix.line: fix for fix in source_fixes}

    target_fixes: list[dict] = []
    pairs = list(zip(source_levels, target_levels))
    for source_level, target_level in pairs:
        source_fix = source_fix_map.get(source_level.line)
        if source_fix is None:
            continue
        target_parsed = parse_t_fields(target_level)
        if target_parsed is None:
            continue
        target_new_line = build_line_with_new_t_dt(target_level.raw, source_fix.new_t, source_fix.new_dt)
        if target_level.t_text.strip() == source_fix.new_t and target_level.dt_text.strip() == source_fix.new_dt:
            continue
        target_fixes.append({
            "source_line": source_level.line,
            "target_line": target_level.line,
            "source_energy": source_level.energy_text,
            "target_energy": target_level.energy_text,
            "xref": target_level.xref,
            "old_line": target_level.raw,
            "new_line": target_new_line,
            "old_t": target_level.t_text.strip(),
            "old_dt": target_level.dt_text.strip(),
            "new_t": source_fix.new_t,
            "new_dt": source_fix.new_dt,
        })

    print("SUMMARY")
    print({
        "source_levels_in_scope": len(source_levels),
        "target_levels_in_scope": len(target_levels),
        "source_width_fixes": len(source_fixes),
        "target_width_fixes": len(target_fixes),
        "excluded_1977Da03_source_widths": sum(1 for level in source_levels if level.t_text.strip() and uses_1977da03_t(level)),
    })
    print("SOURCE_FIXES")
    for item in source_fixes:
        print({
            "line": item.line,
            "energy": item.energy_text,
            "old_t": item.old_t,
            "old_dt": item.old_dt,
            "new_t": item.new_t,
            "new_dt": item.new_dt,
            "rule": item.rule,
            "old_line": item.old_line,
            "new_line": item.new_line,
        })
    print("TARGET_FIXES")
    for item in target_fixes:
        print(item)
    print("SPECIAL_CASES")
    print({
        "target_line_2193_requires_comment_review": True,
        "reason": "7078.90 adopted width/comment currently averages 1977Da03 and 1989Va15; user instructed 1977Da03 T data can be omitted.",
    })


def emit_source_patch() -> None:
    source_levels = parse_levels(SOURCE)
    fixes = [fix for level in source_levels if (fix := ideal_width_fix(level)) is not None]
    print("*** Begin Patch")
    print(f"*** Update File: {SOURCE}")
    for fix in fixes:
        print("@@")
        print(f"-{fix.old_line}")
        print(f"+{fix.new_line}")
    print("*** End Patch")


def emit_target_patch() -> None:
    source_levels = parse_levels(SOURCE)
    target_levels = parse_levels(TARGET, require_xref_with_l=True)
    if len(source_levels) != len(target_levels):
        raise SystemExit(f"Count mismatch: source={len(source_levels)} target={len(target_levels)}")
    source_fix_map = {
        fix.line: fix
        for level in source_levels
        if (fix := ideal_width_fix(level)) is not None
    }
    print("*** Begin Patch")
    print(f"*** Update File: {TARGET}")
    for source_level, target_level in zip(source_levels, target_levels):
        source_fix = source_fix_map.get(source_level.line)
        if source_fix is None:
            continue
        target_parsed = parse_t_fields(target_level)
        if target_parsed is None:
            continue
        if target_level.t_text.strip() == source_fix.new_t and target_level.dt_text.strip() == source_fix.new_dt:
            continue
        target_new_line = build_line_with_new_t_dt(target_level.raw, source_fix.new_t, source_fix.new_dt)
        print("@@")
        print(f"-{target_level.raw}")
        print(f"+{target_new_line}")
    print("*** End Patch")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--emit-source-patch":
        emit_source_patch()
    elif len(sys.argv) > 1 and sys.argv[1] == "--emit-target-patch":
        emit_target_patch()
    else:
        main()
