import sys
import os

def check_lengths(filepath):
    errors = 0
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            # Strip newline characters for length check
            l = line.rstrip('\n\r')
            if len(l) != 80:
                print(f"Error: Line {i+1} has length {len(l)} (expected 80)")
                print(f"Content: '{l}'")
                errors += 1
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_all_lengths.py <filepath>")
    else:
        errs = check_lengths(sys.argv[1])
        if errs == 0:
            print("All lines are exactly 80 characters.")
        else:
            print(f"Total errors: {errs}")
