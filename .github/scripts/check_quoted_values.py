#!/usr/bin/env python3
"""
ENSDF Comment Quoted Values Cross-Check

Cross-checks all quoted values in cL J$ comments against corresponding
L-record and G-record data fields. Detects discrepancies in:

  1. Gamma energies  — quoted |g energy vs. G-record E field
  2. Multipolarities — quoted multipolarity vs. G-record M field (cols 33-41)
  3. Level energies  — quoted level energy vs. L-record E field
  4. J-pi notation   — quoted J-pi vs. L-record J field (cols 23-39)

ENSDF CONVENTIONS RECOGNIZED:

  Ground state notation (g.s.):
    - Comments use g.s. to denote ground state transitions
    - Data fields record ground state energy as 0.0 keV
    - These are semantically equivalent: no error flagged for g.s. vs 0.0

This script is read-only: it never modifies any files.

Usage:
    python check_quoted_values.py <file.ens>
    python check_quoted_values.py <file.ens> --tolerance 2.0
    python check_quoted_values.py <file.ens> --debug
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# ANSI colour helpers (degrade gracefully when piped)
# ---------------------------------------------------------------------------
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class Level:
    """ENSDF level parsed from an L-record."""
    energy: float
    energy_str: str        # original string (preserves trailing zeros)
    jpi: str               # spin-parity as written in cols 23-39
    line_num: int

    def __repr__(self) -> str:
        return f"Level({self.energy_str}, {self.jpi!r}, line {self.line_num})"


@dataclass
class Gamma:
    """ENSDF gamma transition parsed from a G-record."""
    energy: float
    energy_str: str        # original string
    multipolarity: str     # cols 33-41, stripped
    parent_energy: float   # energy of the parent level
    line_num: int

    def __repr__(self) -> str:
        return (f"Gamma({self.energy_str}, M={self.multipolarity!r}, "
                f"parent={self.parent_energy}, line {self.line_num})")


@dataclass
class QuotedRef:
    """A single quoted reference extracted from a cL J$ comment block."""
    gamma_energy_str: str               # e.g. "1824.7"
    gamma_energy: float
    multipolarity: Optional[str]        # e.g. "M1+E2" or None
    direction: str                      # "from" or "to"
    level_energy_str: str               # e.g. "1991" or "g.s."
    level_energy: Optional[float]       # None when "g.s."
    jpi: str                            # e.g. "7/2-"
    line_num: int                       # starting line of cL J$ block
    context: str                        # matched text snippet


@dataclass
class Finding:
    """A single verification finding."""
    code: str              # e.g. GAMMA_NOT_FOUND, JPI_MISMATCH
    severity: str          # "ERROR" or "INFO"
    line: int
    context: str
    message: str
    quoted: str = ""
    actual: str = ""
    diff_kev: Optional[float] = None


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------
def parse_levels(filepath: Path) -> Dict[float, Level]:
    """Parse all L-records and build {energy: Level} dictionary."""
    levels: Dict[float, Level] = {}
    with open(filepath, 'r', encoding='utf-8') as fh:
        for i, line in enumerate(fh, start=1):
            if len(line) < 10:
                continue
            # Data L-record: col 6 blank, col 7 blank, col 8 = 'L'
            col6 = line[5:6]   # continuation marker
            col7 = line[6:7]   # must be blank for data records
            col8 = line[7:8]   # record type
            if col6 != ' ' or col7 != ' ' or col8 != 'L':
                continue
            nucid = line[0:5]
            if not nucid.strip():
                continue
            energy_str = line[9:19].strip()
            if not energy_str:
                continue
            try:
                energy = float(energy_str)
            except ValueError:
                continue
            jpi = line[22:39].strip() if len(line) > 39 else line[22:].strip()
            levels[energy] = Level(energy, energy_str, jpi, i)
    return levels


def parse_gammas(filepath: Path, *, debug: bool = False) -> List[Gamma]:
    """Parse all G-records and build list of Gamma objects."""
    gammas: List[Gamma] = []
    current_level_energy: Optional[float] = None
    with open(filepath, 'r', encoding='utf-8') as fh:
        for i, line in enumerate(fh, start=1):
            if len(line) < 10:
                continue
            col6 = line[5:6]
            col7 = line[6:7]
            col8 = line[7:8]
            nucid = line[0:5]
            if not nucid.strip():
                continue
            # L-record: track parent level energy
            if col6 == ' ' and col7 == ' ' and col8 == 'L':
                e_str = line[9:19].strip()
                if e_str:
                    try:
                        current_level_energy = float(e_str)
                    except ValueError:
                        current_level_energy = None
                if debug:
                    print(f"  L-rec line {i}: level={current_level_energy}")
                continue
            # G-record
            if col6 == ' ' and col7 == ' ' and col8 == 'G':
                if current_level_energy is None:
                    continue
                e_str = line[9:19].strip()
                if not e_str:
                    continue
                try:
                    energy = float(e_str)
                except ValueError:
                    continue
                mul = line[32:41].strip() if len(line) > 41 else ''
                gammas.append(Gamma(energy, e_str, mul, current_level_energy, i))
                if debug:
                    print(f"  G-rec line {i}: E={e_str}  M={mul!r}  parent={current_level_energy}")
    return gammas


# ---------------------------------------------------------------------------
# cL J$ comment extraction
# ---------------------------------------------------------------------------
def extract_quoted_refs(filepath: Path) -> List[QuotedRef]:
    """Extract all quoted gamma/level references from cL J$ comment blocks."""
    refs: List[QuotedRef] = []
    with open(filepath, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()

    in_j_block = False
    block_lines: List[str] = []
    block_start = 0

    def flush_block() -> None:
        if block_lines:
            refs.extend(_parse_j_block(block_lines, block_start))

    for i, line in enumerate(lines, start=1):
        if len(line) < 10:
            if in_j_block:
                flush_block()
                in_j_block = False
                block_lines = []
            continue
        col7 = line[6:7]
        col8 = line[7:8]
        nucid = line[0:5]
        is_cL = col7 == 'c' and col8 == 'L' and nucid.strip() != ''
        if is_cL:
            text = line[9:80] if len(line) >= 80 else line[9:].rstrip('\n')
            if 'J$' in text:
                # New J$ block
                if in_j_block:
                    flush_block()
                in_j_block = True
                block_lines = [text]
                block_start = i
            elif in_j_block:
                # Continuation of current J$ block
                block_lines.append(text)
        else:
            if in_j_block:
                flush_block()
                in_j_block = False
                block_lines = []

    # End of file
    if in_j_block:
        flush_block()
    return refs


def _parse_j_block(texts: List[str], start_line: int) -> List[QuotedRef]:
    """Parse a merged cL J$ text block into QuotedRef objects."""
    full = ''.join(texts)
    results: List[QuotedRef] = []

    # Pattern: [MULTIPOLARITY] ENERGY|g (from|to) JPI (LEVEL_ENERGY|g.s.)
    pattern = (
        r'(?:([A-Z0-9+\(\)\[\]]+)\s+)?'  # group 1: optional multipolarity at start
        r'(\d+(?:\.\d+)?)\s*\|g'          # group 2: gamma energy (allow space before |g)
        r'\s+'
        r'(from|to)'                       # group 3: direction
        r'\s+'
        r'([^\s,;]+(?:\s*\([^\)]*\))?[^\s,;-]*)'  # group 4: J-pi
        r'\s+'
        r'(g\.s\.|(\d+(?:\.\d+)?))(?:-keV)?(?:\s+level)?'  # group 5: level (g.s. or number), group 6: numeric part
    )

    for m in re.finditer(pattern, full):
        mul = m.group(1).strip() if m.group(1) else None
        ge_str = m.group(2)
        direction = m.group(3)
        jpi = m.group(4).strip()
        lev_capture = m.group(5)  # either "g.s." or the numeric string
        if lev_capture == 'g.s.':
            lev_str = 'g.s.'
            lev_e = 0.0
        else:
            lev_str = lev_capture
            lev_e = float(lev_capture)
        
        # Clean trailing artefacts
        jpi = re.sub(r'[;,.]$', '', jpi)

        results.append(QuotedRef(
            gamma_energy_str=ge_str,
            gamma_energy=float(ge_str),
            multipolarity=mul,
            direction=direction,
            level_energy_str=lev_str,
            level_energy=lev_e,
            jpi=jpi,
            line_num=start_line,
            context=m.group(0),
        ))
    return results


# ---------------------------------------------------------------------------
# Record look-up helpers
# ---------------------------------------------------------------------------
def find_closest_level(levels: Dict[float, Level], energy: float,
                       window: float) -> Optional[Level]:
    """Return the closest Level within *window* keV, or None."""
    best: Optional[Level] = None
    best_diff = float('inf')
    for e, lvl in levels.items():
        d = abs(e - energy)
        if d <= window and d < best_diff:
            best_diff = d
            best = lvl
    return best


def find_closest_gamma(gammas: List[Gamma], energy: float,
                       window: float) -> Optional[Gamma]:
    """Return the closest Gamma within *window* keV, or None."""
    best: Optional[Gamma] = None
    best_diff = float('inf')
    for g in gammas:
        d = abs(g.energy - energy)
        if d <= window and d < best_diff:
            best_diff = d
            best = g
    return best


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
_EPS = 1e-6   # floating-point equality threshold


def verify(refs: List[QuotedRef], levels: Dict[float, Level],
           gammas: List[Gamma], window: float) -> List[Finding]:
    """Cross-check every QuotedRef against L/G-records."""
    findings: List[Finding] = []

    for ref in refs:
        # --- Gamma energy ---
        g = find_closest_gamma(gammas, ref.gamma_energy, window)
        if g is None:
            findings.append(Finding(
                code='GAMMA_NOT_FOUND', severity='ERROR',
                line=ref.line_num, context=ref.context,
                message=f'No G-record within {window} keV of '
                        f'{ref.gamma_energy_str} keV',
                quoted=ref.gamma_energy_str,
            ))
        else:
            # Gamma energy must match EXACTLY character-for-character
            if g.energy_str != ref.gamma_energy_str:
                findings.append(Finding(
                    code='GAMMA_ENERGY_MISMATCH', severity='ERROR',
                    line=ref.line_num, context=ref.context,
                    message=(f'Quoted "{ref.gamma_energy_str}" keV, '
                             f'G-record has "{g.energy_str}" keV'),
                    quoted=ref.gamma_energy_str,
                    actual=g.energy_str,
                    diff_kev=abs(g.energy - ref.gamma_energy),
                ))
            # else: exact match — no finding needed

        # --- Multipolarity ---
        if ref.multipolarity is not None and g is not None:
            if g.multipolarity != ref.multipolarity:
                findings.append(Finding(
                    code='MULTIPOLARITY_MISMATCH', severity='ERROR',
                    line=ref.line_num, context=ref.context,
                    message=(f'Quoted "{ref.multipolarity}", '
                             f'G-record M field is "{g.multipolarity}"'),
                    quoted=ref.multipolarity,
                    actual=g.multipolarity,
                ))

        # --- Level energy ---
        if ref.level_energy is not None:
            lvl = find_closest_level(levels, ref.level_energy, window)
            if lvl is None:
                findings.append(Finding(
                    code='LEVEL_NOT_FOUND', severity='ERROR',
                    line=ref.line_num, context=ref.context,
                    message=(f'No L-record within {window} keV of '
                             f'{ref.level_energy_str} keV'),
                    quoted=ref.level_energy_str,
                ))
            else:
                # Level energy must match EXACTLY character-for-character
                # EXCEPTION: g.s. notation in comments is equivalent to 0.0 in data
                # (ENSDF convention: ground state written as g.s. in comments)
                is_ground_state_match = (
                    ref.level_energy_str == 'g.s.' and lvl.energy_str == '0.0'
                )
                if not is_ground_state_match and lvl.energy_str != ref.level_energy_str:
                    findings.append(Finding(
                        code='LEVEL_ENERGY_MISMATCH', severity='ERROR',
                        line=ref.line_num, context=ref.context,
                        message=(f'Quoted "{ref.level_energy_str}" keV, '
                                 f'L-record has "{lvl.energy_str}" keV'),
                        quoted=ref.level_energy_str,
                        actual=lvl.energy_str,
                        diff_kev=abs(lvl.energy - ref.level_energy),
                    ))
                # Check J-pi against this level
                if lvl.jpi != ref.jpi:
                    findings.append(Finding(
                        code='JPI_MISMATCH', severity='ERROR',
                        line=ref.line_num, context=ref.context,
                        message=(f'Quoted J-pi "{ref.jpi}", '
                                 f'L-record J field is "{lvl.jpi}"'),
                        quoted=ref.jpi,
                        actual=lvl.jpi,
                    ))
        elif ref.level_energy_str == 'g.s.':
            # Ground state: find level at 0 keV
            lvl = find_closest_level(levels, 0.0, window)
            if lvl is not None and lvl.jpi != ref.jpi:
                findings.append(Finding(
                    code='JPI_MISMATCH', severity='ERROR',
                    line=ref.line_num, context=ref.context,
                    message=(f'Quoted J-pi "{ref.jpi}" for g.s., '
                             f'L-record J field is "{lvl.jpi}"'),
                    quoted=ref.jpi,
                    actual=lvl.jpi,
                ))

    return findings


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def print_report(filepath: Path, findings: List[Finding],
                 n_refs: int, n_levels: int, n_gammas: int) -> None:
    """Print human-readable verification report."""
    errors = [f for f in findings if f.severity == 'ERROR']
    infos  = [f for f in findings if f.severity == 'INFO']

    print()
    print('=' * 80)
    print(f'{BOLD}ENSDF Comment Quoted Values Cross-Check Report{RESET}')
    print(f'File: {filepath}')
    print(f'Levels: {n_levels}   Gammas: {n_gammas}   '
          f'Quoted references: {n_refs}')
    print('=' * 80)
    print()
    print(f'  ERRORS: {len(errors)}')
    print()

    if errors:
        print('-' * 80)
        print(f'{RED}{BOLD}ERRORS{RESET}')
        print('-' * 80)
        for i, f in enumerate(errors, 1):
            print(f'  {RED}#{i} [{f.code}]{RESET}  line {f.line}')
            print(f'      {f.message}')
            print(f'      Context: {f.context}')
            print()

    print('=' * 80)
    if errors:
        print(f'{RED}RESULT: {len(errors)} error(s) found — all must be fixed{RESET}')
    else:
        print(f'{GREEN}RESULT: All quoted values match records exactly.{RESET}')
    print('=' * 80)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description='Cross-check quoted values in ENSDF cL J$ comments '
                    'against L-record and G-record data fields.',
    )
    p.add_argument('file', type=Path,
                   help='Path to the ENSDF .ens file')
    p.add_argument('--tolerance', type=float, default=1.0,
                   metavar='KEV',
                   help='Search window in keV for finding matching records '
                        '(default: 1.0). Does NOT define acceptance criteria.')
    p.add_argument('--debug', action='store_true',
                   help='Print verbose parser diagnostics')
    return p


def main() -> None:
    args = build_parser().parse_args()
    filepath: Path = args.file
    window: float = args.tolerance

    if not filepath.exists():
        print(f'Error: file not found: {filepath}', file=sys.stderr)
        sys.exit(2)

    # Parse data records
    print(f'Parsing {filepath.name} ...')
    levels = parse_levels(filepath)
    gammas = parse_gammas(filepath, debug=args.debug)
    print(f'  Levels: {len(levels)}    Gammas: {len(gammas)}')

    # Extract quoted references from cL J$ comments
    refs = extract_quoted_refs(filepath)
    print(f'  Quoted references: {len(refs)}')

    # Verify
    findings = verify(refs, levels, gammas, window)

    # Report
    print_report(filepath, findings, len(refs), len(levels), len(gammas))

    # Exit code: 1 if errors, 0 otherwise
    has_errors = any(f.severity == 'ERROR' for f in findings)
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
