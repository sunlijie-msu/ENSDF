from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


DEFAULT_OLD_FILE = r"D:\X\ND\ENSDF\A35\A35_NDS2011.txt"
DEFAULT_NEW_FILE = r"D:\X\ND\ENSDF\A35\A35_revised_2026.ens"


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def powershell_style_counts(old_lines: list[str], new_lines: list[str]) -> tuple[int, int, int]:
    old_counter = Counter(old_lines)
    new_counter = Counter(new_lines)

    removed = sum((old_counter - new_counter).values())
    added = sum((new_counter - old_counter).values())
    total = removed + added
    return total, removed, added


def compare_object_counts(old_path: Path, new_path: Path) -> tuple[int, int, int, str]:
    old_literal = str(old_path).replace("'", "''")
    new_literal = str(new_path).replace("'", "''")
    ps_command = (
        f"$d=Compare-Object (Get-Content -LiteralPath '{old_literal}') (Get-Content -LiteralPath '{new_literal}');"
        "$o=[PSCustomObject]@{"
        "Total=@($d).Count;"
        "Added=@($d|Where-Object SideIndicator -eq '=>').Count;"
        "Removed=@($d|Where-Object SideIndicator -eq '<=').Count"
        "};"
        "$o|ConvertTo-Json -Compress"
    )

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            ps_command,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and result.stdout.strip():
        payload = json.loads(result.stdout.strip())
        return int(payload["Total"]), int(payload["Removed"]), int(payload["Added"]), "Compare-Object"

    old_lines = read_lines(old_path)
    new_lines = read_lines(new_path)
    total, removed, added = powershell_style_counts(old_lines, new_lines)
    return total, removed, added, "CounterFallback"


def git_numstat_counts(old_path: Path, new_path: Path) -> tuple[int | None, int | None, str, int]:
    cmd = [
        "git",
        "diff",
        "--no-index",
        "--numstat",
        "--",
        str(old_path),
        str(new_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    git_exit_code = result.returncode

    stdout_lines = [line for line in result.stdout.splitlines() if line.strip()]
    if stdout_lines:
        parts = stdout_lines[0].split("\t")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]), int(parts[1]), "ok", git_exit_code

    if git_exit_code in (0, 1):
        return None, None, "no-numstat-output", git_exit_code

    return None, None, f"git-error({git_exit_code})", git_exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two files with Compare-Object-style and git --numstat-style metrics."
    )
    parser.add_argument(
        "old_file",
        nargs="?",
        default=DEFAULT_OLD_FILE,
        help="Path to old/original file (optional; defaults to DEFAULT_OLD_FILE in this script)",
    )
    parser.add_argument(
        "new_file",
        nargs="?",
        default=DEFAULT_NEW_FILE,
        help="Path to new/edited file (optional; defaults to DEFAULT_NEW_FILE in this script)",
    )
    args = parser.parse_args()

    old_path = Path(args.old_file).resolve()
    new_path = Path(args.new_file).resolve()

    if not old_path.is_file():
        raise FileNotFoundError(f"Old file not found: {old_path}")
    if not new_path.is_file():
        raise FileNotFoundError(f"New file not found: {new_path}")

    ps_total, ps_removed, ps_added, ps_method = compare_object_counts(old_path, new_path)
    git_added, git_deleted, git_status, git_exit_code = git_numstat_counts(old_path, new_path)

    print(f"OldFile\t{old_path}")
    print(f"NewFile\t{new_path}")
    print(f"PowerShellTotal\t{ps_total}")
    print(f"PowerShellRemoved\t{ps_removed}")
    print(f"PowerShellAdded\t{ps_added}")
    print(f"PowerShellMethod\t{ps_method}")
    print(f"GitAdded\t{git_added}")
    print(f"GitDeleted\t{git_deleted}")
    print(f"GitStatus\t{git_status}")
    print(f"GitExitCode\t{git_exit_code}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
