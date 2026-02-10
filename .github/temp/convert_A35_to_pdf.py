import os
import subprocess
import glob
from pathlib import Path

def convert_a35_pdft():
    # Configuration
    ensdf_root = Path("D:/X/ND/ENSDF/A35")
    jar_pattern = "D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v*.jar"
    
    # Find JAR file
    jar_files = glob.glob(jar_pattern)
    if not jar_files:
        print("Error: McMaster Java JAR not found.")
        return
    jar_file = jar_files[0]
    print(f"Using JAR: {jar_file}")

    # Iterate over element directories in A35
    for element_dir in ensdf_root.iterdir():
        if not element_dir.is_dir():
            continue
            
        # Check for 'new' directory containing .ens files
        new_dir = element_dir / "new"
        if not new_dir.exists():
            continue
            
        ens_files = list(new_dir.glob("*.ens"))
        if not ens_files:
            continue
            
        # Ensure 'pdf' directory exists
        pdf_dir = element_dir / "pdf"
        pdf_dir.mkdir(exist_ok=True)
        
        print(f"Processing {element_dir.name}...")
        
        # Change to pdf directory to avoid path issues with the Java tool
        original_cwd = os.getcwd()
        os.chdir(pdf_dir)
        
        try:
            for ens_file in ens_files:
                output_pdf_name = f"{ens_file.stem}.pdf"
                
                # Command: java -jar <jar> <absolute_input.ens> <output_filename.pdf>
                cmd = ["java", "-jar", str(jar_file), str(ens_file), output_pdf_name]
                print(f"  Converting: {ens_file.name}")
                
                try:
                    # Timeout of 180 seconds per file
                    subprocess.run(cmd, check=True, capture_output=True, timeout=180)
                    print(f"  Success: -> {output_pdf_name}")
                except subprocess.TimeoutExpired:
                     print(f"  TIMEOUT: {ens_file.name}")
                except subprocess.CalledProcessError as e:
                    print(f"  FAILED: {ens_file.name}")
                    # Handle potential None if capture failed differently
                    err_msg = e.stderr.decode() if e.stderr else "No stderr captured"
                    print(f"  Error: {err_msg}")
        finally:
            os.chdir(original_cwd)

if __name__ == "__main__":
    print("Starting conversion script...")
    convert_a35_pdft()
