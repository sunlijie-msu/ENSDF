import os
import subprocess
from pathlib import Path
import glob
import sys
import platform
import re


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


def cleanup_files(directory):
    """Remove non-PDF files from the directory"""
    for file_path in glob.glob(os.path.join(directory, "*")):
        if not file_path.lower().endswith(".pdf"):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                     # Optional: remove directories if necessary, but risky. 
                     # The Java tool generates files, not dirs usually.
                     pass 
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")

def get_pdf_dir(ens_file_path):
    """Get the local pdf directory for an ens file path"""
    # Assuming structure .../{element_dir}/new/{file}.ens
    # We want .../{element_dir}/pdf/
    
    # Check if 'new' is in path
    ens_path = Path(ens_file_path)
    if ens_path.parent.name == "new":
        pdf_dir = ens_path.parent.parent / "pdf"
        pdf_dir.mkdir(exist_ok=True)
        return pdf_dir
    else:
        # If structure is different, default to a 'pdf' folder in the same dir
        pdf_dir = ens_path.parent / "pdf"
        pdf_dir.mkdir(exist_ok=True)
        return pdf_dir

def generate_pdfs(element, open_after=False, use_vscode=True):
    # Find JAR file automatically
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Search in current ENSDF workspace for multiple mass chains
    mass_chains = ["A34", "A35", "A60"]
    total_files = 0
    
    for mass_chain in mass_chains:
        mass_number = mass_chain[1:]  # Extract number (34, 35, 60)
        ens_path = f"D:/X/ND/ENSDF/{mass_chain}/{element}{mass_number}/new/*.ens"
        ens_files = glob.glob(ens_path)
        
        if ens_files:
            print(f"Found {len(ens_files)} files in {mass_chain}/{element}{mass_number}/new/")
            total_files += len(ens_files)
            
            # Group by directory to minimize CWD changes (though glob is specific here)
            # Process all .ens files for the element
            for ens_file_path in ens_files:
                pdf_dir = get_pdf_dir(ens_file_path)
                pdf_filename = f"{Path(ens_file_path).stem}.pdf"
                
                # Change CWD to target PDF dir
                original_cwd = os.getcwd()
                os.chdir(pdf_dir)
                
                try:
                    subprocess.run(["java", "-jar", jar_file, ens_file_path, pdf_filename], check=True, timeout=180)
                    print(f"Converted: {Path(ens_file_path).name} -> {pdf_dir / pdf_filename}")
                    
                    # Cleanup
                    cleanup_files(pdf_dir)
                    
                    if open_after:
                        open_pdf(str(pdf_dir / pdf_filename), use_vscode)
                except subprocess.TimeoutExpired:
                     print(f"TIMEOUT processing {Path(ens_file_path).name}")
                except Exception as e:
                     print(f"Error processing {Path(ens_file_path).name}: {e}")
                finally:
                    os.chdir(original_cwd)
    
    if total_files == 0:
        print(f"No {element} .ens files found in ENSDF workspace (searched A34, A35, A60)")

# Even simpler - single file
def generate_pdf(element, dataset_name, open_after=False, use_vscode=True):
    # Find JAR file automatically
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Extract mass number from dataset name if present
    mass_number = "35"  # default
    for char in dataset_name:
        if char.isdigit():
            # Find consecutive digits
            mass_start = dataset_name.index(char)
            mass_end = mass_start
            while mass_end < len(dataset_name) and dataset_name[mass_end].isdigit():
                mass_end += 1
            mass_number = dataset_name[mass_start:mass_end]
            break
    
    # Search in current ENSDF workspace
    ens_file = f"D:/X/ND/ENSDF/A{mass_number}/{element}{mass_number}/new/{dataset_name}.ens"
    
    if not os.path.exists(ens_file):
        print(f"Error: {dataset_name}.ens not found in ENSDF workspace: A{mass_number}/{element}{mass_number}/new/")
        return
    
    pdf_dir = get_pdf_dir(ens_file)
    pdf_filename = f"{dataset_name}.pdf"
    
    original_cwd = os.getcwd()
    os.chdir(pdf_dir)
    
    try:
        subprocess.run(["java", "-jar", jar_file, ens_file, pdf_filename], check=True, timeout=180)
        print(f"Converted: {dataset_name}.ens -> {pdf_dir / pdf_filename}")
        cleanup_files(pdf_dir)
        
        if open_after:
            open_pdf(str(pdf_dir / pdf_filename), use_vscode)
    except Exception as e:
        print(f"Error converting {dataset_name}: {e}")
    finally:
        os.chdir(original_cwd)

