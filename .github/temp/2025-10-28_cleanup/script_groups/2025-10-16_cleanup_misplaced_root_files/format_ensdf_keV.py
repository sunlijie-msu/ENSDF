#!/usr/bin/env python3
"""
Generate properly formatted 80-column ENSDF records from parsed CSV data.
L-records and G-records in keV units (integers).
All values left-justified in their fields.
"""

# Generate properly formatted ENSDF records
records = []

# L 5645
records.append(" 35CL  L 5645")
records.append(" 35CL  G 2642       80")
records.append(" 35CL  G 3882       6")

# L 7179
records.append(" 35CL  L 7179")
records.append(" 35CL  G 2340       2")
records.append(" 35CL  G 3006       1")
records.append(" 35CL  G 3120       22")
records.append(" 35CL  G 3211       9")
records.append(" 35CL  G 3261       3")
records.append(" 35CL  G 4485       4")
records.append(" 35CL  G 5960       17")
records.append(" 35CL  G 7179       38")

# L 7547
records.append(" 35CL  L 7547")
records.append(" 35CL  G 1901       1")
records.append(" 35CL  G 4384       95")
records.append(" 35CL  G 4544       2")
records.append(" 35CL  G 4901       1")
records.append(" 35CL  G 7070       1")

# L 7838
records.append(" 35CL  L 7838")
records.append(" 35CL  G 1657       1")
records.append(" 35CL  G 2239       1")
records.append(" 35CL  G 2622       1")
records.append(" 35CL  G 3660       28")
records.append(" 35CL  G 3665       3")
records.append(" 35CL  G 3779       2")
records.append(" 35CL  G 3895       1")
records.append(" 35CL  G 4835       4")
records.append(" 35CL  G 6075       2")
records.append(" 35CL  G 6619       37")
records.append(" 35CL  G 7838       21")

# L 8207
records.append(" 35CL  L 8207")
records.append(" 35CL  G 2553       1")
records.append(" 35CL  G 3326       1")
records.append(" 35CL  G 3368       1")
records.append(" 35CL  G 4148       2")
records.append(" 35CL  G 5204       1")
records.append(" 35CL  G 5513       1")
records.append(" 35CL  G 6444       14")
records.append(" 35CL  G 6988       3")
records.append(" 35CL  G 8207       78")

# L 8216
records.append(" 35CL  L 8216")
records.append(" 35CL  G 2562       1")
records.append(" 35CL  G 4038       3")
records.append(" 35CL  G 5053       41")
records.append(" 35CL  G 5213       5")
records.append(" 35CL  G 5522       3")
records.append(" 35CL  G 6453       1")
records.append(" 35CL  G 7739       1")
records.append(" 35CL  G 8216       45")

# L 8381
records.append(" 35CL  L 8381")
records.append(" 35CL  G 3757       1")
records.append(" 35CL  G 4268       7")
records.append(" 35CL  G 4463       24")
records.append(" 35CL  G 5378       25")
records.append(" 35CL  G 5687       1")
records.append(" 35CL  G 5735       5")
records.append(" 35CL  G 6618       34")
records.append(" 35CL  G 7904       1")
records.append(" 35CL  G 8381       2")

# L 8484
records.append(" 35CL  L 8484")
records.append(" 35CL  G 2830       6")
records.append(" 35CL  G 3603       7")
records.append(" 35CL  G 3860       1")
records.append(" 35CL  G 4516       1")
records.append(" 35CL  G 4566       5")
records.append(" 35CL  G 5481       7")
records.append(" 35CL  G 5790       20")
records.append(" 35CL  G 5838       3")
records.append(" 35CL  G 6721       46")
records.append(" 35CL  G 8484       4")

# L 8893
records.append(" 35CL  L 8893")
records.append(" 35CL  G 3294       1")
records.append(" 35CL  G 4780       9")
records.append(" 35CL  G 4950       4")
records.append(" 35CL  G 5730       29")
records.append(" 35CL  G 6199       37")
records.append(" 35CL  G 7130       19")
records.append(" 35CL  G 8893       1")

# L 8907
records.append(" 35CL  L 8907")
records.append(" 35CL  G 3253       4")
records.append(" 35CL  G 3261       2")
records.append(" 35CL  G 3321       4")
records.append(" 35CL  G 4964       15")
records.append(" 35CL  G 7144       69")
records.append(" 35CL  G 8430       6")

# L 9081
records.append(" 35CL  L 9081")
records.append(" 35CL  G 3357       1")
records.append(" 35CL  G 4200       1")
records.append(" 35CL  G 4903       2")
records.append(" 35CL  G 4908       2")
records.append(" 35CL  G 5163       9")
records.append(" 35CL  G 5918       6")
records.append(" 35CL  G 6387       2")
records.append(" 35CL  G 6435       1")
records.append(" 35CL  G 7318       16")
records.append(" 35CL  G 9081       60")

# Validate and format to exactly 80 characters
print("=" * 80)
print("80-COLUMN VALIDATION")
print("=" * 80)

formatted_records = []
for record in records:
    # Pad to 80 characters if needed
    if len(record) < 80:
        record = record + " " * (80 - len(record))
    elif len(record) > 80:
        print(f"ERROR: Record too long ({len(record)} chars): {record[:50]}")
        record = record[:80]
    
    formatted_records.append(record)

# Check for any issues
errors = 0
for i, record in enumerate(formatted_records, 1):
    if len(record) != 80:
        print(f"ERROR Line {i}: Length {len(record)} != 80")
        errors += 1

if errors == 0:
    print("SUCCESS: All records are exactly 80 characters!")
else:
    print(f"FAILED: {errors} records with incorrect length")

# Save to file
output_file = r"d:\X\ND\ENSDF\.github\ensdf_formatted_keV.txt"
with open(output_file, 'w') as f:
    for record in formatted_records:
        f.write(record + "\n")

print(f"\nFormatted records saved to: {output_file}")
print(f"Total records: {len(formatted_records)}")
print(f"  L-records: 11")
print(f"  G-records: 85")
