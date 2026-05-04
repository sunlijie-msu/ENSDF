"""
check_cl34_gamma_refs.py
Cross-check Cl34-format cL J$ gamma references against data records.
Format: ENERGY|g[, MULT[, |DJ=N]] (to|from) JPI[, LEVEL_E[ level]]
"""
import re, sys
from pathlib import Path

ENS_FILE = Path(r"A34\Cl34\new\Cl34_adopted.ens")

# ---------------------------------------------------------------------------
# Parse data records
# ---------------------------------------------------------------------------
def parse_file(path):
    levels = {}   # E_float -> {j, line_no}
    gammas = {}   # (parent_E, gamma_E) -> {mult, line_no}
    cur_parent = None
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    for i, line in enumerate(lines, 1):
        if len(line) < 10:
            continue
        col6 = line[5:6]    # continuation
        col8 = line[7:8]    # record type
        if col6 != ' ':
            continue
        if col8 == 'L':
            e_str = line[9:19].strip()
            j_str = line[22:39].strip()
            try:
                e = float(e_str)
                levels[e] = {'j': j_str, 'line': i}
                cur_parent = e
            except ValueError:
                pass
        elif col8 == 'G' and cur_parent is not None:
            e_str = line[9:19].strip()
            m_str = line[32:41].strip()
            try:
                e = float(e_str)
                gammas.setdefault(cur_parent, {})[e] = {'mult': m_str, 'line': i}
            except ValueError:
                pass
    return levels, gammas


def find_level(levels, energy_str):
    """Find closest level within 1.5 keV of given string."""
    try:
        target = float(energy_str)
    except ValueError:
        return None
    candidates = [(abs(e - target), e) for e in levels]
    if not candidates:
        return None
    diff, best = min(candidates)
    if diff <= 1.5:
        return best
    return None


def find_gamma(gammas, parent_e, gamma_str):
    """Find closest gamma within 2 keV of given string."""
    try:
        target = float(gamma_str)
    except ValueError:
        return None
    if parent_e not in gammas:
        return None
    candidates = [(abs(e - target), e) for e in gammas[parent_e]]
    if not candidates:
        return None
    diff, best = min(candidates)
    if diff <= 2.0:
        return best
    return None