# Handle full file paths
def generate_pdf_from_path(file_path, open_after=False, use_vscode=True):
    """Convert a single ENSDF file given its full path"""
    # Normalize path and get absolute path BEFORE changing directory
    file_path = os.path.normpath(file_path)
    ens_file = os.path.abspath(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Find JAR file automatically
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    pdf_dir = get_pdf_dir(ens_file)
    pdf_filename = f"{base_name}.pdf"
    
    original_cwd = os.getcwd()
    os.chdir(pdf_dir)
    
    try:
        subprocess.run(["java", "-jar", jar_file, ens_file, pdf_filename], check=True, timeout=180)
        print(f"Converted: {file_path} -> {pdf_dir / pdf_filename}")
        cleanup_files(pdf_dir)
        
        if open_after:
            open_pdf(str(pdf_dir / pdf_filename), use_vscode)
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
    finally:
        os.chdir(original_cwd)

def generate_pdfs_pattern(element, pattern, open_after=False, use_vscode=True):
    """Convert files matching a pattern (e.g., '*sig' for files ending with 'sig')"""
    # Find JAR file automatically
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Extract mass number from pattern if present, otherwise try all mass chains
    mass_number = None
    for char in pattern:
        if char.isdigit():
            # Find consecutive digits
            mass_start = pattern.index(char)
            mass_end = mass_start
            while mass_end < len(pattern) and pattern[mass_end].isdigit():
                mass_end += 1
            mass_number = pattern[mass_start:mass_end]
            break
    
    mass_chains = [f"A{mass_number}"] if mass_number else ["A34", "A35", "A60"]
    total_files = 0
    
    for mass_chain in mass_chains:
        mass_num = mass_chain[1:]  # Extract number (34, 35, 60)
        pattern_path = f"D:/X/ND/ENSDF/{mass_chain}/{element}{mass_num}/new/{pattern}.ens"
        ens_files = glob.glob(pattern_path)
        
        if ens_files:
            print(f"Found {len(ens_files)} files matching pattern '{pattern}' in {mass_chain}/{element}{mass_num}/new/")
            total_files += len(ens_files)
            # Process files matching the pattern
            for ens_file_path in ens_files:
                pdf_dir = get_pdf_dir(ens_file_path)
                pdf_filename = f"{Path(ens_file_path).stem}.pdf"
                
                original_cwd = os.getcwd()
                os.chdir(pdf_dir)
                
                try:
                    subprocess.run(["java", "-jar", jar_file, ens_file_path, pdf_filename], check=True, timeout=180)
                    print(f"Converted: {Path(ens_file_path).name} -> {pdf_dir / pdf_filename}")
                    cleanup_files(pdf_dir)
                    
                    if open_after:
                        open_pdf(str(pdf_dir / pdf_filename), use_vscode)
                except Exception as e:
                    print(f"Error processing {Path(ens_file_path).name}: {e}")
                finally:
                    os.chdir(original_cwd)
    
    if total_files == 0:
        print(f"No files matching pattern '{pattern}' found in ENSDF workspace")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ens2pdf.py Ar34                                  # Convert all Ar34 files")
        print("  python ens2pdf.py 34Ar                                  # Same as above (alternate format)")
        print("  python ens2pdf.py S35_adopted                           # Convert single file")
        print("  python ens2pdf.py S35_*sig                              # Convert pattern")
        print("  python ens2pdf.py A35/S35/new/S35_adopted.ens           # Convert with full path")
        print("  python ens2pdf.py Ar34 --open                           # Convert and open in VS Code")
        print("  python ens2pdf.py Ar34 --open --system                  # Convert and open in system viewer")
        print("  Note: Files are searched in ENSDF workspace (A34, A35, A60 mass chains)")
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
    
    # Check if it's an element+mass pattern like "Ar34" or "Si35" (convert ALL files for that isotope)
    elif re.match(r'^[A-Z][a-z]?\d+$', arg):
        # Extract element and mass
        match = re.match(r'^([A-Z][a-z]?)(\d+)$', arg)
        element = match.group(1)
        mass = match.group(2)
        pattern = f"{element}{mass}_*"
        print(f"Converting all {element}{mass} files (pattern: {pattern})...")
        generate_pdfs_pattern(element, pattern, open_after, use_vscode)
    
    # Check if it's mass+element pattern like "34Ar" or "35Si" (alternate user input style)
    elif re.match(r'^\d+[A-Z][a-z]?$', arg):
        # Extract mass and element
        match = re.match(r'^(\d+)([A-Z][a-z]?)$', arg)
        mass = match.group(1)
        element = match.group(2)
        pattern = f"{element}{mass}_*"
        print(f"Converting all {element}{mass} files (pattern: {pattern})...")
        generate_pdfs_pattern(element, pattern, open_after, use_vscode)
    
    # Check if it contains wildcards
    elif '*' in arg or '?' in arg:
        # Extract element (letters before first digit)
        element = ""
        for c in arg:
            if c.isdigit():
                break
            if c.isalpha():
                element += c
        print(f"Converting files matching pattern: {arg}")
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
