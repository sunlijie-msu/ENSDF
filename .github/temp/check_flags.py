
import sys

def check_ensdf_flags(file_path):
    levels_with_x = []
    gammas_with_x = []
    
    with open(file_path, 'r') as f:
        for line in f:
            if len(line) < 80:
                continue
            
            # Record type in col 8
            rec_type = line[7]
            # Flag in col 77 (index 76)
            flag = line[76]
            
            if flag == 'X':
                # Energy is in cols 10-19 (index 9-19)
                energy = line[9:19].strip()
                if rec_type == 'L':
                    levels_with_x.append(energy)
                elif rec_type == 'G':
                    gammas_with_x.append(energy)
                    
    return levels_with_x, gammas_with_x

file_path = "XUNDL/2026WIAA_CN10950_32P.ens"
levels, gammas = check_ensdf_flags(file_path)

print("Levels with 'X':", levels)
print("Count:", len(levels))
print("\nGammas with 'X':", gammas)
print("Count:", len(gammas))