# ---------------------------------------------------------------------------
# Extract cL J$ comment blocks with parent level
# ---------------------------------------------------------------------------
def extract_comment_blocks(path):
    """Yield (parent_e, cL_lineno, full_text) for each J$ block."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    cur_level = None
    in_j = False
    block_text = ""
    block_start = 0

    for i, line in enumerate(lines, 1):
        if len(line) < 10:
            if in_j:
                yield (cur_level, block_start, block_text)
                in_j = False
                block_text = ""
            continue
        col6 = line[5:6]
        col8 = line[7:8]
        is_cL = col8 == 'L' and line[6:7] == 'c' and col6 == ' '
        is_data_L = col6 == ' ' and col8 == 'L' and line[6:7] == ' '

        if is_data_L:
            if in_j:
                yield (cur_level, block_start, block_text)
                in_j = False
                block_text = ""
            e_str = line[9:19].strip()
            try:
                cur_level = float(e_str)
            except ValueError:
                cur_level = None

        elif is_cL:
            text = line[9:80].rstrip('\n') if len(line) >= 10 else ''
            if 'J$' in text:
                if in_j:
                    yield (cur_level, block_start, block_text)
                in_j = True
                block_text = text
                block_start = i
            elif in_j:
                block_text += ' ' + text.strip()
        else:
            if in_j:
                yield (cur_level, block_start, block_text)
                in_j = False
                block_text = ""

    if in_j:
        yield (cur_level, block_start, block_text)


# ---------------------------------------------------------------------------
# Regex for Cl34-format gamma references
# ---------------------------------------------------------------------------
# Match: ENERGY|g[, MULT[,|DJ=...]] (to|from) JPI[, LEVEL_E (level)?|g.s.]
GAMMA_REF = re.compile(
    r'(\d+(?:\.\d+)?)'                           # 1: gamma energy (must be directly adjacent)
    r'\|g'                                        # NO \s* — direct adjacency excludes |DJ=N |g
    r'(?:\s*,\s*([A-Za-z0-9+\(\)\[\]]+))?'       # 2: optional multipolarity
    r'(?:\s*,\s*\|DJ=[^\s,;]+)?'                 # optional |DJ clause
    r'(?:\s*(?:,\s*)?(?:\|g\s+)?)'               # optional standalone |g before to/from
    r'(to|from)'                                  # 3: direction
    r'\s+'
    r'([^\s,;]+(?:\s*[±(][^,;]*[±)])?[^\s,;-]*)' # 4: J-pi
    r'(?:\s*,\s*'
    r'(g\.s\.|\d+(?:\.\d+)?)(?:\s+level)?)?'    # 5: level (g.s. or number)
)


def check_refs(path):
    levels, gammas = parse_file(path)
    errors = []
    warnings = []
    checked = 0

    for parent_e, lineno, text in extract_comment_blocks(path):
        if parent_e is None:
            continue
        after_dollar = text[text.index('J$') + 2:]
        for m in GAMMA_REF.finditer(after_dollar):
            ge_str = m.group(1)
            mult_str = m.group(2)
            direction = m.group(3)
            jpi_str = m.group(4).strip().rstrip('.,;')
            lev_capture = m.group(5)  # "g.s." or numeric or None

            checked += 1

            # 1. Find the level that owns this gamma
            # 'to'   → gamma is in G-records of parent_e (deexciting)
            # 'from' → gamma is in G-records of the feeding level (lev_capture)
            if direction == 'to':
                lookup_parent = parent_e
            else:
                # For 'from', look up feeding level from lev_capture
                if lev_capture and lev_capture != 'g.s.':
                    feeding_e = find_level(levels, lev_capture)
                    lookup_parent = feeding_e  # may be None if resonance not in file
                else:
                    lookup_parent = None

            matched_ge = find_gamma(gammas, lookup_parent, ge_str) if lookup_parent is not None else None
            if matched_ge is None:
                if direction == 'from':
                    # Feeding gammas from resonances may legitimately not be in the file
                    warnings.append(
                        f"Line {lineno} (parent={parent_e}): FEEDING_GAMMA_NOT_FOUND "
                        f"quoted={ge_str}|g from {lev_capture} — not in G-records "
                        f"(may be a resonance or primary transition)"
                    )
                else:
                    errors.append(
                        f"Line {lineno} (parent={parent_e}): GAMMA_NOT_FOUND "
                        f"quoted={ge_str}|g — not in G-records for this level"
                    )
                # Still do energy conservation if level info is present
            else:
                # 2. Check multipolarity matches
                if mult_str:
                    rec_mult = gammas[lookup_parent][matched_ge]['mult']
                    # Strip brackets for comparison
                    clean_rec = rec_mult.strip('[]() ')
                    clean_cmt = mult_str.strip('[]() ')
                    if clean_rec != clean_cmt:
                        errors.append(
                            f"Line {lineno} (parent={parent_e}): MULTIPOLARITY_MISMATCH "
                            f"quoted={mult_str!r} record={rec_mult!r} for {ge_str}|g"
                        )

            # 3. Check level energy if given
            if lev_capture and lev_capture != 'g.s.':
                matched_le = find_level(levels, lev_capture)
                if matched_le is None:
                    errors.append(
                        f"Line {lineno} (parent={parent_e}): LEVEL_NOT_FOUND "
                        f"quoted={lev_capture} — no L-record within 1.5 keV"
                    )
                else:
                    # Check level Jpi
                    rec_jpi = levels[matched_le]['j']
                    # Normalize: remove trailing spaces
                    norm_rec = rec_jpi.strip()
                    norm_cmt = jpi_str.strip()
                    if norm_rec != norm_cmt:
                        errors.append(
                            f"Line {lineno} (parent={parent_e}): JPI_MISMATCH "
                            f"quoted={norm_cmt!r} record={norm_rec!r} "
                            f"for level E={matched_le}"
                        )
                    # Energy conservation
                    if direction == 'to':
                        expected_ge = parent_e - matched_le
                    else:  # from
                        expected_ge = matched_le - parent_e
                    try:
                        actual_ge = float(ge_str)
                        deviation = abs(actual_ge - expected_ge)
                        if deviation > 5.0:
                            errors.append(
                                f"Line {lineno} (parent={parent_e}): ENERGY_CONSERVATION_ERROR "
                                f"{ge_str}|g {direction} {lev_capture}: "
                                f"expected≈{expected_ge:.1f}, deviation={deviation:.1f} keV"
                            )
                        elif deviation > 2.0:
                            warnings.append(
                                f"Line {lineno} (parent={parent_e}): ENERGY_CONSERVATION_WARNING "
                                f"{ge_str}|g {direction} {lev_capture}: "
                                f"expected≈{expected_ge:.1f}, deviation={deviation:.1f} keV"
                            )
                    except ValueError:
                        pass

            elif lev_capture == 'g.s.':
                # Energy conservation with g.s. = 0.0
                if direction == 'to':
                    expected_ge = parent_e
                else:
                    expected_ge = -parent_e
                try:
                    actual_ge = float(ge_str)
                    deviation = abs(actual_ge - expected_ge)
                    if deviation > 5.0:
                        errors.append(
                            f"Line {lineno} (parent={parent_e}): ENERGY_CONSERVATION_ERROR "
                            f"{ge_str}|g {direction} g.s.: "
                            f"expected≈{expected_ge:.1f}, deviation={deviation:.1f} keV"
                        )
                    elif deviation > 2.0:
                        warnings.append(
                            f"Line {lineno} (parent={parent_e}): ENERGY_CONSERVATION_WARNING "
                            f"{ge_str}|g {direction} g.s.: "
                            f"expected≈{expected_ge:.1f}, deviation={deviation:.1f} keV"
                        )
                except ValueError:
                    pass

    print(f"\nChecked {checked} gamma references in cL J$ comments.\n")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(" ", w)
        print()
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(" ", e)
        sys.exit(1)
    else:
        print("RESULT: All quoted gamma references match records within tolerance.")


if __name__ == "__main__":
    check_refs(ENS_FILE)
