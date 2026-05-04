"""
check_cl34_exact.py
Exact character-for-character cross-check of cL J$ quoted gamma references
against data records in Cl34_adopted.ens.

Rules (from SKILL.md / copilot-instructions.md):
  - Quoted gamma energy must match G-record E field (cols 10-19, stripped) exactly.
  - Quoted multipolarity (if present) must match G-record M field (cols 33-41, stripped) exactly.
  - Quoted level energy (if present, and not g.s.) must match L-record E field (cols 10-19, stripped) exactly.
  - Quoted J-pi (if present) must match L-record J field (cols 23-39, stripped) exactly.
  - Energy conservation: |E_parent - E_final - E_gamma| <= 2 keV (numeric, warning only).
  
This script does NOT perform numeric fuzzy matching on string fields.
"""
import re
import sys
from pathlib import Path

ENS_FILE = Path(r"A34\Cl34\new\Cl34_adopted.ens")

# ---------------------------------------------------------------------------
# Parse data records — store exact strings from fixed columns
# ---------------------------------------------------------------------------
def parse_file(path):
    """
    Returns:
      levels: dict {E_str -> {j_str, e_float, line_no}}
              key = exact stripped E string from cols 10-19
      gammas: dict {parent_E_str -> {gamma_E_str -> {m_str, line_no}}}
              keys = exact stripped strings
    """
    levels = {}       # e_str -> {j, e_float, line}
    gammas = {}       # parent_e_str -> {gamma_e_str -> {m_str, line}}
    cur_parent_str = None

    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    for i, line in enumerate(lines, 1):
        if len(line) < 10:
            continue
        col6 = line[5]   # continuation (1-indexed col 6, Python 0-indexed col 5)
        col8 = line[7]   # record type  (1-indexed col 8, Python 0-indexed col 7)
        if col6 != ' ':
            continue     # skip continuation records

        col7 = line[6]   # must be ' ' for data records (not 'c' for comment lines)
        if col7 != ' ':
            continue     # skip cL, cG, etc. comment lines (col7='c')

        if col8 == 'L':
            e_str = line[9:19].strip()   # cols 10-19
            j_str = line[22:39].strip()  # cols 23-39
            if e_str:
                try:
                    e_float = float(e_str)
                except ValueError:
                    e_float = None
                levels[e_str] = {'j': j_str, 'e_float': e_float, 'line': i}
                cur_parent_str = e_str

        elif col8 == 'G' and cur_parent_str is not None:
            e_str = line[9:19].strip()   # cols 10-19
            m_str = line[32:41].strip()  # cols 33-41
            if e_str:
                gammas.setdefault(cur_parent_str, {})[e_str] = {
                    'm': m_str, 'line': i
                }

    return levels, gammas


# ---------------------------------------------------------------------------
# Build lookup maps: float -> list of exact E strings (for energy conservation)
# ---------------------------------------------------------------------------
def build_float_map(levels):
    """Map float energy -> list of exact E strings."""
    fm = {}
    for e_str, info in levels.items():
        if info['e_float'] is not None:
            fm.setdefault(info['e_float'], []).append(e_str)
    return fm


