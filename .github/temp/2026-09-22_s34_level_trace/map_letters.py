import sys
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import letter_to_file
for k in "FLQWNT":
    print(k, "->", letter_to_file.get(k))
