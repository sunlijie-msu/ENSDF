import json
import sys

def parse_ensdf_levels(file_path):
    """
    Parses an ENSDF file and extracts level energies and uncertainties.

    Args:
        file_path (str): The path to the ENSDF file.

    Returns:
        dict: A dictionary where keys are level energies (as strings)
              and values are their uncertainties (as strings).
    """
    levels = {}
    with open(file_path, 'r') as f:
        for line in f:
            if len(line) >= 80 and line[7] == 'L':
                try:
                    energy_str = line[9:19].strip()
                    uncertainty_str = line[19:22].strip()
                    if energy_str:
                        energy = float(energy_str)
                        levels[energy] = {
                            "uncertainty": uncertainty_str,
                            "original_line": line.strip()
                        }
                except (ValueError, IndexError):
                    # Ignore lines that cannot be parsed
                    pass
    return levels

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_ens_levels.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        level_data = parse_ensdf_levels(file_path)
        print(json.dumps(level_data, indent=4))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
