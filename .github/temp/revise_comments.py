#!/usr/bin/env python3

def pad80(s):
    """Pad/trim string to exactly 80 chars."""
    if isinstance(s, bytes):
        s = s.decode('ascii')
    s_bytes = s.encode('ascii')
    if len(s_bytes) >= 80:
        return s_bytes[:80].decode('ascii') + '\n'
    return (s_bytes + b' ' * (80 - len(s_bytes))).decode('ascii') + '\n'

# Read file
with open('D:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens', 'r') as f:
    content = f.read()

# Define replacements as (old_text, new_lines_list)
replacements = [
    (
        # 1983Ra04 - old text (exactly as it appears in file)
        " 34CL c  1983Ra04: {+33}S(p,|g) with E=0.9-1.4 MeV on an 88.2%-enriched S target\n 34CL2c  (CdS on carbon backing). NaI detector (|g rays, 90|' relative to the   \n 34CL3c  beam direction) and Si surface barrier (proton detector, 135|' relative\n 34CL4c  to the beam direction). Measured the reaction Q value and S(p).",
        [
            " 34CL c  1983Ra04: 0.9-1.4-MeV proton beams impinged on an 88.2%-enriched {+33}S",
            " 34CL2c  target (CdS on carbon backing). |g rays were detected using a NaI",
            " 34CL3c  detector at 90|' relative to the beam direction and protons were",
            " 34CL4c  detected using a Si surface barrier detector at 135|' relative to the",
            " 34CL5c  beam direction. Measured E|g, I|g, reaction Q, and S(p).",
        ]
    ),
    (
        # 1971Hy02 - old text
        " 34CL c  1971Hy02: {+33}S(p,|g) E=1058, 1098, 1121 MeV, 84%-enriched S target   \n 34CL2c  (Ag backing soldered on brass disk), Ge(Li) and NaI detectors. Measured\n 34CL3c  |g(|q), |g-branching, |d, resonance strengths. Studied three resonances",
        [
            " 34CL c  1971Hy02: Proton beams at E(lab)=1058, 1098, 1121 keV impinged on an",
            " 34CL2c  84%-enriched {+33}S target (Ag backing soldered on brass disk). |g rays",
            " 34CL3c  were detected using Ge(Li) and NaI detectors. Measured E|g, I|g, angular",
            " 34CL4c  distribution |g(|q). Deduced resonance strengths, |g-branching ratios,",
            " 34CL5c  and |d. Studied three resonances.",
        ]
    ),
    (
        # 1969Gr29 - old text
        " 34CL c  1969Gr29: {+33}S(p,|g) E=1.0-1.3 MeV, 25%-enriched S target (|a|g      \n 34CL2c  backing soldered on brass disk). Ge(Li) detector placed at 0|' and     \n 34CL3c  115|' or 120|' relative to beam direction. Measured J, |p, |d,         \n 34CL4c  |g-branching, T{-1/2} by DSAM. Data for six resonances from 1057 to    \n 34CL5c  1266 keV. Studied six resonances",
        [
            " 34CL c  1969Gr29: 1.0-1.3-MeV proton beams impinged on a 25%-enriched {+33}S",
            " 34CL2c  target (|a|g backing soldered on brass disk). |g rays were detected using",
            " 34CL3c  a Ge(Li) detector placed at 0|' and 115|' or 120|' relative to the beam",
            " 34CL4c  direction. Measured E|g, I|g, angular distribution |g(|q). Deduced J, |p,",
            " 34CL5c  |d, |g-branching ratios, and lifetimes for six resonances (1057-1266",
            " 34CL6c  keV) using DSAM.",
        ]
    ),
    (
        # 1964Gl04 - old text
        " 34CL c  1964Gl04: {+33}S(p,|g) E=0.3-1.3 MeV, 22%-enriched S target (CdS on Cu \n 34CL2c  or Ta backings), NaI detectors at +85|' and -85|' relative to the beam \n 34CL3c  direction. Measured primary and secondary E|g, I|g, |g|g, levels,      \n 34CL4c  resonances and resonance strengths for E{-p}(lab)=447, 507, 546, 639,  \n 34CL5c  662, 683, 731, 777, and 822 keV. For strong primary transitions the    \n 34CL6c  branching ratios are in general agreement with Ge data from 1993Wa27   \n 34CL7c  with exception of a few cases as noted under comments for relevant |g  \n 34CL8c  rays. Studied 22 resonances",
        [
            " 34CL c  1964Gl04: 0.3-1.3-MeV proton beams impinged on a 22%-enriched {+33}S",
            " 34CL2c  target (CdS on Cu or Ta backings). |g rays were detected using NaI",
            " 34CL3c  detectors at +85|' and -85|' relative to the beam direction. Measured",
            " 34CL4c  E|g, I|g, |g|g-coin for nine resonances (E{-p}(lab)=447, 507, 546, 639,",
            " 34CL5c  662, 683, 731, 777, 822 keV). Deduced resonance strengths and levels.",
            " 34CL6c  For strong primary transitions branching ratios in general agreement with",
            " 34CL7c  Ge data from 1993Wa27 with noted exceptions.",
        ]
    ),
]

# Apply replacements
for old_text, new_lines in replacements:
    new_text = '\n'.join([pad80(line).rstrip('\n') for line in new_lines])
    if old_text in content:
        content = content.replace(old_text, new_text, 1)
        print(f"Replaced: {new_lines[0][:40]}...")
    else:
        print(f"WARNING: Old text not found for {new_lines[0][:30]}...")

# Write back
with open('D:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens', 'w') as f:
    f.write(content)

print("\nFile updated successfully.")
