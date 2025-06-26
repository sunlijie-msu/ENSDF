import os
import subprocess
from pathlib import Path
import glob
import sys
import platform


def open_pdf(pdf_path, use_vscode=True):
    """Open PDF in VS Code or default system viewer"""
    if use_vscode:
        try:
            subprocess.run(["code", pdf_path], check=True)
            print(f"Opened {os.path.basename(pdf_path)} in VS Code")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("VS Code command not found, opening in system viewer instead...")
            use_vscode = False
    
    if not use_vscode:
        if platform.system() == "Windows":
            os.startfile(pdf_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", pdf_path])
        else:  # Linux
            subprocess.run(["xdg-open", pdf_path])
        print(f"Opened {os.path.basename(pdf_path)} in system viewer")


def generate_pdfs(element, open_after=False, use_vscode=True):
    os.chdir("D:/X/ND/Files")
    
    # Find JAR file automatically
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Process all .ens files for the element
    for ens_file_path in glob.glob(f"D:/X/ND/A35/finished/{element}35/new/*.ens"):
        pdf_file = f"{Path(ens_file_path).stem}.pdf"
        subprocess.run(["java", "-jar", jar_file, ens_file_path, pdf_file])
        print(f"Converted: {Path(ens_file_path).name} -> {pdf_file}")
        if open_after:
            # PDF is always generated in D:/X/ND/Files
            pdf_path = f"D:/X/ND/Files/{Path(ens_file_path).stem}.pdf"
            open_pdf(pdf_path, use_vscode)

# Even simpler - single file
def generate_pdf(element, dataset_name, open_after=False, use_vscode=True):
    os.chdir("D:/X/ND/Files")
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    ens_file = f"D:/X/ND/A35/finished/{element}35/new/{dataset_name}.ens"
    pdf_file = f"{dataset_name}.pdf"
    subprocess.run(["java", "-jar", jar_file, ens_file, pdf_file])
    print(f"Converted: {dataset_name}.ens -> {dataset_name}.pdf")
    if open_after:
        # PDF is always generated in D:/X/ND/Files
        pdf_path = f"D:/X/ND/Files/{dataset_name}.pdf"
        open_pdf(pdf_path, use_vscode)

# Handle full file paths
def generate_pdf_from_path(file_path, open_after=False, use_vscode=True):
    """Convert a single ENSDF file given its full path"""
    # Normalize path and get absolute path BEFORE changing directory
    file_path = os.path.normpath(file_path)
    ens_file = os.path.abspath(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    os.chdir("D:/X/ND/Files")
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    pdf_file = f"{base_name}.pdf"
    
    # Extract element from filename
    element = ""
    for c in base_name:
        if c.isdigit():
            break
        if c.isalpha():
            element += c
    
    subprocess.run(["java", "-jar", jar_file, ens_file, pdf_file])
    print(f"Converted: {file_path} -> {base_name}.pdf")
    
    if open_after:
        # PDF is always generated in D:/X/ND/Files
        pdf_path = f"D:/X/ND/Files/{base_name}.pdf"
        open_pdf(pdf_path, use_vscode)

def generate_pdfs_pattern(element, pattern, open_after=False, use_vscode=True):
    """Convert files matching a pattern (e.g., '*sig' for files ending with 'sig')"""
    os.chdir("D:/X/ND/Files")
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Process files matching the pattern
    for ens_file_path in glob.glob(f"D:/X/ND/A35/finished/{element}35/new/{pattern}.ens"):
        pdf_file = f"{Path(ens_file_path).stem}.pdf"
        subprocess.run(["java", "-jar", jar_file, ens_file_path, pdf_file])
        print(f"Converted: {Path(ens_file_path).name} -> {pdf_file}")
        if open_after:
            # PDF is always generated in D:/X/ND/Files
            pdf_path = f"D:/X/ND/Files/{Path(ens_file_path).stem}.pdf"
            open_pdf(pdf_path, use_vscode)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ens2pdf.py Si                                    # Convert all Si35 files")
        print("  python ens2pdf.py Si35_adopted                          # Convert single file")
        print("  python ens2pdf.py Si35_*sig                             # Convert pattern")
        print("  python ens2pdf.py finished/Si35/new/Si35_adopted.ens    # Convert with full path")
        print("  python ens2pdf.py Si --open                             # Convert and open in VS Code")
        print("  python ens2pdf.py Si --open --system                    # Convert and open in system viewer")
        sys.exit(1)
    
    # Check for flags
    open_after = "--open" in sys.argv
    use_system = "--system" in sys.argv
    
    if open_after:
        sys.argv.remove("--open")
    if use_system:
        sys.argv.remove("--system")
    
    use_vscode = not use_system  # Default to VS Code unless --system is specified
    
    arg = sys.argv[1]
    
    # Check if it's a full file path
    if (os.path.sep in arg or '/' in arg) and arg.endswith('.ens'):
        print(f"Converting single file: {arg}")
        generate_pdf_from_path(arg, open_after, use_vscode)
    
    # Check if it's just an element (like "Si")
    elif len(arg) <= 2 and arg.isalpha():
        print(f"Converting all {arg}35 files...")
        generate_pdfs(arg, open_after, use_vscode)
    
    # Check if it contains wildcards
    elif '*' in arg or '?' in arg:
        # Extract element (letters before first digit)
        element = ""
        for c in arg:
            if c.isdigit():
                break
            if c.isalpha():
                element += c
        print(f"Converting {element}35 files matching pattern: {arg}")
        generate_pdfs_pattern(element, arg, open_after, use_vscode)
    
    # Single file
    else:
        # Extract element (letters before first digit)
        element = ""
        for c in arg:
            if c.isdigit():
                break
            if c.isalpha():
                element += c
        print(f"Converting single file: {arg}")
        generate_pdf(element, arg, open_after, use_vscode)
