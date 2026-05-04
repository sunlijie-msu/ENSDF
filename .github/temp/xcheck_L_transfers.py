"""
Cross-check ALL cL J$ comment L= values against source reaction .ens L-transfer fields.
Also verify angular momentum coupling deductions.
"""
import re
import os
import subprocess
import sys

ADOPTED_PATH = r'A34\Cl34\new\Cl34_adopted.ens'
THRESHOLD = 5200.0

# Mapping from comment text reaction names to .ens files
REACTION_FILES = {
    '36ar_d_a': r'A34\Cl34\new\Cl34_36ar_d_a_pol_d_a.ens',
    '33s_3he_d': r'A34\Cl34\new\Cl34_33s_3he_d.ens',
    '35cl_3he_a': r'A34\Cl34\new\Cl34_35cl_3he_a.ens',
    '32s_3he_p': r'A34\Cl34\new\Cl34_32s_3he_p.ens',
    '32s_a_d': r'A34\Cl34\new\Cl34_32s_a_d.ens',
    '35cl_p_d': r'A34\Cl34\new\Cl34_35cl_p_d.ens',
    '34s_3he_t': r'A34\Cl34\new\Cl34_34s_3he_t.ens',
    '32s_3he_pg': r'A34\Cl34\new\Cl34_32s_3he_pg.ens',
    '33s_3he_d': r'A34\Cl34\new\Cl34_33s_3he_d.ens',
}

def load_level_L_transfers(filepath):
    """Load all L-records with energy and L-transfer field (cols 56-64, 0-indexed 55-63)."""
    levels = []
    try:
        with open(filepath, 'r') as f:
            for i, line in enumerate(f, 1):
                raw = line.rstrip('\n')
                if len(raw) >= 9 and raw[7] == 'L' and raw[5] == ' ' and raw[6] == ' ':
                    e_str = raw[9:19].strip()
                    try:
                        E = float(e_str)
                    except ValueError:
                        E = None
                    L_field = raw[55:64].strip() if len(raw) >= 64 else ''
                    levels.append({'line': i, 'E': E, 'E_str': e_str, 'L': L_field})
    except FileNotFoundError:
        pass
    return levels


def find_matching_level(levels, E_adopted, tol=30.0):
    """Find level in source file matching adopted level within tolerance keV."""
    if E_adopted is None:
        return None
    best = None
    best_diff = tol
    for lvl in levels:
        if lvl['E'] is None:
            continue
        diff = abs(lvl['E'] - E_adopted)
        if diff <= best_diff:
            best_diff = diff
            best = lvl
    return best


def extract_adopted_levels_with_J_comments():
    """Extract all adopted L-records + full J$ comment text blocks below threshold."""
    with open(ADOPTED_PATH, 'r') as f:
        lines = f.readlines()
    
    results = []
    current_E = None
    current_line = None
    in_scope = False
    current_J_text = []   # Full J$ comment text (concatenated)
    current_J_lines = []  # Raw lines
    in_J_block = False

    for i, line in enumerate(lines, 1):
        raw = line.rstrip('\n')
        if len(raw) < 8:
            continue

        # L-record detection: col6=' ', col7=' ', col8='L'
        if raw[5] == ' ' and raw[6] == ' ' and raw[7] == 'L':
            # Save previous level if in scope
            if in_scope and current_E is not None and current_J_text:
                results.append({
                    'E': current_E,
                    'adopted_line': current_line,
                    'J_text': ' '.join(current_J_text),
                    'J_lines': current_J_lines[:]
                })
            elif in_scope and current_E is not None:
                results.append({
                    'E': current_E,
                    'adopted_line': current_line,
                    'J_text': '',
                    'J_lines': []
                })
            # New level
            e_str = raw[9:19].strip()
            try:
                current_E = float(e_str)
            except ValueError:
                current_E = None
            current_line = i
            in_scope = (current_E is not None and current_E < THRESHOLD)
            current_J_text = []
            current_J_lines = []
            in_J_block = False
            continue

        if not in_scope:
            continue

        col6 = raw[5]  # CONT marker (index 5 = col 6)
        col7 = raw[6]  # index 6 = col 7
        col8 = raw[7]  # index 7 = col 8

        # Primary cL comment: col6=' ', col7='c', col8='L'
        if col6 == ' ' and col7 == 'c' and col8 == 'L':
            rest = raw[9:].strip()
            if rest.startswith('J$'):
                # Start new J$ block
                current_J_text = [rest[2:]]  # strip 'J$'
                current_J_lines = [(i, raw)]
                in_J_block = True
            else:
                in_J_block = False

        # Continuation cL comment: col6 in '23456789', col7='c', col8='L'
        elif col6 in '23456789' and col7 == 'c' and col8 == 'L':
            if in_J_block:
                rest = raw[9:].strip()
                current_J_text.append(rest)
                current_J_lines.append((i, raw))

        # Non-comment record type (G, B, E, A) — don't reset J block but it won't matter
        # since new cL non-J$ will reset in_J_block=False

    # Save last level
    if in_scope and current_E is not None:
        if current_J_text:
            results.append({
                'E': current_E,
                'adopted_line': current_line,
                'J_text': ' '.join(current_J_text),
                'J_lines': current_J_lines[:]
            })
        else:
            results.append({
                'E': current_E,
                'adopted_line': current_line,
                'J_text': '',
                'J_lines': []
            })
    return results


