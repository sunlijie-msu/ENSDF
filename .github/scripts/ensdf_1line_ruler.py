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
import sys
from dataclasses import dataclass
from typing import Callable, Dict, Optional


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


def _g_flag(ch: str) -> bool:
    return ch == ' ' or ch.isalpha() or ch in {'*', '&', '@'}


def _blank_only(ch: str) -> bool:
    return ch == ' '


RECORD_DEFINITIONS: Dict[str, RecordDefinition] = {
    'H': RecordDefinition(
        label='Header record (H)',
        fmt='H-Fmt: 35XX  H metadata...                                                        ',
        fields='H-Fld: NUCID(1-5)|CONT(6)|BLANK(7)|H(8)|BLANK(9)|...metadata fields...             ',
        col77_hint='Column 77 must be blank for H records',
        col80_hint='Column 80 must be blank for H records',
        col77_validator=_blank_only,
        col80_validator=_blank_only,
    ),
    'L': RecordDefinition(
        label='Level record (L)',
        fmt='L-Fmt: 35XX  L EEEE.E    DE JP               T         DT    L        S         DSC  Q',
        fields='L-Fld: NUCID(1-5)|CONT(6)|BLANK(7)|L(8)|BLANK(9)|E(10-19)|DE(20-21)|SPACE(22)|J-pi(23-39)|T(40-49)|DT(50-55)|L(56-64)|S(65-74)|DS(75-76)|C(77)|BLANK(78-79)|Q(80)',
        col77_hint='Column 77 may hold alphabetic comment flags only',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_alpha_or_space,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'G': RecordDefinition(
        label='Gamma record (G)',
        fmt='G-Fmt: 35XX  G EEEE.E    DE II.I   DI MUL      MR      DMR   CC     DC TI       DTC  Q',
        fields='G-Fld: NUCID(1-5)|CONT(6)|BLANK(7)|G(8)|BLANK(9)|E(10-19)|DE(20-21)|SPACE(22)|RI(23-29)|DRI(30-31)|SPACE(32)|M(33-41)|MR(42-49)|DMR(50-55)|CC(56-62)|DCC(63-64)|TI(65-74)|DTI(75-76)|C(77)|BLANK(78-79)|Q(80)',
        col77_hint='Column 77: space, alphabetic, *, &, @ only',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_g_flag,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'E': RecordDefinition(
        label='Electron capture record (E)',
        fmt='E-Fmt: 35XX  E EEEE.E   DE  IB     DIB IE     DIE LOGFT   DFT    TI       DTI C UN  Q',
        fields='E-Fld: NUCID(1-5)|CONT(6)|BLANK(7)|E(8)|BLANK(9)|E(10-19)|DE(20-21)|IB(22-29)|DIB(30-31)|IE(32-39)|DIE(40-41)|LOGFT(42-49)|DFT(50-55)|BLANK(56-64)|TI(65-74)|DTI(75-76)|C(77)|UN(78-79)|Q(80)',
        col77_hint='Column 77 alphabetic comment flag (C = coincidence, etc.)',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_alpha_or_space,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
    'B': RecordDefinition(
        label='Beta-minus record (B)',
        fmt='B-Fmt: 35XX  B EEEE.E   DE  IB     DIB          LOGFT   DFT              C   UN  Q',
        fields='B-Fld: NUCID(1-5)|CONT(6)|BLANK(7)|B(8)|BLANK(9)|E(10-19)|DE(20-21)|IB(22-29)|DIB(30-31)|BLANK(32-41)|LOGFT(42-49)|DFT(50-55)|BLANK(56-76)|C(77)|UN(78-79)|Q(80)',
        col77_hint='Column 77 alphabetic comment flag',
        col80_hint='Column 80: space, ? only',
        col77_validator=_alpha_or_space,
        col80_validator=lambda ch: ch in {' ', '?'},
    ),
    'DP': RecordDefinition(
        label='Delayed particle record (DP)',
        fmt='DP-Fmt:35XX  DP EP       DE IP     DIP EI',
        fields='DP-Fld: NUCID(1-5)|CONT(6)|BLANK(7)|D(8)|P(9)|BLANK(10)|EP(11-19)|DE(20-21)|BLANK(22)|IP(23-29)|DIP(30-31)|BLANK(32)|EI(33-39)',
        col77_hint='Column 77 blank for DP records',
        col80_hint='Column 80: space, ?, S only',
        col77_validator=_blank_only,
        col80_validator=lambda ch: ch in {' ', '?', 'S'},
    ),
}


def _record_key(line: str) -> Optional[str]:
    if len(line) < 8:
        return None
    base = line[7]
    if base == 'D' and len(line) >= 9 and line[8] == 'P':
        return 'DP'
    return base


def _is_primary_data_record(line: str) -> bool:
    return len(line) > 6 and line[6] == ' '


def _is_comment_record(line: str) -> bool:
    return len(line) > 6 and line[6] in {'c', 'C'}


def _describe_comment(line: str) -> Optional[str]:
    if _is_comment_record(line):
        target = line[7] if len(line) > 7 else '?'
        return f'Comment record referencing "{target}" data block'
    return None

def print_ruler(line: str, label: Optional[str] = None) -> bool:
    """Print ENSDF 80-column ruler with format specifications for validation."""

    print('ENSDF 80-Column Ruler:')
    print('Ones: 12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('Tens: 1111111111222222222233333333334444444444555555555566666666667777777777888888888999')
    
    record_key = _record_key(line)
    record_def = RECORD_DEFINITIONS.get(record_key)
    comment_hint = _describe_comment(line)
    is_comment = comment_hint is not None

    if record_def:
        print(record_def.fmt)
        print(record_def.fields)
    if comment_hint:
        print(comment_hint)
        print('Comment lines must still obey the 80-column rule and inherit the associated record scope.')
    elif record_key and not record_def:
        print(f'Unknown record type "{record_key}" (Column 8).')

    if label:
        print(f'Line ({label}): {line}')
    else:
        print(f'Line: {line}')
    print(f'Len:  {len(line)} chars')
    
    # Quick validation
    errors = []
    if len(line) != 80:
        errors.append(f'Length {len(line)} ≠ 80')
    if '\t' in line:
        errors.append('Tab character present. ENSDF records must use spaces only.')
    
    if record_key and not record_def and not is_comment:
        errors.append(f'Unknown/Invalid record type "{record_key}" at Column 8.')
        # Specific heuristic for shifted comments
        if len(line) > 7 and line[7] in {'c', 'C'} and line[6] == ' ':
            errors.append('HINT: Found "c" in Column 8. Comment flags must be in Column 7.')

    if record_def and _is_primary_data_record(line):
        col_77 = line[76] if len(line) > 76 else ' '
        col_80 = line[79] if len(line) > 79 else ' '

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
        valid_col76 = {' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T'} # T for LT/GT
        if col_76 not in valid_col76:
            errors.append(f'Col 76: "{col_76}" invalid. Expected digit, space, or "T" (for LT/GT). Possible shifted flag?')

        if not record_def.col77_validator(col_77):
            errors.append(f'Col 77: "{col_77}" invalid — {record_def.col77_hint}')
        if not record_def.col80_validator(col_80):
            errors.append(f'Col 80: "{col_80}" invalid — {record_def.col80_hint}')
    elif record_def and len(line) >= 8 and not _is_primary_data_record(line) and not is_comment:
        errors.append('Column 7 must be blank for data records (found continuation/comment marker).')
    
    if errors:
        print(f'[ERROR] {" | ".join(errors)}')
        return False
    else:
        print('[OK]')
        return True


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
        # Check ALL record types (H, L, G, E, B, DP records)
        # ENSDF standard: ALL record types must be exactly 80 characters
        if len(line) >= 8 and line[7] in ['H', 'L', 'G', 'E', 'B', 'D']:
            total_checked += 1
            if show_only_wrong:
                if not print_ruler(line, label=f'{filename}:{lineno}'):
                    error_count += 1
                    print(f'Line {lineno}: {line}')
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