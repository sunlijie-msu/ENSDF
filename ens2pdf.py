import os
import subprocess
from pathlib import Path
import glob
import sys


def generate_pdfs(element):
    os.chdir("D:/X/ND/Files")
    
    # Find JAR file automatically
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Process all .ens files for the element
    for ens_file_path in glob.glob(f"D:/X/ND/A35/finished/{element}35/new/*.ens"):
        pdf_file = f"{Path(ens_file_path).stem}.pdf"
        subprocess.run(["java", "-jar", jar_file, ens_file_path, pdf_file])
        print(f"Converted: {Path(ens_file_path).name} -> {pdf_file}")

# Even simpler - single file
def generate_pdf(element, dataset_name):
    os.chdir("D:/X/ND/Files")
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    ens_file = f"D:/X/ND/A35/finished/{element}35/new/{dataset_name}.ens"
    pdf_file = f"{dataset_name}.pdf"
    subprocess.run(["java", "-jar", jar_file, ens_file, pdf_file])
    print(f"Converted: {dataset_name}.ens -> {dataset_name}.pdf")

def generate_pdfs_pattern(element, pattern):
    """Convert files matching a pattern (e.g., '*sig' for files ending with 'sig')"""
    os.chdir("D:/X/ND/Files")
    jar_file = glob.glob("D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar")[0]
    
    # Process files matching the pattern
    for ens_file_path in glob.glob(f"D:/X/ND/A35/finished/{element}35/new/{pattern}.ens"):
        pdf_file = f"{Path(ens_file_path).stem}.pdf"
        subprocess.run(["java", "-jar", jar_file, ens_file_path, pdf_file])
        print(f"Converted: {Path(ens_file_path).name} -> {pdf_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ens2pdf.py Si                    # Convert all Si35 files")
        print("  python ens2pdf.py Si35_adopted          # Convert single file")
        print("  python ens2pdf.py Si35_*sig             # Convert pattern")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    # Check if it's just an element (like "Si")
    if len(arg) <= 2 and arg.isalpha():
        print(f"Converting all {arg}35 files...")
        generate_pdfs(arg)
    
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
        generate_pdfs_pattern(element, arg)
    
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
        generate_pdf(element, arg)