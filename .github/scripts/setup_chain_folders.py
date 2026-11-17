#!/usr/bin/env python3
r"""Organize a mass-chain folder into the A60 evaluation layout.

Flat layout (before):                      Target layout (as in A60):
  A61\Co61\Co61_adopted.new                  A61\Co61\new\Co61_adopted.ens
  A61\Co61\Co61_adopted.old                  A61\Co61\old\Co61_adopted.old
  A61\Co61\Co61_x_xundl-2.ens                A61\Co61\new\Co61_x_xundl-2.ens
  A61\Co61\Co61_x_xundl-2.xundl              A61\Co61\old\Co61_x_xundl-2.xundl
  A61\A61_cover.new                          A61\A61_cover.ens

Rules, applied inside every nuclide folder of the chain:
  *.new   -> new\<stem>.ens   evaluator's working dataset, final name
  *.old   -> old\             previous evaluation round, archived
  *.xundl -> old\             XUNDL archive copy
  *.ens   -> new\             dataset, including *_xundl-N.ens
Chain root: <chain>_*.new -> <stem>.ens; existing *.old/*.ens stay in place.

Nothing is overwritten and nothing is deleted except a byte-identical
duplicate: every move is verified by SHA-256 before and after, and a
destination holding different content aborts that file as a conflict.

Usage (run from the repository root, or pass an absolute chain path):
  python .github\scripts\setup_chain_folders.py A61
      Dry run: list every planned move, dedup and conflict.
  python .github\scripts\setup_chain_folders.py A61 --apply
      Perform the moves, then verify the resulting layout.
  python .github\scripts\setup_chain_folders.py A61 --verify
      Only check that the folder already has the A60 layout.
  python .github\scripts\setup_chain_folders.py D:\X\ND\ENSDF\A62 --apply
      Same, for a chain given as an absolute path.
"""

import argparse
import hashlib
import pathlib
import re
import shutil
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
GITATTRIBUTES = "# Auto detect text files and perform LF normalization\n* text=auto\n"
SUBDIRS = ("new", "old")
OWNED_SUFFIXES = (".new", ".old", ".xundl", ".ens")
NUCLIDE_RE = re.compile(r"[A-Z][a-z]?\d+")


