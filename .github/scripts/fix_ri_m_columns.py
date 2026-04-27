#!/usr/bin/env python3
"""
Fix ENSDF G-record RI and M left-shift issues only. Shifts RI/M columns right by one if col22/col32 are non-space, but only on true G-records with strict 80-character length.

Usage:
  python fix_ri_m_columns.py Cl34_adopted.ens
  python fix_ri_m_columns.py A34/Cl34/new/Cl34_adopted.ens

Behavior:
- Edits the input file IN-PLACE (no separate output file created).
- Accepts file path or bare filename.
- If bare filename is not found directly, searches workspace recursively.
- Requires true G-record lines to be exactly 80 characters (excluding newline).
- Non-G lines are passed through unchanged.
- Applies only these fixes on true G-records:
  1) RI: col22->col23 shift (indices 21:28 -> 22:29)
  2) M:  col32->col33 shift (indices 31:40 -> 32:41)
- DRI and all non-target columns remain byte-identical.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


def is_true_g_record(line80: str) -> bool:
    return len(line80) == 80 and line80[6] == " " and line80[7] == "G" and line80[8] == " "


def resolve_input(user_arg: str, workspace_root: Path) -> Path:
    p = Path(user_arg)
    if p.exists():
        return p.resolve()

    # Try relative to workspace root first.
    p2 = workspace_root / user_arg
    if p2.exists():
        return p2.resolve()

    # Fallback: recursive basename search.
    matches = list(workspace_root.rglob(Path(user_arg).name))
    files = [m for m in matches if m.is_file()]

    if len(files) == 1:
        return files[0].resolve()

    if len(files) == 0:
        raise FileNotFoundError(f"Input not found: {user_arg}")

    sample = "\n".join(f"- {m}" for m in files[:20])
    raise RuntimeError(
        "Ambiguous input filename. Multiple matches found. "
        "Provide a path instead.\n" + sample
    )


def ensure_g_lines_80(lines: Iterable[str], src: Path) -> None:
    bad = []
    for i, line in enumerate(lines, start=1):
        core = line[:-1] if line.endswith("\n") else line
        if core == "" or len(core) < 9:
            continue
        # Enforce strict 80-column length only for true G-records.
        if core[6] == " " and core[7] == "G" and core[8] == " " and len(core) != 80:
            bad.append((i, len(core)))
            if len(bad) >= 10:
                break
    if bad:
        details = "\n".join(f"line {ln}: length {lg}" for ln, lg in bad)
        raise ValueError(
            f"Input has non-80 G-record lines: {src}\n{details}"
        )


def fix_one_line(line80: str) -> tuple[str, bool, bool]:
    chars = list(line80)
    original = line80
    ri_fixed = False
    m_fixed = False

    # RI fix: col 22 (idx 21) must always be a readability space in valid G-records.
    # If it is non-space, the RI value is shifted one column left and must be corrected.
    if chars[21] != " ":
        moved = chars[21:28]  # 7 chars starting at wrong col 22
        chars[21] = " "
        chars[22:29] = moved   # shift right to correct cols 23-29
        ri_fixed = True

    # M fix: col 32 (idx 31) must always be a readability space in valid G-records.
    # If it is non-space, the M value is shifted one column left and must be corrected.
    if chars[31] != " ":
        moved = chars[31:40]  # cols 32-40
        chars[31] = " "
        chars[32:41] = moved   # cols 33-41
        m_fixed = True

    fixed = "".join(chars)

    # Hard invariant: only RI and M windows may change.
    allowed = set(range(21, 29)) | set(range(31, 41))
    for idx, (a, b) in enumerate(zip(original, fixed)):
        if idx not in allowed and a != b:
            raise RuntimeError(
                f"Unexpected change outside RI/M windows at index {idx}"
            )

    return fixed, ri_fixed, m_fixed


def process(src: Path) -> Path:
    raw = src.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    ensure_g_lines_80(lines, src)

    out_lines: list[str] = []
    g_scanned = 0
    changed_lines = 0
    ri_count = 0
    m_count = 0

    for line in lines:
        nl = "\n" if line.endswith("\n") else ""
        core = line[:-1] if nl else line

        if not is_true_g_record(core):
            out_lines.append(line)
            continue

        g_scanned += 1
        fixed, ri_fixed, m_fixed = fix_one_line(core)

        if fixed != core:
            changed_lines += 1
        if ri_fixed:
            ri_count += 1
        if m_fixed:
            m_count += 1

        out_lines.append(fixed + nl)

    src.write_text("".join(out_lines), encoding="utf-8", newline="")

    print(f"File:              {src}")
    print(f"G-records scanned: {g_scanned}")
    print(f"Lines changed:     {changed_lines}")
    print(f"RI shifts applied: {ri_count}")
    print(f"M shifts applied:  {m_count}")

    return src


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix RI/M column left-shifts on ENSDF G-records in-place."
    )
    parser.add_argument("input", help="Input .ens file path or filename")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parent.parent
    src = resolve_input(args.input, workspace_root)
    process(src)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
