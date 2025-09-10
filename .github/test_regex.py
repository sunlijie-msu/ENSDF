#!/usr/bin/env python3
"""
Test specific lifetime lines to understand the format
"""

def test_lifetime_regex():
    # Test sample from the ENSDF file
    sample_lines = [
        "127I  cL T$|t{-Ave}=1.42 ps {I+10-11}. |t{-GTA}=1.42 ps {I+10-11}.",
        "127I  cL T$|t{-Ave}=2.41 ps {I+27-33}. |t{-GTA}=2.41 ps {I+27-33}.",
        "127I  cL T$|t{-Ave}=0.91 ps {I+11-11}. |t{-GTA}=1.10 ps {I+8-9}. |t{-GTB}=0.71",
        "127I 2cL ps {I+8-7}.",
        "127I  cL T$|t{-Ave}=0.79 ps {I+6-9}. |t{-GTA}=0.86 ps {I+5-7}. |t{-GTB}=0.72 ps",
        "127I 2cL {I+3-6}.",
        "127I  cL T$|t{-Ave}=1.34 ps {I+17-20}. |t{-GTB}=1.34 ps {I+17-20}.",
        "127I  cL T$|t{-Ave}=1.01 ps {I+12-14}. |t{-GTA}=0.88 ps {I+7-7}. |t{-GTB}=1.14",
        "127I 2cL ps {I+10-12}.",
    ]
    
    import re
    
    tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
    
    for line in sample_lines:
        print(f"Line: {line}")
        matches = re.findall(tau_pattern, line)
        print(f"Matches: {matches}")
        print()

if __name__ == "__main__":
    test_lifetime_regex()
