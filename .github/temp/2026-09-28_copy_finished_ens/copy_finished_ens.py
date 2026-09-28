#!/usr/bin/env python3
"""Copy revised individual ENSDF datasets from a "finished" folder into the workspace.

Source:  D:\\X\\ND\\Files\\A34\\finished\\<Nuclide>\\<file>.ens
Target:  <workspace>\\A34\\<Nuclide>\\new\\<file>.ens

Rules:
  * The source file name is authoritative: the target file name is identical to it.
  * Root-level source files (e.g. A34_cover.ens) go to A34\\<file>.ens.
  * A few workspace files still carry older names for the same dataset; those are
    listed in LEGACY_NAMES and are removed once the correctly named copy is in place.
    A legacy file is only removed when its ID line matches the source file's ID line.
  * Files are copied byte-for-byte, so line endings and encoding are preserved.

Usage:
  python copy_finished_ens.py            # dry run (report only)
  python copy_finished_ens.py --apply    # copy files and retire legacy names
"""

import argparse
import pathlib
import shutil
import sys

SRC_ROOT = pathlib.Path(r"D:\X\ND\Files\A34\finished")
DST_ROOT = pathlib.Path(r"D:\X\ND\ENSDF\A34")
NEW_DIR = "new"

# Older workspace name (relative to DST_ROOT) -> source-relative path of the same dataset.
# The dataset is identified by its ID line, which both sides share.
LEGACY_NAMES = {
    r"Al34\new\Al34_34mg_beta_decay_44.9_ms.ens": r"Al34\Al34_beta_decay_44.9_ms.ens",
    r"Al34\new\Al34_he_34al_34alg.ens": r"Al34\Al34_he_34al_34alPg.ens",
    r"Cl34\new\Cl34_33s_p_p_resonances.ens": r"Cl34\Cl34_33s_p_p_p_pPg_resonances.ens",
    r"Cl34\new\Cl34_34ar_ec_decay_0.84646_s.ens": r"Cl34\Cl34_34ar_ec+b+_decay_0.84646_s.ens",
    r"S34\new\S34_34cl_ec_decay_1.5266_s.ens": r"S34\S34_34cl_ec+b+_decay_1.5266_s.ens",
    r"S34\new\S34_34cl_ec_decay_31.99_m.ens": r"S34\S34_34cl_ec+b+_decay_31.99_m.ens",
    r"S34\new\S34_34s_p_pP_pol_p_pP.ens": r"S34\S34_34s_p_p_p_pP_pol_p_pP.ens",
    r"S34\new\S34_34p_beta_decay_12.43_s.ens": r"S34\S34_beta_decay_12.43_s.ens",
    r"S34\new\S34_33s_n_g_n_n_resonances.ens": r"S34\S34_ng_n_n_resonances.ens",
}


def target_for(rel: str) -> pathlib.Path:
    """Workspace target path for a source-relative path (same file name)."""
    parts = pathlib.PurePath(rel).parts
    if len(parts) == 1:                      # root-level file -> A34\<file>.ens
        return DST_ROOT / parts[0]
    return DST_ROOT / parts[0] / NEW_DIR / parts[-1]


def id_line(path: pathlib.Path) -> str:
    """First line of a file (the ENSDF ID record), used to identify a dataset."""
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        return fh.readline().rstrip("\n\r")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="copy files (default: dry run)")
    args = parser.parse_args()

    if not SRC_ROOT.is_dir():
        print(f"ERROR: source folder not found: {SRC_ROOT}")
        return 1

    sources = sorted(SRC_ROOT.rglob("*.ens"))
    counts = {"new": 0, "replace": 0, "same": 0, "no-dir": 0}
    problems = []

    for src in sources:
        rel = str(src.relative_to(SRC_ROOT))
        tgt = target_for(rel)

        if not tgt.parent.is_dir():
            counts["no-dir"] += 1
            problems.append(f"missing target folder: {tgt.parent}")
            status = "NO-DIR"
        elif not tgt.exists():
            counts["new"] += 1
            status = "new"
        elif src.read_bytes() == tgt.read_bytes():
            counts["same"] += 1
            status = "same"
        else:
            counts["replace"] += 1
            status = "replace"

        if args.apply and status in ("new", "replace"):
            shutil.copy2(src, tgt)
            if src.read_bytes() != tgt.read_bytes():
                problems.append(f"copy verification failed: {tgt}")

        print(f"  {status:8s} {rel}")

    # Retire workspace files that carry an older name for the same dataset.
    for legacy_rel, src_rel in sorted(LEGACY_NAMES.items()):
        legacy = DST_ROOT / legacy_rel
        src = SRC_ROOT / src_rel
        if not src.is_file():
            problems.append(f"LEGACY_NAMES entry has no source file: {src_rel}")
            continue
        if not legacy.exists():
            continue
        if id_line(legacy) != id_line(src):
            problems.append(f"NOT removed (ID line differs - review by hand): {legacy_rel}")
            continue
        print(f"  {'remove':8s} {legacy_rel}  (renamed to {pathlib.PurePath(src_rel).name})")
        if args.apply:
            legacy.unlink()

    # Anything left in new/ that the source does not provide is reported, never deleted.
    provided = {target_for(str(s.relative_to(SRC_ROOT))).name.lower() for s in sources}
    legacy_keys = {k.lower() for k in LEGACY_NAMES}
    for folder in sorted(p for p in DST_ROOT.iterdir() if p.is_dir() and (p / NEW_DIR).is_dir()):
        for extra in sorted((folder / NEW_DIR).glob("*.ens")):
            rel = str(extra.relative_to(DST_ROOT)).lower()
            if extra.name.lower() not in provided and rel not in legacy_keys:
                problems.append(f"stale file not in source (left untouched): {extra.relative_to(DST_ROOT)}")

    print(f"\n{'APPLIED' if args.apply else 'DRY RUN'} - {len(sources)} source files")
    print(f"  new: {counts['new']}  replaced: {counts['replace']}  "
          f"already identical: {counts['same']}  missing target folder: {counts['no-dir']}")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  {p}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
