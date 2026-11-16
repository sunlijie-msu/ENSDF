#!/usr/bin/env python3
r"""Set up the A=61 mass-chain working tree in the A60 layout.

Current A61 layout is flat inside each nuclide folder; the A60 reference
layout separates the finished datasets from the archived material:

  A61\Co61\Co61_adopted.new        ->  A61\Co61\new\Co61_adopted.ens
  A61\Co61\Co61_adopted.old        ->  A61\Co61\old\Co61_adopted.old
  A61\Co61\Co61_..._xundl-2.ens    ->  A61\Co61\new\Co61_..._xundl-2.ens
  A61\Co61\Co61_..._xundl-2.xundl  ->  A61\Co61\old\Co61_..._xundl-2.xundl
  A61\A61_cover.new                ->  A61\A61_cover.ens
  A61\A61_cover.old                ->  unchanged, stays at chain root (as A60_cover.old)

Rules
  *.new   -> <Nuclide>\new\<stem>.ens   evaluator's working dataset, final name
  *.old   -> <Nuclide>\old\             previous evaluation round, archived
  *.xundl -> <Nuclide>\old\             XUNDL archive copy
  *.ens   -> <Nuclide>\new\             dataset, including *_xundl-N.ens
Chain root: <chain>_*.new -> <stem>.ens; existing *.old/*.ens stay in place.

No file is copied over another and nothing is deleted except a byte-identical
duplicate source. Every move is verified by SHA-256 before and after, so a
failed move is reported instead of silently losing a dataset.

Usage (from the repository root D:\X\ND\ENSDF):
  python .github\temp\2026-11-16_A61_setup\setup_A61_folders.py --help
  python .github\temp\2026-11-16_A61_setup\setup_A61_folders.py
      Dry run: print every planned move, dedup and conflict.
  python .github\temp\2026-11-16_A61_setup\setup_A61_folders.py --apply
      Perform the moves, then verify the resulting layout.
  python .github\temp\2026-11-16_A61_setup\setup_A61_folders.py --verify
      Only check that the tree already has the A60 layout.
"""

import argparse
import hashlib
import pathlib
import shutil
import sys

DEFAULT_ROOT = pathlib.Path(r"D:\X\ND\ENSDF\A61")
REFERENCE_ROOT = pathlib.Path(r"D:\X\ND\ENSDF\A60")
GITATTRIBUTES = "# Auto detect text files and perform LF normalization\n* text=auto\n"
SUBDIRS = ("new", "old")


def sha256(path):
    """Return the SHA-256 digest of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_moves(root):
    """Return (moves, keeps): moves are (source, destination) pairs."""
    moves = []
    keeps = []
    for entry in sorted(root.iterdir()):
        if entry.is_file():
            # Chain-root files: only <chain>_*.new is renamed, everything else
            # (cover.old, references.old, PDFs) stays at the root as in A60.
            if entry.suffix.lower() == ".new":
                moves.append((entry, root / (entry.stem + ".ens")))
            else:
                keeps.append(entry)
            continue
        if not entry.is_dir() or entry.name in SUBDIRS:
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


def apply_move(source, destination):
    """Move one file and verify the bytes survived the move."""
    digest = sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    if not destination.is_file():
        return f"move failed: {destination} missing after move"
    if sha256(destination) != digest:
        return f"content changed during move: {source} -> {destination}"
    return None


def run(root, apply_changes):
    """Plan, optionally perform, and report the reorganization."""
    moves, keeps = find_moves(root)
    counts = {"move": 0, "dedup": 0, "conflict": 0}
    problems = []

    for source, destination in moves:
        status, detail = classify(source, destination)
        counts[status] += 1
        label = root.name + "\\" + str(source.relative_to(root))
        target = root.name + "\\" + str(destination.relative_to(root))
        note = f"  ({detail})" if detail else ""
        print(f"  {status:8s} {label} -> {target}{note}")
        if status == "conflict":
            problems.append(f"refused: {label} -> {target} ({detail})")
            continue
        if not apply_changes:
            continue
        if status == "dedup":
            source.unlink()
            continue
        error = apply_move(source, destination)
        if error:
            problems.append(error)

    for path in keeps:
        print(f"  {'keep':8s} {root.name}\\{path.relative_to(root)}")

    if apply_changes:
        for folder in sorted(p for p in root.iterdir() if p.is_dir()):
            for name in SUBDIRS:
                (folder / name).mkdir(exist_ok=True)

    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'} - {len(moves)} files to organize")
    print(
        f"  moved: {counts['move']}  duplicate source removed: {counts['dedup']}  "
        f"conflicts: {counts['conflict']}  left in place: {len(keeps)}"
    )

    if problems:
        print("\nPROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    return 0


def verify(root):
    """Check that the tree already matches the A60 layout."""
    errors = []
    for entry in sorted(root.iterdir()):
        if entry.is_file() and entry.suffix.lower() == ".new":
            errors.append(f"loose chain-root working file: {entry.name}")
        if not entry.is_dir() or entry.name in SUBDIRS:
            continue
        for path in sorted(entry.iterdir()):
            if path.is_file():
                errors.append(f"loose file in {entry.name}: {path.name}")
        for name in SUBDIRS:
            if not (entry / name).is_dir():
                errors.append(f"missing folder: {entry.name}\\{name}")
        for path in sorted((entry / "new").glob("*")):
            if path.is_file() and path.suffix.lower() != ".ens":
                errors.append(f"non-ENs file in {entry.name}\\new: {path.name}")
        for path in sorted((entry / "old").glob("*")):
            if path.is_file() and path.suffix.lower() not in (".old", ".xundl"):
                errors.append(f"unexpected file in {entry.name}\\old: {path.name}")

    if not (root / ".gitattributes").is_file():
        errors.append("missing .gitattributes at chain root")

    datasets = sum(1 for _ in root.glob("*\\new\\*.ens"))
    archived = sum(1 for _ in root.glob("*\\old\\*"))
    print(f"  datasets in new folders: {datasets}")
    print(f"  archived files in old folders: {archived}")
    print(f"  chain-root files: {', '.join(sorted(p.name for p in root.iterdir() if p.is_file()))}")

    if errors:
        print("\nLAYOUT PROBLEMS:")
        for error in errors:
            print(f"  {error}")
        return 1
    print("\n[OK] A61 tree matches the A60 layout")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT,
                        help=f"chain folder to organize (default: {DEFAULT_ROOT})")
    parser.add_argument("--apply", action="store_true",
                        help="perform the moves, then verify the layout")
    parser.add_argument("--verify", action="store_true",
                        help="only verify that the tree already has the A60 layout")
    args = parser.parse_args()

    root = args.root
    if not root.is_dir():
        print(f"ERROR: chain folder not found: {root}")
        return 1
    if args.verify:
        return verify(root)

    code = run(root, args.apply)
    if code or not args.apply:
        return code

    attributes = root / ".gitattributes"
    if not attributes.is_file():
        reference = REFERENCE_ROOT / ".gitattributes"
        attributes.write_text(
            reference.read_text() if reference.is_file() else GITATTRIBUTES,
            encoding="utf-8",
        )
        print(f"  created {root.name}\\.gitattributes (copied from {REFERENCE_ROOT.name})")

    print("\nVERIFY:")
    return verify(root)


if __name__ == "__main__":
    sys.exit(main())
