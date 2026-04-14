"""
Dry-run: Insert XREF label K (36S(p,d)) into matched adopted levels.
For Δ > 5 keV, uses K(pd_energy) notation.

Usage:
  python .github/temp/insert_xref_k.py [--apply]
  Default: dry-run (no file changes).
  --apply : actually write changes to S35_adopted.ens
"""

import sys
import re

ADOPTED_FILE = r"d:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens"

# Matched levels: (adopted_E_str, pd_E_int, delta_keV)
# If delta > 5 keV → XREF label is K(pd_E), else K
MATCHED = [
    (0.000,     0,    0.0),
    (1572.370,  1569, 3.4),
    (1991.270,  1990, 1.3),
    (2347.779,  2348, 0.2),
    (2717.070,  2718, 0.9),
    (2938.620,  2937, 1.6),
    (3423.200,  3420, 3.2),
    (3558.079,  3558, 0.1),
    (3594.620,  3592, 2.6),
    (3801.952,  3800, 2.0),
    (3886.280,  3883, 3.3),
    (4023.240,  4023, 0.2),
    (4105.600,  4107, 1.4),
    (4180.000,  4182, 2.0),
    (4302.600,  4300, 2.6),
    (4482.000,  4486, 4.0),
    (4576.000,  4574, 2.0),
    (4617.000,  4614, 3.0),
    (4839.000,  4838, 1.0),
    (4903.371,  4907, 3.6),
    (4963.081,  4955, 8.1),   # > 5 → K(4955)
    (5127.000,  5121, 6.0),   # > 5 → K(5121)
    (5771.000,  5766, 5.0),   # exactly 5 → K (not >5)
    (5841.482,  5844, 2.5),
    (6129.000,  6121, 8.0),   # > 5 → K(6121)
    (6334.000,  6338, 4.0),
    (6446.000,  6439, 7.0),   # > 5 → K(6439)
    (6545.100,  6550, 4.9),
    (6635.200,  6639, 3.8),
    (6684.000,  6682, 2.0),
    (6986.096,  6962, 24.1),  # > 5 → K(6962)
    (7018.890,  7019, 0.1),
    (7100.730,  7102, 1.3),
    (7143.270,  7151, 7.7),   # > 5 → K(7151)
    (7218.000,  7215, 3.0),
    (7253.200,  7249, 4.2),
    (7275.930,  7279, 3.1),
    (7331.000,  7326, 5.0),   # exactly 5 → K
    (7347.900,  7349, 1.1),
    (7442.140,  7441, 1.1),
    (7494.500,  7490, 4.5),
    (7749.700,  7753, 3.3),
    (7889.000,  7885, 4.0),
    (7974.190,  7980, 5.8),   # > 5 → K(7980)
    (8076.460,  8073, 3.5),
    (8093.000,  8103, 10.0),  # > 5 → K(8103)
    (8224.200,  8221, 3.2),
    (8273.300,  8270, 3.3),
    (8406.550,  8410, 3.5),
]

# Build lookup: adopted_E → K_label
# Match adopted energy by parsing L-record E field (cols 9-18, 0-based)
THRESHOLD = 5.0  # strictly >5 keV

def k_label(pd_e, delta):
    if delta > THRESHOLD:
        return f"K({pd_e})"
    return "K"

# Build dict: round adopted_E to 3 decimal places as key
target_map = {}
for (adE, pdE, delta) in MATCHED:
    label = k_label(pdE, delta)
    # Store the rounded value as key
    key = round(adE, 3)
    target_map[key] = label


def parse_l_energy(line):
    """Parse L-record energy from cols 9-18 (0-based), return float or None."""
    if len(line) < 10:
        return None
    # Check record type: col5=' ', col6=' ', col7='L', col8=' '
    if not (line[5] == ' ' and line[6] == ' ' and line[7] == 'L' and line[8] == ' '):
        return None
    e_str = line[9:19].strip()
    if not e_str:
        return None
    try:
        return float(e_str)
    except ValueError:
        return None


def insert_k_in_xref(xref_str, k_label):
    """
    Insert k_label alphabetically between J and L in the XREF string.
    xref_str is the full XREF= value, e.g. 'ABCDEFHIJLMNO'
    Handles parenthetical notations like L(4186*), K(3592), etc.
    Returns the new XREF string portion (after 'XREF=').
    """
    # Parse the XREF string into a sequence of (letter, optional_paren_suffix)
    # Pattern: uppercase letter, then optional (...)
    pattern = re.compile(r'([A-Z])(\([^)]*\))?')
    entries = pattern.findall(xref_str)  # list of (letter, paren_or_empty)

    # Check if K is already present
    letters = [e[0] for e in entries]
    if 'K' in letters:
        # K already present — skip
        return None  # signal: no change needed

    # Find insertion point: after J entries, before L entries
    # Insert K so that labels remain alphabetically sorted
    new_entries = []
    k_inserted = False
    for (letter, paren) in entries:
        if not k_inserted and letter > 'K':
            new_entries.append(k_label)
            k_inserted = True
        new_entries.append(letter + paren)
    if not k_inserted:
        new_entries.append(k_label)

    return ''.join(new_entries)


def process(apply=False):
    with open(ADOPTED_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_l_energy = None
    changes = []  # list of (line_idx, old_line, new_line)

    for i, line in enumerate(lines):
        # Remove trailing newline for processing
        raw = line.rstrip('\n').rstrip('\r')

        # Check if this is an L-record (first occurrence, col6=blank)
        e = parse_l_energy(raw)
        if e is not None:
            current_l_energy = e
            continue

        # Check if this is an XREF line: " 35S X L XREF=..."
        # Pattern: cols 0-4 = NUCID, col5='X', col6=' ', col7='L'
        if (len(raw) >= 18 and
            raw[5] == 'X' and raw[6] == ' ' and raw[7] == 'L' and
            'XREF=' in raw):

            if current_l_energy is None:
                continue

            # Look up this energy in our target map
            rounded = round(current_l_energy, 3)
            if rounded not in target_map:
                # Not a matched level — skip
                continue

            k_lbl = target_map[rounded]
            xref_start = raw.index('XREF=') + 5
            xref_content = raw[xref_start:].rstrip()

            new_content = insert_k_in_xref(xref_content, k_lbl)
            if new_content is None:
                print(f"Line {i+1}: K already present in XREF for E={rounded} — skipping")
                continue

            # Build new line: preserve up to 'XREF=' then new content, pad to 80
            prefix = raw[:xref_start]
            new_raw = (prefix + new_content).ljust(80)
            if len(new_raw) > 80:
                print(f"WARNING line {i+1}: new XREF line exceeds 80 chars ({len(new_raw)}): {new_raw!r}")

            changes.append((i, raw, new_raw))
            delta = target_map[rounded]
            print(f"Line {i+1:4d} E={rounded:>10.3f}:  {raw.rstrip()}")
            print(f"           →  {new_raw.rstrip()}")
            print()

    print(f"\nTotal changes: {len(changes)}")
    print(f"Expected: {len(MATCHED)}")

    if apply:
        print("\nApplying changes...")
        for (idx, old, new) in changes:
            # Preserve original line ending
            orig_ending = lines[idx][len(lines[idx].rstrip('\r\n')):]
            lines[idx] = new + orig_ending
        with open(ADOPTED_FILE, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
        print(f"Written {len(changes)} changes to {ADOPTED_FILE}")
    else:
        print("\n[DRY RUN] No changes written. Use --apply to apply.")


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    process(apply=apply)