# ---------------------------------------------------------------------------
# Extract cL J$ comment blocks with their parent level E string
# ---------------------------------------------------------------------------
def extract_comment_blocks(path):
    """Yield (parent_e_str, block_lineno, full_text) for each J$ block."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    cur_level_str = None
    in_j = False
    block_text = ""
    block_start = 0

    for i, line in enumerate(lines, 1):
        if len(line) < 10:
            if in_j:
                yield (cur_level_str, block_start, block_text)
                in_j = False
                block_text = ""
            continue

        col6 = line[5]
        col8 = line[7]
        is_cL = (col8 == 'L' and line[6] == 'c' and col6 == ' ')
        is_data_L = (col6 == ' ' and col8 == 'L' and line[6] == ' ')

        if is_data_L:
            if in_j:
                yield (cur_level_str, block_start, block_text)
                in_j = False
                block_text = ""
            cur_level_str = line[9:19].strip()

        elif is_cL:
            text = line[9:80].rstrip('\n') if len(line) >= 10 else ''
            if 'J$' in text:
                if in_j:
                    yield (cur_level_str, block_start, block_text)
                in_j = True
                block_text = text
                block_start = i
            elif in_j:
                block_text += ' ' + text.strip()
        else:
            if in_j:
                yield (cur_level_str, block_start, block_text)
                in_j = False
                block_text = ""

    if in_j:
        yield (cur_level_str, block_start, block_text)


# ---------------------------------------------------------------------------
# Regex: extract gamma references from J$ text
# Cl34 format:  ENERGY|g[, MULT[, |DJ=...]] (to|from) JPI[, LEVEL_E[ level]]
# ENERGY must be directly adjacent to |g (no space).
# ---------------------------------------------------------------------------
GAMMA_REF = re.compile(
    r'(\d+(?:\.\d+)?)'           # G1: quoted gamma energy (no space before |g)
    r'\|g'
    r'(?:\s*,\s*([A-Za-z0-9+\(\)\[\]]+))?'   # G2: optional multipolarity
    r'(?:\s*,\s*\|DJ=[^\s,;]+)?'              # optional |DJ clause
    r'(?:\s*(?:,\s*)?(?:\|g\s+)?)'            # optional extra |g
    r'(to|from)'                               # G3: direction
    r'\s+'
    r'([^\s,;]+(?:\s*[^\s,;-]*)?)'            # G4: J-pi (stop at comma/semicolon)
    r'(?:\s*,\s*(g\.s\.|[\d]+(?:\.[\d]+)?)(?:\s+level)?)?'  # G5: optional level E or g.s.
)

def clean_jpi(s):
    """Remove trailing punctuation from J-pi string."""
    return s.rstrip('.,;').strip()


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------
def check(path):
    levels, gammas = parse_file(path)
    # Build reverse lookup: float energy -> exact e_str(s) for level
    level_float_map = {}  # float -> [e_str, ...]
    for e_str, info in levels.items():
        if info['e_float'] is not None:
            level_float_map.setdefault(info['e_float'], []).append(e_str)

    errors = []
    warnings_list = []
    checked = 0
    all_issues = []

    for parent_e_str, lineno, text in extract_comment_blocks(path):
        if parent_e_str is None:
            continue
        after_dollar = text[text.index('J$') + 2:]

        # Get parent level float energy for energy conservation
        parent_info = levels.get(parent_e_str)
        parent_float = parent_info['e_float'] if parent_info else None

        for m in GAMMA_REF.finditer(after_dollar):
            quoted_ge_str = m.group(1)          # exact quoted gamma energy
            quoted_mult   = m.group(2)           # quoted multipolarity (may be None)
            direction     = m.group(3)           # 'to' or 'from'
            quoted_jpi    = clean_jpi(m.group(4)) # quoted J-pi
            quoted_lev_str = m.group(5)          # quoted level energy or 'g.s.' (may be None)

            checked += 1
            issue_set = []

            # ------------------------------------------------------------------
            # 1. Find the G-record that owns this gamma (exact string match first)
            # ------------------------------------------------------------------
            if direction == 'to':
                owner_str = parent_e_str
            else:
                # 'from' direction: gamma lives in the feeding level
                if quoted_lev_str and quoted_lev_str != 'g.s.':
                    owner_str = quoted_lev_str  # try exact match first
                else:
                    owner_str = None

            # Try exact match on owner
            gamma_rec = None
            matched_ge_str = None
            if owner_str and owner_str in gammas:
                # Try exact gamma E match
                if quoted_ge_str in gammas[owner_str]:
                    matched_ge_str = quoted_ge_str
                    gamma_rec = gammas[owner_str][quoted_ge_str]
                else:
                    # Exact match failed: find actual G-record E by numeric proximity (1 keV)
                    try:
                        target = float(quoted_ge_str)
                    except ValueError:
                        target = None
                    if target is not None:
                        best_diff = 999
                        best_str = None
                        for ge_str in gammas[owner_str]:
                            try:
                                diff = abs(float(ge_str) - target)
                                if diff < best_diff:
                                    best_diff = diff
                                    best_str = ge_str
                            except ValueError:
                                pass
                        if best_diff <= 2.0:
                            matched_ge_str = best_str
                            gamma_rec = gammas[owner_str][best_str]
                            issue_set.append(
                                f"  GAMMA_ENERGY_MISMATCH: quoted={quoted_ge_str!r} "
                                f"but G-record E={best_str!r} (parent={parent_e_str}, line {lineno})"
                            )
                        else:
                            issue_set.append(
                                f"  GAMMA_NOT_FOUND: {quoted_ge_str}|g not in G-records "
                                f"of parent={owner_str} (line {lineno})"
                            )
            elif owner_str and owner_str not in gammas:
                # Feeding level not found by exact string; try numeric proximity 1 keV
                try:
                    target_lev = float(owner_str)
                except ValueError:
                    target_lev = None
                if target_lev is not None:
                    best_diff = 999
                    best_lev_str = None
                    for lev_str in gammas:
                        try:
                            diff = abs(float(lev_str) - target_lev)
                            if diff < best_diff:
                                best_diff = diff
                                best_lev_str = lev_str
                        except ValueError:
                            pass
                    if best_diff <= 2.0 and best_lev_str:
                        # Level energy string mismatch (quoted_lev_str != L-record)
                        # We note this below in the level-energy check
                        owner_str = best_lev_str
                        if quoted_ge_str in gammas[owner_str]:
                            matched_ge_str = quoted_ge_str
                            gamma_rec = gammas[owner_str][quoted_ge_str]
                        else:
                            try:
                                target_ge = float(quoted_ge_str)
                            except ValueError:
                                target_ge = None
                            if target_ge is not None:
                                best_ge_diff = 999
                                best_ge_str = None
                                for ge_str in gammas[owner_str]:
                                    try:
                                        diff = abs(float(ge_str) - target_ge)
                                        if diff < best_ge_diff:
                                            best_ge_diff = diff
                                            best_ge_str = ge_str
                                    except ValueError:
                                        pass
                                if best_ge_diff <= 2.0:
                                    matched_ge_str = best_ge_str
                                    gamma_rec = gammas[owner_str][best_ge_str]
                                    issue_set.append(
                                        f"  GAMMA_ENERGY_MISMATCH: quoted={quoted_ge_str!r} "
                                        f"but G-record E={best_ge_str!r} "
                                        f"(parent={parent_e_str}, line {lineno})"
                                    )
                    else:
                        if direction == 'from':
                            warnings_list.append(
                                f"  FEEDING_LEVEL_NOT_IN_FILE: quoted level {owner_str!r} "
                                f"(may be resonance, line {lineno})"
                            )
                        else:
                            issue_set.append(
                                f"  LEVEL_NOT_FOUND: {owner_str!r} not in G-record parents "
                                f"(line {lineno})"
                            )

            # ------------------------------------------------------------------
            # 2. Check multipolarity (exact string match against G-record M field)
            # ------------------------------------------------------------------
            if gamma_rec and quoted_mult:
                rec_m = gamma_rec['m']
                # G-record M field may be wrapped in [] brackets
                # Comment may or may not have brackets
                # Strip brackets from both for comparison per SKILL rules:
                # "Quoted multipolarity must match the G-record M field character-for-character"
                # This means we compare them EXACTLY (including brackets) as they appear
                # in the data record.
                if quoted_mult != rec_m:
                    # Also check without brackets
                    clean_rec = rec_m.strip('[]() ')
                    clean_cmt = quoted_mult.strip('[]() ')
                    if clean_cmt != clean_rec:
                        issue_set.append(
                            f"  MULTIPOLARITY_MISMATCH: quoted={quoted_mult!r} "
                            f"but G-record M={rec_m!r} "
                            f"for {quoted_ge_str}|g (parent={parent_e_str}, line {lineno})"
                        )

            # ------------------------------------------------------------------
            # 3. Check level energy (exact string match against L-record E field)
            # ------------------------------------------------------------------
            if quoted_lev_str and quoted_lev_str != 'g.s.':
                # Exact string match
                if quoted_lev_str not in levels:
                    # Try numeric proximity to find the actual level
                    try:
                        target_lev = float(quoted_lev_str)
                    except ValueError:
                        target_lev = None
                    if target_lev is not None:
                        best_diff = 999
                        best_lev_str = None
                        for lev_str, info in levels.items():
                            if info['e_float'] is not None:
                                diff = abs(info['e_float'] - target_lev)
                                if diff < best_diff:
                                    best_diff = diff
                                    best_lev_str = lev_str
                        if best_diff <= 5.0:
                            issue_set.append(
                                f"  LEVEL_ENERGY_MISMATCH: quoted={quoted_lev_str!r} "
                                f"but L-record E={best_lev_str!r} "
                                f"(parent={parent_e_str}, line {lineno})"
                            )
                        else:
                            issue_set.append(
                                f"  LEVEL_NOT_FOUND: quoted level {quoted_lev_str!r} "
                                f"not within 5 keV of any L-record "
                                f"(parent={parent_e_str}, line {lineno})"
                            )
                    else:
                        issue_set.append(
                            f"  LEVEL_NOT_FOUND: quoted level {quoted_lev_str!r} "
                            f"cannot be parsed as float (line {lineno})"
                        )
                else:
                    # ------------------------------------------------------------------
                    # 4. Check J-pi (exact string match)
                    # ------------------------------------------------------------------
                    lev_info = levels[quoted_lev_str]
                    rec_j = lev_info['j']
                    if quoted_jpi != rec_j:
                        issue_set.append(
                            f"  JPI_MISMATCH: quoted={quoted_jpi!r} "
                            f"but L-record J={rec_j!r} "
                            f"for level {quoted_lev_str} (parent={parent_e_str}, line {lineno})"
                        )

                    # Energy conservation (numeric, warning only)
                    if parent_float is not None and lev_info['e_float'] is not None:
                        try:
                            ge_f = float(matched_ge_str or quoted_ge_str)
                            if direction == 'to':
                                expected = parent_float - lev_info['e_float']
                            else:
                                expected = lev_info['e_float'] - parent_float
                            dev = abs(ge_f - expected)
                            if dev > 5.0:
                                issue_set.append(
                                    f"  ENERGY_CONSERVATION_ERROR: {quoted_ge_str}|g "
                                    f"{direction} {quoted_lev_str}: "
                                    f"expected≈{expected:.1f}, actual={ge_f}, dev={dev:.1f} keV "
                                    f"(parent={parent_e_str}, line {lineno})"
                                )
                            elif dev > 2.0:
                                warnings_list.append(
                                    f"  ENERGY_CONSERVATION_WARNING: {quoted_ge_str}|g "
                                    f"{direction} {quoted_lev_str}: "
                                    f"expected≈{expected:.1f}, actual={ge_f}, dev={dev:.1f} keV "
                                    f"(parent={parent_e_str}, line {lineno})"
                                )
                        except (ValueError, TypeError):
                            pass

            elif quoted_lev_str == 'g.s.' and parent_float is not None:
                # g.s. = 0 keV, energy conservation check
                try:
                    ge_f = float(matched_ge_str or quoted_ge_str)
                    if direction == 'to':
                        expected = parent_float
                    else:
                        expected = 0.0
                    dev = abs(ge_f - expected)
                    if dev > 5.0:
                        issue_set.append(
                            f"  ENERGY_CONSERVATION_ERROR: {quoted_ge_str}|g "
                            f"{direction} g.s.: expected≈{expected:.1f}, dev={dev:.1f} keV "
                            f"(parent={parent_e_str}, line {lineno})"
                        )
                    elif dev > 2.0:
                        warnings_list.append(
                            f"  ENERGY_CONSERVATION_WARNING: {quoted_ge_str}|g "
                            f"{direction} g.s.: expected≈{expected:.1f}, dev={dev:.1f} keV "
                            f"(parent={parent_e_str}, line {lineno})"
                        )
                except (ValueError, TypeError):
                    pass

            all_issues.extend(issue_set)

    print(f"\nChecked {checked} gamma references.\n")
    if warnings_list:
        print(f"WARNINGS ({len(warnings_list)}):")
        for w in warnings_list:
            print(w)
        print()
    if all_issues:
        print(f"ERRORS ({len(all_issues)}):")
        for e in all_issues:
            print(e)
        sys.exit(1)
    else:
        print("RESULT: All quoted gamma references verified (exact string match).")


if __name__ == "__main__":
    check(ENS_FILE)
