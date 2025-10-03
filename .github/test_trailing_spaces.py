#!/usr/bin/env python3
"""Test if trailing spaces are preserved when writing to files."""

import os

# Create test line with trailing spaces
test_line = "TEST" + (" " * 76)  # 80 characters total
print(f"Original line length: {len(test_line)}")
print(f"Original line repr: {repr(test_line)}")

# Write to file
test_file = os.path.join('A35', 'Cl35', 'temp', 'test_80char.txt')
with open(test_file, 'w') as f:
    f.write(test_line + '\n')

# Read back
with open(test_file, 'r') as f:
    read_back = f.readline()

print(f"\nRead back line length (with \\n): {len(read_back)}")
print(f"Read back line length (stripped): {len(read_back.rstrip())}")
print(f"Read back repr: {repr(read_back)}")

# Check if trailing spaces preserved
if len(read_back.rstrip('\n')) == 80:
    print("\n[OK] SUCCESS: Trailing spaces preserved!")
else:
    print(f"\n[ERROR] FAIL: Expected 80 chars, got {len(read_back.rstrip(chr(10)))}")
