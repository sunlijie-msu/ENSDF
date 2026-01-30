
import sys
import re

def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    l_records_info = {}
    current_l_index = -1
    
    # Regex STRICTLY matches "$Band X ->"
    band_pattern = re.compile(r'\$Band\s+(\d+)\s+->')

    for i, line in enumerate(lines):
        if len(line) < 8:
            continue
            
        # Check chars at specific columns
        # Col 7 (index 6)
        # Col 8 (index 7)
        
        col7 = line[6]
        col8 = line[7]
        
        if col8 == 'L' and col7 == ' ':
            # L-Record found
            # (Note: Col 6 (index 5) is continuation, normally space for start of level)
            current_l_index = i
            l_records_info[current_l_index] = set()
            continue
            
        if col8 == 'G' and col7 in ['c', 'C']:
            # cG Record found
            if current_l_index != -1:
                # Parse
                # Text starts at Col 10 (index 9) typically for "$"
                # But allow for scanning whole line after index 8
                text = line[8:]
                match = band_pattern.search(text)
                if match:
                    band_num = match.group(1)
                    l_records_info[current_l_index].add(band_num)
                    # print(f"Found Band {band_num} for L-record at {current_l_index+1}")
    
    band_map = {
        '7': 'D',
        '8': 'd',
        '9': 'E',
        '10': 'e'
    }
    
    modifications = 0
    
    for idx, bands in l_records_info.items():
        if len(bands) == 1:
            band = list(bands)[0]
            if band in band_map:
                flag = band_map[band]
                line = lines[idx]
                
                # Check line length and pad
                line = line.rstrip('\r\n')
                line = line.ljust(80)
                
                # Col 77 is index 76
                existing_flag = line[76]
                
                if existing_flag == flag:
                    # Already set, skip writing to avoid unnecessary IO/logs
                    continue
                
                if existing_flag != ' ':
                    print(f"Warning: Line {idx+1} has flag '{existing_flag}'. Replacing with '{flag}'.")
                    
                line_list = list(line)
                line_list[76] = flag
                new_line = "".join(line_list) + '\n'
                
                lines[idx] = new_line
                modifications += 1
                print(f"Updated L-record at line {idx+1}: Band {band} -> Flag {flag}")
                
        elif len(bands) > 1:
            print(f"Skipping Line {idx+1}: Ambiguous bands {bands}")
            
    if modifications > 0:
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(f"Total L-records updated: {modifications}")
    else:
        print("No modifications needed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_band_flags.py <file_path>")
        sys.exit(1)
    
    process_file(sys.argv[1])
