#!/usr/bin/env python3
"""
Revise dataset comments in Cl34_33s_p_g.ens with proper 80-char padding.
"""

def pad_to_80(s):
    """Pad string to exactly 80 chars."""
    if isinstance(s, bytes):
        s = s.decode('ascii')
    # Strip any trailing whitespace first
    s = s.rstrip()
    if len(s) > 80:
        raise ValueError(f"String too long (would lose data): {len(s)} > 80: {s[:50]}")
    # Pad to exactly 80 chars
    return s + ' ' * (80 - len(s))

# Read the full file
with open('D:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens', 'r') as f:
    content = f.read()

# Define replacements with exact 80-char lines
replacements = [
    # 1983Ra04 (from old compressed form to new detailed form with 5 lines)
    (
        " 34CL c  1983Ra04: {+33}S(p,|g) with E=0.9-1.4 MeV on an 88.2%-enriched S target\n 34CL2c  (CdS on carbon backing). NaI detector (|g rays, 90|' relative to the   \n 34CL3c  beam direction) and Si surface barrier (proton detector, 135|' relative\n 34CL4c  to the beam direction). Measured the reaction Q value and S(p).",
        [
            " 34CL c  1983Ra04: 0.9-1.4-MeV proton beams impinged on an 88.2%-enriched {+33}S",
            " 34CL2c  target (CdS on carbon backing). |g rays were detected using a NaI",
            " 34CL3c  detector at 90|' relative to the beam direction and protons were",
            " 34CL4c  detected using a Si surface barrier detector at 135|' relative to the",
            " 34CL5c  beam direction. Measured E|g, I|g, reaction Q, and S(p).",
        ]
    ),
    # 1971Hy02 (from compressed to detailed with 5 lines)
    (
        " 34CL c  1971Hy02: {+33}S(p,|g) E=1058, 1098, 1121 MeV, 84%-enriched S target   \n 34CL2c  (Ag backing soldered on brass disk), Ge(Li) and NaI detectors. Measured\n 34CL3c  |g(|q), |g-branching, |d, resonance strengths. Studied three resonances",
        [
            " 34CL c  1971Hy02: Proton beams at E(lab)=1058, 1098, 1121 keV impinged on an",
            " 34CL2c  84%-enriched {+33}S target (Ag backing soldered on brass disk). |g rays",
            " 34CL3c  were detected using Ge(Li) and NaI detectors. Measured E|g, I|g, angular",
            " 34CL4c  distribution |g(|q). Resonance strengths, |g-branching ratios, |d",
            " 34CL5c  deduced. Studied three resonances.",
        ]
    ),
    # 1969Gr29 (from mixed form to detailed with 6 lines)
    (
        " 34CL c  1969Gr29: {+33}S(p,|g) E=1.0-1.3 MeV, 25%-enriched S target (|a|g      \n 34CL2c  backing soldered on brass disk). Ge(Li) detector placed at 0|' and     \n 34CL3c  115|' or 120|' relative to beam direction. Measured J, |p, |d,         \n 34CL4c  |g-branching, T{-1/2} by DSAM. Data for six resonances from 1057 to    \n 34CL5c  1266 keV. Studied six resonances",
        [
            " 34CL c  1969Gr29: 1.0-1.3-MeV proton beams impinged on a 25%-enriched {+33}S",
            " 34CL2c  target (|a|g backing soldered on brass disk). |g rays detected using a",
            " 34CL3c  Ge(Li) detector at 0|' and 115|' or 120|' relative to beam. Measured E|g,",
            " 34CL4c  I|g, angular distribution |g(|q). Deduced J, |p, |d, |g-branching",
            " 34CL5c  ratios, lifetimes for six resonances (1057-1266 keV) using DSAM.",
            " 34CL6c  ",
        ]
    ),
    # 1964Gl04 (from extended to improved 7-line form)
    (
        " 34CL c  1964Gl04: {+33}S(p,|g) E=0.3-1.3 MeV, 22%-enriched S target (CdS on Cu \n 34CL2c  or Ta backings), NaI detectors at +85|' and -85|' relative to the beam \n 34CL3c  direction. Measured primary and secondary E|g, I|g, |g|g, levels,      \n 34CL4c  resonances and resonance strengths for E{-p}(lab)=447, 507, 546, 639,  \n 34CL5c  662, 683, 731, 777, and 822 keV. For strong primary transitions the    \n 34CL6c  branching ratios are in general agreement with Ge data from 1993Wa27   \n 34CL7c  with exception of a few cases as noted under comments for relevant |g  \n 34CL8c  rays. Studied 22 resonances",
        [
            " 34CL c  1964Gl04: 0.3-1.3-MeV proton beams impinged on a 22%-enriched {+33}S",
            " 34CL2c  target (CdS on Cu or Ta backings). NaI detectors at +85|' and -85|' to",
            " 34CL3c  the beam. Measured E|g, I|g, |g|g-coincidence. Proton energies E{-p}(lab)",
            " 34CL4c  =447, 507, 546, 639, 662, 683, 731, 777, 822 keV. Deduced resonance",
            " 34CL5c  strengths and levels. For strong primary |g branching ratios generally",
            " 34CL6c  agree with Ge data from 1993Wa27; noted exceptions in gamma-ray comments.",
            " 34CL7c  ",
        ]
    ),
]

# Apply replacements
for old_text, new_lines in replacements:
    # Pad all lines to exactly 80 chars
    padded_new_lines = [pad_to_80(line) for line in new_lines]
    new_text = '\n'.join(padded_new_lines)
    
    if old_text in content:
        content = content.replace(old_text, new_text, 1)
        print(f"✓ Replaced: {new_lines[0][:50]}...")
    else:
        print(f"✗ WARNING: Old text not found for {new_lines[0][:40]}...")

# Verify all lines are exactly 80 chars
lines = content.split('\n')
error_count = 0
for i, line in enumerate(lines, 1):
    if line and not line.startswith(' 34CL'):
        continue  # Skip non-comment lines for this check
    if line and len(line) != 80:
        print(f"✗ ERROR: Line {i} is {len(line)} chars, not 80")
        error_count += 1

if error_count > 0:
    print(f"\n⚠ FOUND {error_count} LINE LENGTH ERRORS - NOT WRITING FILE")
else:
    # Write back
    with open('D:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens', 'w') as f:
        f.write(content)
    print(f"\n✅ All lines verified as exactly 80 chars. File updated successfully.")
