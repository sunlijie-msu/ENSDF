import json
import sys
import re

def load_json_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r', encoding='utf-16') as f:
        return json.load(f)

def find_closest_level(energy, data, tolerance=5.0):
    """
    Finds the closest level in the data within a given tolerance.

    Args:
        energy (float): The energy to search for.
        data (dict): The reference data to search in.
        tolerance (float): The maximum allowed energy difference.

    Returns:
        tuple: A tuple containing the found energy (str) and its data, or (None, None).
    """
    closest_energy_key = None
    min_diff = float('inf')

    for ref_energy_str, level_data in data.items():
        try:
            ref_energy = float(ref_energy_str)
            diff = abs(energy - ref_energy)
            if diff < min_diff:
                min_diff = diff
                closest_energy_key = ref_energy_str
        except ValueError:
            continue

    if closest_energy_key and min_diff <= tolerance:
        return closest_energy_key, data[closest_energy_key]
    
    return None, None


def verify_ensdf_levels(main_ens_file, go16_data, se09_data):
    """
    Verifies the energy levels in the main ENSDF file against reference data.

    Args:
        main_ens_file (str): Path to the main ENSDF file to verify.
        go16_data (dict): Parsed level data from 1973GO16.
        se09_data (dict): Parsed level data from 2019SE09.
    """
    discrepancies = []
    with open(main_ens_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
                try:
                    energy_str = line[9:19].strip()
                    uncertainty_str = line[19:22].strip()
                    flag = line[76:77].strip()

                    if not energy_str:
                        continue

                    energy = float(energy_str)
                    
                    # Check for special comments on the next line(s) that explain the origin
                    is_special_case = False
                    for j in range(1, 4): # Check next 3 lines
                        if i + j < len(lines):
                            next_line = lines[i+j].upper()
                            # Comments indicating a special case that should be skipped by this script
                            if "CL CL E$" in next_line or "CL2CL" in next_line:
                                if "WEIGHTED AVERAGE" in next_line or \
                                   "QUOTED FROM" in next_line or \
                                   "OTHER:" in next_line or \
                                   "FROM 2019SE09" in next_line or \
                                   "TENTATIVE LEVEL" in next_line:
                                    is_special_case = True
                                    break
                    
                    if is_special_case:
                        continue

                    if flag == 'K':
                        # Check against 2019SE09 data
                        found_key, found_level = find_closest_level(energy, se09_data)
                        if not found_level:
                            discrepancies.append(f"Discrepancy at line {i+1}: Level {energy_str} with flag 'K' not found in 2019SE09 data.")
                        else:
                            ref_unc = found_level.get('uncertainty', '')
                            # Allow for empty uncertainty in reference
                            if uncertainty_str != ref_unc and ref_unc != '':
                                discrepancies.append(f"Discrepancy at line {i+1}: Level {energy_str} (found as {found_key}) with flag 'K' has uncertainty '{uncertainty_str}' but should be '{ref_unc}' from 2019SE09.")
                    else:
                        # Check against 1973GO16 data
                        found_key, found_level = find_closest_level(energy, go16_data)
                        if not found_level:
                            discrepancies.append(f"Discrepancy at line {i+1}: Level {energy_str} (no 'K' flag) not found in 1973GO16 data.")
                        else:
                            ref_unc = found_level.get('uncertainty', '')
                            # Allow for empty uncertainty in reference
                            if uncertainty_str != ref_unc and ref_unc != '':
                                discrepancies.append(f"Discrepancy at line {i+1}: Level {energy_str} (found as {found_key}) (no 'K' flag) has uncertainty '{uncertainty_str}' but should be '{ref_unc}' from 1973GO16.")

                except (ValueError, IndexError) as e:
                    # This should now only catch actual parsing errors on L-records
                    discrepancies.append(f"Could not parse L-record at line {i+1}: {line.strip()} - Error: {e}")

    return discrepancies

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python verify_levels.py <main_ens_file> <go16_json> <se09_json>")
        sys.exit(1)

    main_file = sys.argv[1]
    go16_json_file = sys.argv[2]
    se09_json_file = sys.argv[3]

    try:
        go16_data = load_json_data(go16_json_file)
        se09_data = load_json_data(se09_json_file)
        
        all_discrepancies = verify_ensdf_levels(main_file, go16_data, se09_data)

        if all_discrepancies:
            print("Verification found the following issues:")
            for d in all_discrepancies:
                print(d)
        else:
            print("Verification complete. No discrepancies found.")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