def sha256(path):
    """Return the SHA-256 digest of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_nuclide_folder(path):
    """True for a chain subfolder named like a nuclide (A61, Al61, Ge60)."""
    return path.is_dir() and NUCLIDE_RE.fullmatch(path.name) is not None


def find_moves(root):
    """Return (moves, keeps) for the chain: moves are (source, destination)."""
    moves = []
    keeps = []
    for entry in sorted(root.iterdir()):
        if entry.is_file():
            # Chain root: only <chain>_*.new becomes <stem>.ens; cover.old,
            # references.old, PDFs and published .ens files stay put.
            if entry.suffix.lower() == ".new":
                moves.append((entry, root / (entry.stem + ".ens")))
            else:
                keeps.append(entry)
            continue
        if not is_nuclide_folder(entry):
            keeps.append(entry)
            continue
        for path in sorted(entry.iterdir()):
            if not path.is_file():
                keeps.append(path)
                continue
            suffix = path.suffix.lower()
            if suffix == ".new":
                moves.append((path, entry / "new" / (path.stem + ".ens")))
            elif suffix in (".old", ".xundl"):
                moves.append((path, entry / "old" / path.name))
            elif suffix == ".ens":
                moves.append((path, entry / "new" / path.name))
            else:
                keeps.append(path)
    return moves, keeps


def classify(source, destination):
    """Return (status, detail) for one planned move."""
    if not destination.exists():
        return "move", ""
    if destination.is_dir():
        return "conflict", "destination is a folder"
    if sha256(source) == sha256(destination):
        return "dedup", "destination byte-identical"
    return "conflict", "destination exists with different content"


def move_verified(source, destination):
    """Move one file and return an error string if the bytes changed."""
    digest = sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    if not destination.is_file():
        return f"move failed: {destination} missing after move"
    if sha256(destination) != digest:
        return f"content changed during move: {source} -> {destination}"
    return None


def plan_moves(root):
    """Return (plan, keeps): plan items are (source, destination, status, detail)."""
    moves, keeps = find_moves(root)
    plan = []
    claimed = {}
    for source, destination in moves:
        other = claimed.get(destination)
        if other is not None:
            if sha256(source) == sha256(other):
                status, detail = "dedup", f"byte-identical to {other.name}"
            else:
                status, detail = "conflict", f"same destination as {other.name}"
        else:
            claimed[destination] = source
            status, detail = classify(source, destination)
        plan.append((source, destination, status, detail))
    return plan, keeps


def run(root, apply_changes):
    """Plan, optionally perform, and report the reorganization."""
    plan, keeps = plan_moves(root)
    counts = {"move": 0, "dedup": 0, "conflict": 0}
    problems = []

    for source, destination, status, detail in plan:
        counts[status] += 1
        note = f"  ({detail})" if detail else ""
        print(f"  {status:8s} {source.relative_to(root.parent)} -> "
              f"{destination.relative_to(root.parent)}{note}")
        if status == "conflict":
            problems.append(f"refused: {source} -> {destination} ({detail})")

    verb = "would mkdir"
    missing = [
        (entry / name, f"{entry.name}\\{name}")
        for entry in sorted(root.iterdir()) if is_nuclide_folder(entry)
        for name in SUBDIRS if not (entry / name).is_dir()
    ]
    attributes = root / ".gitattributes"
    will_execute = apply_changes and not problems
    if will_execute:
        verb = "mkdir"
    for path, label in missing:
        print(f"  {verb:8s} {label}")
    if not attributes.is_file():
        print(f"  {verb:8s} {root.name}\\.gitattributes")

    header = "ABORTED" if problems else ("APPLIED" if will_execute else "DRY RUN")
    print(f"\n{header} - {len(plan)} files to organize, {len(keeps)} already in place")
    print(f"  move: {counts['move']}  dedup: {counts['dedup']}  "
          f"conflict: {counts['conflict']}")

    if problems:
        print("\nPROBLEMS (nothing was changed):")
        for problem in problems:
            print(f"  {problem}")
        return 1
    if not will_execute:
        return 0

    for path, _ in missing:
        path.mkdir(exist_ok=True)
    if not attributes.is_file():
        attributes.write_text(GITATTRIBUTES, encoding="utf-8")

    for source, destination, status, _ in plan:
        if status == "dedup":
            source.unlink()
            continue
        try:
            error = move_verified(source, destination)
        except OSError as exc:
            error = f"move failed: {source} -> {destination}: {exc}"
        if error:
            problems.append(error)

    if problems:
        print("\nPROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    return 0


def verify(root):
    """Check that the chain already matches the A60 layout."""
    errors = []
    for entry in sorted(root.iterdir()):
        if entry.is_file() and entry.suffix.lower() == ".new":
            errors.append(f"loose chain-root working file: {entry.name}")
        if not entry.is_dir() or entry.name in SUBDIRS:
            continue
        if not is_nuclide_folder(entry):
            # Auxiliary folders are left alone, but flag them when they hide
            # dataset files that the move rules would otherwise touch.
            stray = sorted(p.name for p in entry.iterdir()
                           if p.is_file() and p.suffix.lower() in OWNED_SUFFIXES)
            if stray:
                errors.append(f"unrecognized folder {entry.name}: {', '.join(stray)}")
            continue
        loose = sorted(p.name for p in entry.iterdir()
                       if p.is_file() and p.suffix.lower() in OWNED_SUFFIXES)
        if loose:
            errors.append(f"loose file(s) in {entry.name}: {', '.join(loose)}")
        for name in SUBDIRS:
            if not (entry / name).is_dir():
                errors.append(f"missing folder: {entry.name}\\{name}")
        for path in sorted((entry / "new").glob("*")):
            if path.is_file() and path.suffix.lower() in (".new", ".old", ".xundl"):
                errors.append(f"archived file in {entry.name}\\new: {path.name}")
        for path in sorted((entry / "old").glob("*")):
            if path.is_file() and path.suffix.lower() in (".new", ".ens"):
                errors.append(f"unreleased file in {entry.name}\\old: {path.name}")

    if not (root / ".gitattributes").is_file():
        errors.append("missing .gitattributes at chain root")

    datasets = sum(1 for _ in root.glob("*\\new\\*.ens"))
    archived = sum(1 for _ in root.glob("*\\old\\*"))
    print(f"  datasets in new folders: {datasets}")
    print(f"  archived files in old folders: {archived}")
    print("  chain-root files: " + ", ".join(
        sorted(p.name for p in root.iterdir() if p.is_file())))

    if errors:
        print("\nLAYOUT PROBLEMS:")
        for error in errors:
            print(f"  {error}")
        return 1
    print(f"\n[OK] {root.name} matches the A60 layout")
    return 0


def resolve_chain(value):
    """Accept a chain name (A61) or a path; return the absolute folder."""
    path = pathlib.Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("chain", help="chain folder name (A61) or absolute path")
    parser.add_argument("--apply", action="store_true",
                        help="perform the moves, then verify the layout")
    parser.add_argument("--verify", action="store_true",
                        help="only verify that the chain already has the A60 layout")
    args = parser.parse_args()

    root = resolve_chain(args.chain)
    if not root.is_dir():
        print(f"ERROR: chain folder not found: {root}")
        return 1
    if args.verify:
        return verify(root)

    code = run(root, args.apply)
    if code or not args.apply:
        return code

    print("\nVERIFY:")
    return verify(root)


if __name__ == "__main__":
    sys.exit(main())
