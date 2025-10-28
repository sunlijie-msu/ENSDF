#!/usr/bin/env python3
"""
Compare G-record interpretation with CSV final states for L 7547
"""

# Adopted levels in 2001VO24.ens
adopted = [0, 1219, 5645, 7179, 7547, 7838, 8207, 8216, 8381, 8484, 8893, 8907, 9081]

# Gammas from L 7547 in .ens file
gammas_7547_ens = [1901, 4384, 4544, 4901, 7070]

# Corresponding final states (if gamma is egamma)
print('If G-record energies are GAMMA ENERGIES (egamma):')
for g in gammas_7547_ens:
    final = 7547 - g
    exists = final in adopted
    status = "YES" if exists else "NO"
    print(f'  G {g:4d} -> final state {final:5.0f}  {status}')

print()

# CSV matrix final states for Exi=7547
csv_finals_7547 = [5646, 3163, 3003, 2646, 477]
print('CSV final states for Exi=7547:')
for f in csv_finals_7547:
    exists = f in adopted
    status = "YES" if exists else "NO"
    print(f'  Exf {f:4d}  {status}')

print()
print("ANALYSIS: None of the 2001VO24 CSV final states exist in the adopted level scheme!")
print("This suggests a FUNDAMENTAL MISMATCH between 2001VO24 data and the adopted scheme.")
print()
print("POSSIBLE CAUSES:")
print("1. The adopted level scheme is different from the one used in 2001VO24")
print("2. The G-record format is misinterpreted (records might mean something else)")
print("3. The CSV data has conversion errors in the transformation")
print("4. The gammas should be DELETED because they point to unobserved intermediate states")
