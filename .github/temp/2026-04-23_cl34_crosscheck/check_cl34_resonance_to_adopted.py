from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import re

SOURCE = Path(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_p_resonances.ens")
TARGET = Path(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens")
ENERGY_MIN = 6321.2
SPOTCHECK_SEED = 34023
FLOAT_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)?$")


@dataclass
class Level:
    line: int
    energy: float
    de: str
    j: str
    t: str
    dt: str
    raw: str
    xref: str | None
    comments: list[tuple[int, str]]


def parse_energy(text: str) -> float | None:
    text = text.strip()
    return float(text) if FLOAT_RE.match(text) else None


def is_l_record(line: str) -> bool:
    return len(line) >= 9 and line[5] == " " and line[6] == " " and line[7] == "L" and line[8] == " "


def parse_levels(path: Path, require_xref_with_l: bool = False) -> list[Level]:
    levels: list[Level] = []
    current: Level | None = None
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if is_l_record(line):
            energy = parse_energy(line[9:19])
            current = Level(
                line=idx,
                energy=energy if energy is not None else float("nan"),
                de=line[19:21].strip(),
                j=line[22:39].rstrip(),
                t=line[39:49].rstrip(),
                dt=line[49:55].rstrip(),
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
        if level.energy != level.energy or level.energy < ENERGY_MIN:
            continue
        if require_xref_with_l and (level.xref is None or "L" not in level.xref):
            continue
        scoped.append(level)
    return scoped


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def comment_lines(level: Level, tag: str) -> list[tuple[int, str]]:
    return [entry for entry in level.comments if f"{tag}$" in entry[1]]


def expected_t_comment_fragment(source: Level) -> str | None:
    if not source.t:
        return None
    value_unit = source.t.lower().replace("kev", "keV").replace("ev", "eV")
    if source.dt:
        return f"{value_unit} {{I{source.dt}}}"
    return value_unit


def contains_source_j(source: Level, target: Level) -> bool:
    if not source.j.strip():
        return True
    joined = " ".join(line for _, line in comment_lines(target, "J"))
    return source.j.strip() in joined


def contains_source_t(source: Level, target: Level) -> bool:
    if not source.t.strip():
        return True
    fragment = expected_t_comment_fragment(source)
    if fragment is None:
        return True
    joined = normalize_space(" ".join(line for _, line in comment_lines(target, "T")))
    return normalize_space(fragment) in joined


def main() -> None:
    source_levels = parse_levels(SOURCE)
    target_levels = parse_levels(TARGET, require_xref_with_l=True)
    if len(source_levels) != len(target_levels):
        raise SystemExit(f"Count mismatch: source={len(source_levels)} target={len(target_levels)}")

    pairs = list(zip(source_levels, target_levels))
    j_field_mismatches = []
    j_missing = []
    t_field_mismatches = []
    t_missing = []
    energy_pairs = []

    for source, target in pairs:
        delta = round(target.energy - source.energy, 3)
        energy_pairs.append(delta)

        source_j = source.j.strip()
        target_j = target.j.strip()
        source_t = source.t.strip()
        source_dt = source.dt.strip()
        target_t = target.t.strip()
        target_dt = target.dt.strip()

        if source_j and source_j != target_j:
            item = {
                "source_line": source.line,
                "target_line": target.line,
                "source_E": source.energy,
                "target_E": target.energy,
                "delta_E": delta,
                "source_J": source_j,
                "target_J": target_j,
                "xref": target.xref,
                "target_J_comments": [line for _, line in comment_lines(target, "J")],
            }
            j_field_mismatches.append(item)
            if not contains_source_j(source, target):
                j_missing.append(item)

        if source_t and (source_t, source_dt) != (target_t, target_dt):
            item = {
                "source_line": source.line,
                "target_line": target.line,
                "source_E": source.energy,
                "target_E": target.energy,
                "delta_E": delta,
                "source_T": source_t,
                "source_DT": source_dt,
                "target_T": target_t,
                "target_DT": target_dt,
                "xref": target.xref,
                "target_T_comments": [line for _, line in comment_lines(target, "T")],
            }
            t_field_mismatches.append(item)
            if not contains_source_t(source, target):
                t_missing.append(item)

    print("CONFIG")
    print({
        "source": str(SOURCE),
        "target": str(TARGET),
        "scope_min_energy": ENERGY_MIN,
        "checks": ["value/sign", "uncertainty/format", "completeness"],
        "matching": "ordered one-to-one after verifying equal counts in scoped source and target",
    })
    print("SUMMARY")
    print({
        "source_levels": len(source_levels),
        "target_levels_with_L": len(target_levels),
        "max_abs_delta_E": max(abs(value) for value in energy_pairs),
        "j_field_mismatches": len(j_field_mismatches),
        "j_missing_from_field_and_comments": len(j_missing),
        "t_field_mismatches": len(t_field_mismatches),
        "t_missing_from_field_and_comments": len(t_missing),
    })

    print("J_FIELD_MISMATCHES")
    for item in j_field_mismatches:
        print(item)

    print("T_FIELD_MISMATCHES")
    for item in t_field_mismatches:
        print(item)

    print("J_MISSING")
    for item in j_missing:
        print(item)

    print("T_MISSING")
    for item in t_missing:
        print(item)

    sample_size = max(10, -(-len(pairs) * 15 // 100))
    random.seed(SPOTCHECK_SEED)
    sample = random.sample(pairs, sample_size)
    print("SPOTCHECK")
    print({"sample_size": sample_size, "seed": SPOTCHECK_SEED})
    failures = []
    for idx, (source, target) in enumerate(sample, 1):
        result = {
            "sample": idx,
            "source_line": source.line,
            "target_line": target.line,
            "source_E": source.energy,
            "target_E": target.energy,
            "xref": target.xref,
            "j_ok": (not source.j.strip()) or (source.j.strip() == target.j.strip()) or contains_source_j(source, target),
            "t_ok": (not source.t.strip()) or ((source.t.strip(), source.dt.strip()) == (target.t.strip(), target.dt.strip())) or contains_source_t(source, target),
        }
        if not (result["j_ok"] and result["t_ok"]):
            failures.append(result)
        print(result)
    print({"spotcheck_failures": len(failures)})


if __name__ == "__main__":
    main()
