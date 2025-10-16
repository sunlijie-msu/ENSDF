import os
import subprocess
import sys
import platform
import shutil
import glob
from pathlib import Path

# Auto-discover latest FormatCheck jar (like ens2pdf.py)
def find_latest_jar() -> str | None:
    candidates = glob.glob(r"D:\\X\\ND\\FormatCheck\\FormatCheck_*.jar")
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]
FILES_DIR = r"D:\X\ND\Files"
OUTPUT_FILE = Path(FILES_DIR) / "formatcheck.fmt"

def open_file(path: str, use_vscode: bool = True) -> None:
    """Open a file in VS Code or default system viewer."""
    if use_vscode:
        try:
            subprocess.run(["code", path], check=True)
            print(f"Opened {os.path.basename(path)} in VS Code")
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("VS Code CLI not available, opening in system viewer...")
    # Fallback to system viewer
    if platform.system() == "Windows":
        os.startfile(path)  # type: ignore[attr-defined]
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])
    print(f"Opened {os.path.basename(path)} in system viewer")

def run_formatcheck(ens_path: str, open_after: bool = False, use_vscode: bool = True) -> int:
    """Run the Java FormatCheck tool on the given ENSDF file.

    Generates D:\\X\\ND\\Files\\formatcheck.fmt
    Returns process return code (0 on success).
    """
    # Validate inputs
    ens_abs = os.path.abspath(os.path.normpath(ens_path))
    if not os.path.exists(ens_abs):
        print(f"Error: ENSDF file not found: {ens_abs}")
        return 1
    jar_path = find_latest_jar()
    if not jar_path or not os.path.exists(jar_path):
        print("Error: Could not find FormatCheck jar. Looked for 'D:/X/ND/FormatCheck/FormatCheck_*.jar'")
        return 1

    # Prepare output location
    os.makedirs(FILES_DIR, exist_ok=True)
    # Remove previous output to avoid confusion
    try:
        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()
    except Exception as e:
        print(f"Warning: Could not remove previous output: {e}")

    # Run tool (jar writes report where it decides; observed path is alongside input file)
    cmd = ["java", "-jar", jar_path, ens_abs]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd)

    # The Java tool typically writes report next to the input as 'formatcheck.fmt'
    probable_src = Path(ens_abs).parent / "formatcheck.fmt"

    rc = result.returncode
    if rc != 0:
        print(f"Note: FormatCheck exited with code {rc}. Proceeding to check for report file.")

    # Prefer the file in Files dir if already created; otherwise move/copy from source
    if OUTPUT_FILE.exists():
        pass
    elif probable_src.exists():
        try:
            # Move to Files location (overwrite if exists)
            shutil.move(str(probable_src), str(OUTPUT_FILE))
        except Exception:
            # Fallback: copy if move fails (e.g., across volumes)
            shutil.copy2(str(probable_src), str(OUTPUT_FILE))
            try:
                probable_src.unlink()
            except Exception:
                pass

    if OUTPUT_FILE.exists():
        print(f"Report available at: {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} bytes)")
        if open_after:
            open_file(str(OUTPUT_FILE), use_vscode)
        # Treat existence of the report as success
        return 0
    else:
        print("Error: Report not found. Checked:")
        print(f" - {OUTPUT_FILE}")
        print(f" - {probable_src}")
        return 2


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage:")
        print("  python .github/Java_FormatCheck.py <path-to-file>.ens [--open] [--system]")
        print("Notes:")
        print("  - Output is written to D:/X/ND/Files/formatcheck.fmt")
        return 1

    open_after = "--open" in argv
    use_system = "--system" in argv

    args = [a for a in argv[1:] if a not in ("--open", "--system")]
    if not args:
        print("Error: Missing ENSDF file path")
        return 1

    ens = args[0]
    use_vscode = not use_system

    return run_formatcheck(ens, open_after=open_after, use_vscode=use_vscode)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
