#!/usr/bin/env python3
r"""Synchronize finished ENSDF datasets into workspace new folders.

Source:  D:\X\ND\Files\A34\finished\<Nuclide>\*.ens
         D:\X\ND\Files\A34\finished\A34_cover.ens
Target:  D:\X\ND\ENSDF\A34\<Nuclide>\new\*.ens
         D:\X\ND\ENSDF\A34\A34_cover.ens

Dataset synchronization is limited to .ens files directly inside target
``new`` folders. The root-level A34_cover.ens is the sole root-file exception.
The script never scans, changes, or deletes ``old``, ``raw``, ``pdf``, or
any other folders/files. The root-level A34_cover.ens is explicitly copied
to the matching target path when new or changed; other root files are ignored.

Usage (run from repository root D:\X\ND\ENSDF):
  python .github\temp\keep_do_not_delete\copy_finished_ens.py --help
      Show command-line help.

  python .github\temp\keep_do_not_delete\copy_finished_ens.py
      Dry run. Report cover and dataset changes plus stale new-folder ENS files.
      Does not change any files.

  python .github\temp\keep_do_not_delete\copy_finished_ens.py --apply
      Copy new/changed dataset files and A34_cover.ens; remove stale .ens
      files only from Nuclide\new folders.
      Review the dry-run output before using this command.

Usage (run after changing into the script folder):
  cd /d D:\X\ND\ENSDF\.github\temp\keep_do_not_delete
  python copy_finished_ens.py
  python copy_finished_ens.py --apply
"""

import argparse
import pathlib
import shutil
import sys

SRC_ROOT = pathlib.Path(r"D:\X\ND\Files\A34\finished")
DST_ROOT = pathlib.Path(r"D:\X\ND\ENSDF\A34")


def source_files() -> dict[pathlib.Path, pathlib.Path]:
    """Return source dataset files keyed by target-relative path."""
    files = {}
    cover = SRC_ROOT / "A34_cover.ens"
    if cover.is_file():
        files[pathlib.Path(cover.name)] = cover

    for folder in SRC_ROOT.iterdir():
        if not folder.is_dir():
            continue
        for source in folder.glob("*.ens"):
            files[pathlib.Path(folder.name) / "new" / source.name] = source
    return files


def target_files() -> dict[pathlib.Path, pathlib.Path]:
    """Return only .ens files directly inside target Nuclide\\new folders."""
    if not DST_ROOT.is_dir():
        return {}
    files = {}
    for folder in DST_ROOT.iterdir():
        new_folder = folder / "new"
        if folder.is_dir() and new_folder.is_dir():
            for target in new_folder.glob("*.ens"):
                files[target.relative_to(DST_ROOT)] = target
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="copy source files and remove stale .ens files only from new folders",
    )
    args = parser.parse_args()

    if not SRC_ROOT.is_dir():
        print(f"ERROR: source folder not found: {SRC_ROOT}")
        return 1

    sources = source_files()
    targets = target_files()
    counts = {"new": 0, "replace": 0, "same": 0, "remove": 0}
    problems = []

    for rel, src in sorted(sources.items()):
        tgt = DST_ROOT / rel
        if not tgt.exists():
            counts["new"] += 1
            status = "new"
        elif src.read_bytes() == tgt.read_bytes():
            counts["same"] += 1
            status = "same"
        else:
            counts["replace"] += 1
            status = "replace"

        if args.apply and status in ("new", "replace"):
            tgt.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, tgt)
            if src.read_bytes() != tgt.read_bytes():
                problems.append(f"copy verification failed: {rel}")

        print(f"  {status:8s} {rel}")

    for rel, target in sorted(targets.items()):
        if rel in sources:
            continue
        counts["remove"] += 1
        print(f"  {'remove':8s} {rel}")
        if args.apply:
            try:
                target.unlink()
            except OSError as exc:
                problems.append(f"remove failed for {rel}: {exc}")

    ignored = sorted(
        path for path in SRC_ROOT.glob("*")
        if path.is_file() and pathlib.Path(path.name) not in sources
    )
    for path in ignored:
        print(f"  {'ignored':8s} {path.relative_to(SRC_ROOT)}")

    print(f"\n{'APPLIED' if args.apply else 'DRY RUN'} - {len(sources)} source dataset files")
    print(
        f"  new: {counts['new']}  replaced: {counts['replace']}  "
        f"already identical: {counts['same']}  stale new ENS files removed: {counts['remove']}"
    )

    if problems:
        print("\nPROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
