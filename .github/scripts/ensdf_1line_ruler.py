#!/usr/bin/env python3
"""
ENSDF 80-Column Ruler - Simple Visual Verification Tool

🎯 PURPOSE: Quick visual verification of ENSDF 80-column positioning
🎯 USE FREQUENTLY: Before edit, during edit, after edit for AI self-diagnostics
🎯 CRITICAL: Prevents column positioning errors that break ENSDF format

USAGE:
  python ensdf_1line_ruler.py --line "your 80-char line"
  python ensdf_1line_ruler.py --file "filename.ens"
"""

from __future__ import annotations

import argparse
import io
import sys
from dataclasses import dataclass
from typing import Callable, Dict, Optional

# Column 7 holds a flag on comment-style records, which may be continued ('2c', '2d', ...):
#   'c'/'C' -> comment record
#   'd'/'D' -> hidden message record (kept in the file, ignored by the processing codes);
#              free-format note, so the 80-column length rule is not enforced for these.
# Any other character in Column 7 is invalid.
COMMENT_FLAGS = {'c': 'comment', 'C': 'comment',
                 'd': 'hidden message', 'D': 'hidden message'}

# Other column-7 flags emitted by processing/plotting tooling. Their lines are free-form
# text, so the column-77/80 field checks are skipped (the 80-column rule still applies):
#   't' -> table/plot text
#   'P' -> dataset parent/normalization record, whose "PN" type occupies columns 7-8
OTHER_COL7_FLAGS = {'t': 'table/plot text',
                    'P': 'dataset parent/normalization ("PN" record)'}


@dataclass(frozen=True)
class RecordDefinition:
    """Metadata plus validation hooks for a specific ENSDF record type."""

    label: str
    fmt: str
    fields: str
    col77_hint: str
    col80_hint: str
    col77_validator: Callable[[str], bool]
    col80_validator: Callable[[str], bool]


def _alpha_or_space(ch: str) -> bool:
    return ch == ' ' or ch.isalpha()


def _comment_flag_field(ch: str) -> bool:
    """C field (column 77): space, alphabetic comment flag, or multiply-placed marker."""
    return ch == ' ' or ch.isalpha() or ch in {'*', '&', '@'}


def _blank_only(ch: str) -> bool:
    return ch == ' '


def _pad_record_example(text: str) -> str:
    return text.ljust(80)


# Delayed-particle records share one layout; only the particle letter in column 9 differs.
DELAYED_PARTICLES = {
    'P': ('Delayed proton record (DP)', 'proton', 'EP', 'IP'),
    'N': ('Delayed neutron record (DN)', 'neutron', 'EN', 'IN'),
    'A': ('Delayed alpha record (DA)', 'alpha', 'EA', 'IA'),
    'D': ('Delayed deuteron record (DD)', 'deuteron', 'ED', 'ID'),
    'T': ('Delayed triton record (DT)', 'triton', 'ET', 'IT'),
}


def _delayed_particle_definition(letter: str) -> RecordDefinition:
    label, particle, e_field, i_field = DELAYED_PARTICLES[letter]
    return RecordDefinition(
        label=label,
        fmt=_pad_record_example(f' 35XX  D{letter} {e_field:<9} DE {i_field:<6} DI EI'),
        fields=(f'NUCID(1-5)|CONT(6)|BLANK(7)|D(8)|{letter}(9)|BLANK(10)|{e_field}(11-19)'
                f'|DE(20-21)|BLANK(22)|{i_field}(23-29)|DI(30-31)|BLANK(32)|EI(33-39)'
                '|BLANK(40-76)|C(77)|BLANK(78-79)|Q(80)'),
        col77_hint=(f'Column 77: space, alphabetic comment flag, *, &, @ only '
                    f'(cD{letter} ...$ identifiers name the flag)'),
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_comment_flag_field,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    )