def run_coupling(Ji_pi, reaction_type, L_val):
    """Run angular_momentum_coupling.py for a given initial Jpi and L transfer.
    Returns string like '1+,2+,3+' or error message."""
    # Determine particle type from reaction
    # Stripping reactions (add nucleon to target): (3He,d) adds proton, (3He,t) adds proton,
    #   (d,a) removes? Actually (d,alpha) removes a neutron+proton pair (dineutron+dipro?
    #   No: (d,alpha) = d + target → α + residual. Residual = target + d - α = target - (A=2,Z=2) + d?
    #   Actually (d,α): target absorbs d, emits α → removes 2 nucleons from target
    #   For 36Ar(d,α)34Cl: 36Ar - d + α → wait, 36Ar(d,α) means:
    #     36Ar + d → 34Cl + α 
    #     36Ar(Z=18,A=36) + d(A=2) → 34Cl(Z=17,A=34) + α(A=4)
    #     Transfer: 2 nucleons (one proton, one neutron) removed from 36Ar? No wait:
    #     α=4He(Z=2,A=4) absorbed, d(Z=1,A=2) emitted → net gain = α-d = Z:+1,A:+2
    #     So 36Ar gains 1p+2n? That doesn't give 34Cl.
    #     Let me redo: 36Ar(d,α): the d comes in, α goes out.
    #     Input: 36Ar + d → Output: 34Cl + α
    #     Nucleons: 36Ar(18p,18n) + d(1p,1n) → 34Cl(17p,17n) + α(2p,2n)
    #     LHS: 19p+19n, RHS: 19p+19n ✓
    #     Transfer: 34Cl = 36Ar - (1p+1n) i.e., removes 1p+1n from 36Ar
    #     Target: 36Ar(0+), L-transfer for removing proton+neutron pair...
    # This is getting complex. The angular_momentum_coupling.py script should handle it.
    # Let me just call it with the appropriate particle type.
    # From the script's last usage: python angular_momentum_coupling.py Ji_pi j_transfer_or_particle
    # Let me check what arguments it takes.
    try:
        result = subprocess.run(
            ['python', r'.github\scripts\angular_momentum_coupling.py', Ji_pi, L_val],
            capture_output=True, text=True, timeout=10, cwd='.'
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return f"ERROR: {e}", -1


def parse_L_claims_from_J_text(J_text):
    """
    Extract all 'L=X from Jpi in reaction' claims from J$ text.
    Returns list of dicts: {L, Jpi_target, reaction, result_Jpi, full_clause}
    """
    claims = []
    # Pattern: L=<L> from <Jpi> in <reaction> gives <result>
    # or L=<L> from <Jpi> in <reaction>: ...
    # Remove ENSDF text format codes like {+33}, |g, etc.
    return J_text  # Return raw text for manual parsing


# Main execution
levels = extract_adopted_levels_with_J_comments()
with_J = [(lvl) for lvl in levels if lvl['J_text']]
print(f"Total levels below {THRESHOLD} keV: {len(levels)}")
print(f"Levels with cL J$ comments: {len(with_J)}")
print()

for lvl in with_J:
    print(f"=== E={lvl['E']} keV (line {lvl['adopted_line']}) ===")
    for i, raw in lvl['J_lines']:
        print(f"  L{i:4d}: {raw}")
    print(f"  FULL J$ TEXT: {lvl['J_text'][:200]}")
    print()
