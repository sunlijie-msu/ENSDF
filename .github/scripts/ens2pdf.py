"""
ens2pdf.py — Convert ENSDF files to PDF using the McMaster-MSU Java NDS tool.

HOW TO USE:
  1. Edit the CONFIG section below (ELEMENT, MASS, FILES).
  2. Click the Run Python File button in VS Code.  Done.

OUTPUT:
  • Java NDS writes ALL its output files to OUTPUT_DIR (D:/X/ND/Files).
    Nothing in that folder is touched or deleted by this script.
  • The generated PDF(s) are moved to the element's pdf/ folder.
"""

import glob
import os
import shutil
import subprocess
import time
from pathlib import Path


# =============================================================================
# CONFIG — edit these three lines, then run
# =============================================================================

ELEMENT = "Cl"   # Element symbol, e.g. "Cl", "S", "Ar", "Si"
MASS    = 35     # Mass number, e.g. 34, 35, 36, 60

# FILES: None  → convert ALL .ens files for the element
#        list  → convert only the named datasets (without .ens extension)
# Example: FILES = ["Cl35_34s_p_g", "Cl35_adopted"]
FILES = None

# =============================================================================
# PATHS — adjust only if your folder layout is different
# =============================================================================

ENSDF_ROOT = r"D:\X\ND\ENSDF"
OUTPUT_DIR = r"D:\X\ND\Files"   # Java NDS writes all outputs here; PDFs are moved out afterwards
JAR_GLOB   = r"D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v*.jar"

# =============================================================================
# SCRIPT — no need to edit below this line
# =============================================================================


def find_jar():
    matches = sorted(glob.glob(JAR_GLOB))
    if not matches:
        raise FileNotFoundError(f"No JAR found matching: {JAR_GLOB}")
    return matches[-1]   # pick the latest version


def ens_files_to_convert():
    """Return list of absolute .ens paths based on the CONFIG above."""
    new_dir = Path(ENSDF_ROOT) / f"A{MASS}" / f"{ELEMENT}{MASS}" / "new"
    if not new_dir.exists():
        raise FileNotFoundError(f"new/ folder not found: {new_dir}")

    if FILES is None:
        paths = sorted(new_dir.glob("*.ens"))
    else:
        paths = []
        for name in FILES:
            p = new_dir / f"{name}.ens"
            if not p.exists():
                print(f"  WARNING: {p} not found — skipped")
            else:
                paths.append(p)
    return paths


def pdf_dest_dir():
    """Return (and create if needed) the element's pdf/ folder."""
    d = Path(ENSDF_ROOT) / f"A{MASS}" / f"{ELEMENT}{MASS}" / "pdf"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_java(ens_path: Path, jar: str, out_dir: Path) -> Path | None:
    """Step 1 worker: run Java NDS on one .ens file.
    Returns the generated PDF path, or None on failure.
    Does NOT move the file — all moves happen in Step 2 after every
    conversion is finished."""
    pdf_name = ens_path.stem + ".pdf"
    original_cwd = os.getcwd()
    os.chdir(out_dir)
    try:
        subprocess.run(
            ["java", "-jar", jar, str(ens_path.resolve()), pdf_name],
            check=True, timeout=300,
        )
        generated = out_dir / pdf_name
        if generated.exists():
            print(f"  converted  {ens_path.name}")
            return generated
        else:
            print(f"  WARN  PDF not produced for {ens_path.name}")
            return None
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT  {ens_path.name}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"  ERROR  {ens_path.name}: Java exited with code {e.returncode}")
        return None
    finally:
        os.chdir(original_cwd)


def move_all_pdfs(generated: list, dest_dir: Path, max_wait_s: int = 300):
    """Step 2: move every PDF from staging to dest_dir.

    Keeps retrying ALL pending files together (every 1 s) so that as the
    user naturally closes PDF viewer windows the moves happen automatically.
    No window needs to be closed before the next file can be attempted.
    Total patience: max_wait_s seconds (default 5 min).
    """
    pending = list(generated)   # list of (src Path, dst Path)
    start = time.time()

    while pending:
        if time.time() - start > max_wait_s:
            break
        still_locked = []
        for src, dst in pending:
            try:
                shutil.move(str(src), str(dst))
                print(f"  moved  {src.name}  \u2192  {dst.parent}")
            except PermissionError:
                still_locked.append((src, dst))
            except FileNotFoundError:
                print(f"  WARN  {src.name} already gone — skipped")
        pending = still_locked
        if pending:
            time.sleep(1)   # wait 1 s then re-try all remaining files

    if pending:
        print(f"\n  WARNING: {len(pending)} PDF(s) still locked after {max_wait_s} s"
              f" (close their viewer windows and re-run Step 2 manually if needed):")
        for src, _ in pending:
            print(f"    {src}")



def main():
    jar      = find_jar()
    out_dir  = Path(OUTPUT_DIR)
    dest_dir = pdf_dest_dir()

    print(f"JAR  : {jar}")
    print(f"Stage: {out_dir}")
    print(f"PDF  : {dest_dir}")

    files = ens_files_to_convert()
    if not files:
        print("No .ens files to convert.")
        return

    # ── Step 1: convert ALL files first ──────────────────────────────────────
    # Every Java process runs to completion before we touch any PDF.
    # Java may open a PDF viewer window; users can close them at any time —
    # no window interaction is required to proceed.
    print(f"\nStep 1 — converting {len(files)} file(s) for {ELEMENT}{MASS}:")
    generated = []   # list of (src_pdf_in_stage, dst_pdf_in_pdf_folder)
    for ens in files:
        pdf = run_java(ens, jar, out_dir)
        if pdf is not None:
            generated.append((pdf, dest_dir / pdf.name))

    # ── Step 2: move ALL produced PDFs at once ────────────────────────────────
    # Loops over all pending files every 1 s.  As the user closes PDF viewer
    # windows the moves happen automatically — no specific order required.
    print(f"\nStep 2 — moving {len(generated)} PDF(s) to {dest_dir}:")
    move_all_pdfs(generated, dest_dir)

    moved = sum(1 for _, dst in generated if dst.exists())
    print(f"\nDone. {moved}/{len(files)} PDF(s) in {dest_dir}")




if __name__ == "__main__":
    main()