RECORD_DEFINITIONS: Dict[str, RecordDefinition] = {
    'H': RecordDefinition(
        label='Header record (H)',
        fmt=_pad_record_example(' 35XX  H metadata...'),
        fields='NUCID(1-5)|CONT(6)|BLANK(7)|H(8)|BLANK(9)|...metadata fields...             ',
        col77_hint='Column 77 must be blank for H records',
        col80_hint='Column 80 must be blank for H records',
        col77_validator=_blank_only,
        col80_validator=_blank_only,
    ),
    'L': RecordDefinition(
        label='Level record (L)',
        fmt=_pad_record_example(' 35XX  L EEEE.E    DE JP               T         DT    L        S         DSC  Q'),
        fields='NUCID(1-5)|CONT(6)|BLANK(7)|L(8)|BLANK(9)|E(10-19)|DE(20-21)|SPACE(22)|J-pi(23-39)|T(40-49)|DT(50-55)|L(56-64)|S(65-74)|DS(75-76)|C(77)|BLANK(78-79)|Q(80)',
        col77_hint='Column 77 may hold alphabetic comment flags only',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_alpha_or_space,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'G': RecordDefinition(
        label='Gamma record (G)',
        fmt=_pad_record_example(' 35XX  G EEEE.E    DE II.I   DI MUL      MR      DMR   CC     DC TI       DTC  Q'),
        fields='NUCID(1-5)|CONT(6)|BLANK(7)|G(8)|BLANK(9)|E(10-19)|DE(20-21)|SPACE(22)|RI(23-29)|DRI(30-31)|SPACE(32)|M(33-41)|MR(42-49)|DMR(50-55)|CC(56-62)|DCC(63-64)|TI(65-74)|DTI(75-76)|C(77)|BLANK(78-79)|Q(80)',
        col77_hint='Column 77: space, alphabetic, *, &, @ only',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_comment_flag_field,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'E': RecordDefinition(
        label='Electron capture record (E)',
        fmt=_pad_record_example(' 35XX  E EEEE.E   DE  IB     DIB IE     DIE LOGFT   DFT    TI       DTI C UN  Q'),
        fields='NUCID(1-5)|CONT(6)|BLANK(7)|E(8)|BLANK(9)|E(10-19)|DE(20-21)|IB(22-29)|DIB(30-31)|IE(32-39)|DIE(40-41)|LOGFT(42-49)|DFT(50-55)|BLANK(56-64)|TI(65-74)|DTI(75-76)|C(77)|UN(78-79)|Q(80)',
        col77_hint='Column 77 alphabetic comment flag (C = coincidence, etc.)',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_alpha_or_space,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'B': RecordDefinition(
        label='Beta-minus record (B)',
        fmt=_pad_record_example(' 35XX  B EEEE.E   DE  IB     DIB          LOGFT   DFT              C   UN  Q'),
        fields='NUCID(1-5)|CONT(6)|BLANK(7)|B(8)|BLANK(9)|E(10-19)|DE(20-21)|IB(22-29)|DIB(30-31)|BLANK(32-41)|LOGFT(42-49)|DFT(50-55)|BLANK(56-76)|C(77)|UN(78-79)|Q(80)',
        col77_hint='Column 77 alphabetic comment flag',
        col80_hint='Column 80: space, ? only',
        col77_validator=_alpha_or_space,
        col80_validator=lambda ch: ch in {' ', '?'},
    ),
    'A': RecordDefinition(
        label='Alpha decay record (A)',
        fmt=_pad_record_example('235XX  A EEEE.E    DE IA     DI HF     DHF                                  C  Q'),
        fields='NUCID(1-5)|CONT(6)|BLANK(7)|A(8)|BLANK(9)|E(10-19)|DE(20-21)|SPACE(22)|IA(23-29)|DIA(30-31)|SPACE(32)|HF(33-39)|DHF(40-41)|BLANK(42-76)|C(77)|BLANK(78-79)|Q(80)',
        col77_hint="Column 77: alphabetic comment flag ('C' = coincidence, '?' = probable coincidence)",
        col80_hint='Column 80: space, ?, S only',
        col77_validator=lambda ch: ch == ' ' or ch.isalpha() or ch == '?',
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'PN': RecordDefinition(
        label='Dataset parent/normalization record (PN - type occupies columns 7-8)',
        fmt=_pad_record_example(' 35XX PN'),
        fields='NUCID(1-5)|CONT(6)|P(7)|N(8)|...parent/normalization fields...|C(77)|...|BLANK(80)',
        col77_hint='Column 77: space, alphabetic comment flag, *, &, @ only',
        col80_hint='Column 80 must be blank for PN records',
        col77_validator=_comment_flag_field,
        col80_validator=_blank_only,
    ),
}

# Delayed-particle family: D in column 8 with P/N/A/D/T in column 9.
for _letter in DELAYED_PARTICLES:
    RECORD_DEFINITIONS['D' + _letter] = _delayed_particle_definition(_letter)
del _letter


def _record_key(line: str) -> Optional[str]:
    if len(line) < 8:
        return None
    # Dataset parent/normalization record: type 'PN' occupies columns 7-8.
    if len(line) >= 9 and line[6] == 'P' and line[7] == 'N':
        return 'PN'
    base = line[7]
    # Delayed-particle records: D in column 8 with P/N/A/D/T in column 9.
    if base == 'D' and len(line) >= 9 and line[8] in DELAYED_PARTICLES:
        return 'D' + line[8]
    return base


def _is_primary_data_record(line: str) -> bool:
    """Primary data record: column 6 (continuation) and column 7 both blank."""
    return len(line) > 6 and line[5] == ' ' and line[6] == ' '


def _is_continuation_record(line: str) -> bool:
    """Continuation record: label in column 6, column 7 blank. Its columns 78-79 hold
    continued field data, so only the 80-column rule applies to it."""
    return len(line) > 5 and line[5] != ' ' and len(line) > 6 and line[6] == ' '


def _nucid_shifted_left(line: str) -> bool:
    """True when a 2-digit-mass NUCID lost its leading space ('34S  L ...').
    Three-digit masses (e.g. '204AT') legitimately start with a digit in column 1."""
    if len(line) < 3:
        return False
    return line[0].isdigit() and line[1].isdigit() and not line[2].isdigit()


def _is_comment_record(line: str) -> bool:
    """Comment-style records carry a flag in column 7 ('c'/'C' comment, 'd'/'D' hidden
    message) and the commented record type in column 8 (blank for a dataset-wide record)."""
    return len(line) > 6 and line[6] in COMMENT_FLAGS


def _describe_comment(line: str) -> Optional[str]:
    """Label a comment-style record, naming the column-7 flag that marks it."""
    if _is_comment_record(line):
        flag = line[6]
        target = line[7] if len(line) > 7 else ' '
        scope = f'"{target}" data block' if target.strip() else 'the whole dataset'
        return (f'{COMMENT_FLAGS[flag].capitalize()} record (flag "{flag}") '
                f'referencing {scope}')
    return None


def _is_free_text_record(line: str) -> bool:
    """'d'/'D' flagged records hold free-format notes, e.g. ' 34S  d' or
    ' 58FE DB EAV,LOGFT$...', so the 80-column rule is not enforced for them."""
    return len(line) > 6 and line[6] in {'d', 'D'}


def _is_misplaced_comment(line: str) -> bool:
    """True when a comment flag sits in column 8 instead of column 7, which makes the
    line unrecognizable; without this test a file scan silently skips it."""
    return len(line) > 7 and line[6] == ' ' and line[7] in {'c', 'C'}


def print_ruler(line: str, label: Optional[str] = None) -> bool:
    """Print ENSDF 80-column ruler with format specifications for validation."""

    print('ENSDF 80-Column Ruler:')
    print('Tens:')
    print('11111111112222222222333333333344444444445555555555666666666677777777778888888889')
    print('Ones:')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    
    record_key = _record_key(line)
    record_def = RECORD_DEFINITIONS.get(record_key)
    comment_hint = _describe_comment(line)
    is_comment = comment_hint is not None
    free_text = _is_free_text_record(line)
    # An all-space line is a legal separator, e.g. the 80-column line that ends an
    # ENSDF submission. It carries no record type and must be preserved, not flagged.
    is_blank = line.strip() == ''

    if is_blank:
        print('Blank record: all-space separator line (no record type). '
              'ENSDF submissions end with an 80-column blank line; keep it.')
    elif record_def:
        print(f'Format ({record_def.label}):')
        print(record_def.fmt)
        print('Fields (schematic):')
        print(record_def.fields)
    if comment_hint:
        print(comment_hint)
        if free_text:
            print('Hidden message (free-text) record: 80-column length is not enforced.')
        else:
            print('Comment lines must still obey the 80-column rule and inherit the associated record scope.')
    elif record_def and len(line) > 6 and line[6] in OTHER_COL7_FLAGS:
        print(f'{OTHER_COL7_FLAGS[line[6]].capitalize()} record (flag "{line[6]}"): '
              'free-form text, column-77/80 field checks are not applied.')
    elif record_key and not record_def and not is_blank:
        print(f'Unknown record type "{record_key}" (Column 8).')

    if label:
        print(f'Line ({label}):')
    else:
        print('Line:')
    print(line)
    print(f'Len:  {len(line)} chars')
    
    # Quick validation
    errors = []
    is_primary = record_def is not None and _is_primary_data_record(line)
    if len(line) != 80 and not free_text:
        errors.append(f'Length {len(line)} != 80')
    if '\t' in line:
        errors.append('Tab character present. ENSDF records must use spaces only.')
    
    if record_key and not record_def and not is_comment and not is_blank:
        errors.append(f'Unknown/Invalid record type "{record_key}" at Column 8.')
        # Specific heuristic for shifted comments
        if len(line) > 7 and line[7] in {'c', 'C'} and line[6] == ' ':
            errors.append('HINT: Found "c" in Column 8. Comment flags must be in Column 7.')
        # NUCID shift detection: if col 1 is a digit, the whole line is shifted left
        if _nucid_shifted_left(line) and len(line) < 80:
            errors.append('NUCID shifted left: Column 1 is digit "' + line[0] + '" (must be space for A<100). Whole line shifted left by 1 column.')
    elif is_comment and line[7:8].strip() and not line[7].isalpha():
        errors.append(f'Comment record has invalid commented-record-type "{line[7]}" in '
                      'Column 8. Expected blank (dataset-wide comment) or a record-type '
                      'letter such as H, L, G, B, E, A, D, or Q.')

    # Columns 8-9 hold the commented-record-type code (1-2 letters, or blanks), so the
    # comment text must start at Column 10. Free-text 'd' notes are exempt.
    if is_comment and not free_text and len(line) > 9:
        col8, col9 = line[7], line[8]
        if col8 == ' ' and col9 != ' ':
            errors.append(f'Comment text starts at Column 9 ("{col9}"). Columns 8-9 hold the '
                          'record-type code, so Column 9 must be blank and text must start at Column 10.')
        elif col8 != ' ' and not (col9.isalpha() or col9 == ' '):
            errors.append(f'Invalid commented-record-type code "{col8}{col9}" in Columns 8-9. '
                          'Codes are 1-2 letters, left-justified at Column 8.')

    if is_primary:
        col_77 = line[76] if len(line) > 76 else ' '
        col_80 = line[79] if len(line) > 79 else ' '

        # NUCID column 1 check: only 2-digit masses need a leading space in column 1
        if _nucid_shifted_left(line):
            errors.append('NUCID shifted left: Column 1 is digit "' + line[0] + '" (must be space for A<100).')

        # CRITICAL AI FIX: Check for shifted flags in Column 76 (Index 75)
        # Column 76 (part of 2-col uncertainty fields like DS, DTI) should only contain:
        # - Digits (0-9)
        # - Spaces
        # - 'T' (part of LT/GT markers)
        # - 'L' or 'G' (start of LT/GT markers - but usually L/G is at Col 75, T at 76? No, LT is 2 chars. 
        #   If at 75-76: 75=L, 76=T. If at 76-77? No field is 76-77. 
        #   Fields are 75-76. So 75 can be L/G/digit/space. 76 can be T/digit/space.
        #   If 76 has 'X', it is INVALID.
        col_76 = line[75] if len(line) > 75 else ' '
        col_75 = line[74] if len(line) > 74 else ' '
        # Column 76 closes the 2-column uncertainty field (75-76): digit, space, or the
        # second letter of a limit marker (LT, GT, LE, GE).
        valid_col76 = {' ', 'T', 'E', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        if col_76 not in valid_col76:
            errors.append(f'Col 76: "{col_76}" invalid. Expected digit, space, or "T"/"E" (for LT/GT/LE/GE). Possible shifted flag?')
        elif col_76 in 'TE' and col_75 not in 'LG':
            errors.append(f'Col 75-76: "{col_75}{col_76}" invalid. Limit markers are LT, GT, LE, GE.')

        if not record_def.col77_validator(col_77):
            errors.append(f'Col 77: "{col_77}" invalid — {record_def.col77_hint}')
        if not record_def.col80_validator(col_80):
            errors.append(f'Col 80: "{col_80}" invalid — {record_def.col80_hint}')
    elif (record_def and len(line) >= 8 and not is_comment
          and not _is_continuation_record(line)
          and not is_primary
          and line[6] not in OTHER_COL7_FLAGS):
        errors.append('Column 7 must be blank or hold a known flag ("c"/"C" comment, '
                      f'"d"/"D" hidden message, "t" table/plot text, "P" PN record); found "{line[6]}".')
    
    if errors:
        print(f'[ERROR] {" | ".join(errors)}')
        return False
    else:
        print('[OK]')
        return True


def _quiet_call(fn: Callable, *args, **kwargs):
    """Run fn with stdout suppressed and return its result."""
    buffer = io.StringIO()
    saved_stdout, sys.stdout = sys.stdout, buffer
    try:
        return fn(*args, **kwargs)
    finally:
        sys.stdout = saved_stdout


def scan_file(filename: str, show_only_wrong: bool = False, line_number: Optional[int] = None) -> bool:
    """Scan ENSDF file and check all data record lines."""

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f'[ERROR] Cannot open {filename}: {e}')
        return False
    
    if line_number is not None:
        if line_number < 1 or line_number > len(lines):
            print(f'[ERROR] Line number {line_number} is outside the file range (1-{len(lines)}).')
            return False
        target_indexes = {line_number}
    else:
        target_indexes = None

    total_checked = 0
    error_count = 0
    
    for lineno, raw_line in enumerate(lines, 1):
        if target_indexes and lineno not in target_indexes:
            continue
        line = raw_line.rstrip('\n')
        # Check ALL record types (H, L, G, E, B, A, delayed-particle and PN records)
        # ENSDF standard: ALL record types must be exactly 80 characters
        key = _record_key(line)
        if key in RECORD_DEFINITIONS or _is_misplaced_comment(line):
            total_checked += 1
            if show_only_wrong:
                if not _quiet_call(print_ruler, line, f'{filename}:{lineno}'):
                    error_count += 1
                    print(f'\nLine {lineno}:')
                    print_ruler(line, label=f'{filename}:{lineno}')
                    print('-' * 40)
            else:
                print(f'\nLine {lineno}:')
                if not print_ruler(line, label=f'{filename}:{lineno}'):
                    error_count += 1
    
    print(f'\nSummary: {total_checked} data records checked, {error_count} errors found')
    return error_count == 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ENSDF 80-column ruler - simple visual verification')
    parser.add_argument('--line', help='Verify single line (in quotes)')
    parser.add_argument('--file', help='Scan ENSDF file for data record errors')
    parser.add_argument('--line-number', type=int, help='Only inspect the specified 1-based line number in --file')
    parser.add_argument('--show-only-wrong', action='store_true', help='Show only error lines')

    args = parser.parse_args()

    if args.line and args.file:
        parser.error('Use either --line or --file, not both.')

    if args.line_number and not args.file:
        parser.error('--line-number requires --file to be specified.')

    if args.line:
        success = print_ruler(args.line)
        sys.exit(0 if success else 1)
    elif args.file:
        success = scan_file(args.file, args.show_only_wrong, args.line_number)
        sys.exit(0 if success else 1)
    else:
        print('🎯 ENSDF 80-Column Ruler Tool')
        print('Usage:')
        print('  --line "your line"     Check single line')
        print('  --file filename.ens    Check all data records in file')
        print('  --show-only-wrong      Show only error lines when scanning')
        print()
        print('💡 Use this tool FREQUENTLY during ENSDF editing:')
        print('   • BEFORE making edits (verify current state)')
        print('   • DURING editing (check each changed line)')
        print('   • AFTER editing (final validation)')
        sys.exit(0)