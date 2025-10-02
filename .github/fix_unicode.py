#!/usr/bin/env python3
"""Fix Unicode emoji characters in Python scripts for PowerShell compatibility."""

import sys

# Read file
with open('.github/column_calibrate.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Unicode characters with ASCII equivalents
replacements = {
    '✅': '[OK]',
    '❌': '[ERROR]',
    '⚠️': '[WARNING]',
    '✓': '[OK]'
}

original_content = content
for unicode_char, ascii_equiv in replacements.items():
    content = content.replace(unicode_char, ascii_equiv)

# Write back
with open('.github/column_calibrate.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Report
count = sum(original_content.count(char) for char in replacements.keys())
print(f"SUCCESS: Replaced {count} Unicode symbols with ASCII equivalents")
print("Replacements made:")
for unicode_char, ascii_equiv in replacements.items():
    count = original_content.count(unicode_char)
    if count > 0:
        print(f"  {unicode_char} -> {ascii_equiv} ({count} occurrences)")
