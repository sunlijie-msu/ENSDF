#!/usr/bin/env python3
"""
Convert plain-number uncertainties in ENSDF comment lines to {In} notation.

Only processes cL, cG comment records (primary and continuations: 2cG, 3cG, 2cL, etc.)
Preserves all data records (L, G, B, E, DP, etc.) unchanged.

Pattern: VALUE UNCERTAINTY  ->  VALUE {IUNCERTAINTY}
Example: "507.1 10 (1959Ku79)" -> "507.1 {I10} (1959Ku79)"

Algorithm:
  - Processes multi-line comment GROUPS (primary + all consecutive continuations) as units.
  - Joins the logical content, applies {I} conversion, then re-wraps to fit 80-char lines.
  - Creates new continuation records when needed; removes excess empty continuations.

Usage:
    python convert_uncertainties.py filename.ens            # dry run (shows changes)
    python convert_uncertainties.py filename.ens --write    # write changes to file
    python convert_uncertainties.py filename.ens --count    # count changed groups only
"""

import re
import sys


# ─── Constants ────────────────────────────────────────────────────────────────

MAX_CONTENT_PRIMARY = 72   # Primary line: cols 9-80 = 72 chars (8 prefix + 72 = 80)
MAX_CONTENT_CONT    = 71   # Continuation: 8 prefix + 1 space at col 9 + 71 chunk = 80


# ─── Regex pattern ────────────────────────────────────────────────────────────

# Matches:  VALUE<space>UNCERTAINTY  where:
#   VALUE: optional sign + integer [+ decimal]   e.g.  -0.12  507.1  1266  8
#   UNCERTAINTY: 1-4 plain digits
#   Delimiter after uncertainty: space, comma, semicolon, closing paren, or EOL
#
# NOT matched:
#   - Already-converted  VALUE {I...}  entries (no plain digit follows the space)
#   - FROM E(p)(lab)=1119)  (letter after space, not matched as uncertainty)
#   - NSR codes like  1977Da02  (matched pattern "1977 Da" — but "Da" is not
#     a digit, so the lookahead sees a non-delimiter and skips it correctly)
PATTERN = re.compile(
    r'([+-]?[0-9]+(?:\.[0-9]+)?)'  # Group 1: VALUE
    r' '                            # single space separator
    r'([0-9]{1,4})'                 # Group 2: UNCERTAINTY (1-4 digits)
    r'(?=[ ,;)(]|$)'                # lookahead: delimiter after uncertainty
)


def convert_content(text):
    """Replace  VALUE UNCT  patterns with  VALUE {IUNCT}  in comment text."""
    return PATTERN.sub(lambda m: f'{m.group(1)} {{I{m.group(2)}}}', text)


# ─── ENSDF line classification ────────────────────────────────────────────────

def is_comment_line(line):
    """True for any ENSDF comment record (primary OR continuation cL/cG).

    ENSDF columns (1-indexed):
      col 6 (index 5): blank=primary, digit/letter=continuation
      col 7 (index 6): 'c' for all comment records
      col 8 (index 7): 'L' or 'G' (which record type the comment applies to)
    """
    if len(line) < 8:
        return False
    return line[6] == 'c' and line[7] in ('L', 'G', 'l', 'g')


def is_primary_comment(line):
    """True only for the PRIMARY (non-continuation) comment record (col 6 blank)."""
    return is_comment_line(line) and line[5] == ' '


def is_continuation_comment(line):
    """True for continuation comment records (col 6 is digit or uppercase letter)."""
    return is_comment_line(line) and line[5] != ' '


# ─── Content wrapping ─────────────────────────────────────────────────────────

def _find_split(content, max_chars):
    """Find the last valid split position within max_chars.

    Skips any space that is immediately followed by '{' (ENSDF markup token)
    to avoid separating a value from its {Iunc} notation.
    Returns the index of the split space, or -1 if none found.
    """
    end = max_chars
    while end > 0:
        pos = content.rfind(' ', 0, end)
        if pos < 0:
            return -1
        if pos + 1 < len(content) and content[pos + 1] == '{':
            end = pos   # skip this position; look earlier
            continue
        return pos
    return -1


def wrap_into_chunks(content, max_chars_primary=MAX_CONTENT_PRIMARY,
                     max_chars_cont=MAX_CONTENT_CONT):
    """Split content into chunks fitting within the ENSDF 80-char line limit.

    Primary chunk  (index 0): up to max_chars_primary  chars  (8 + 72 = 80)
    Continuation chunks (1+): up to max_chars_cont      chars  (8 + 1 + 71 = 80)

    The leading space at col 9 for the primary record is embedded inside the
    first chunk.  Continuation chunks are stored WITHOUT a leading space here;
    a space is added by the caller when creating the physical line.

    Splits at spaces, avoiding breaks just before '{' (ENSDF markup).
    """
    chunks = []
    first = True
    while content:
        mc = max_chars_primary if first else max_chars_cont
        first = False

        if len(content) <= mc:
            chunks.append(content)
            break

        split_pos = _find_split(content, mc)
        if split_pos < 0:
            # No valid space: force-split at boundary
            chunks.append(content[:mc])
            content = content[mc:]
        else:
            chunks.append(content[:split_pos])
            content = content[split_pos + 1:]   # consume the split space

    return chunks


def continuation_marker(index):
    """Return the continuation marker character for position index in a group.

    index 0 -> ' '  (primary, blank at col 6)
    index 1 -> '2'  (first continuation: 2cG, 2cL)
    index 2 -> '3'
    ...
    index 8 -> '9'
    index 9 -> 'A'
    """
    if index == 0:
        return ' '
    n = index + 1    # 1-based: primary=1, first continuation=2, ...
    if n <= 9:
        return str(n)
    return chr(ord('A') + n - 10)


# ─── Group processing ──────────────────────────────────────────────────────────

def process_group(group_lines):
    """Process a comment group (primary + zero or more continuations).

    Returns (new_lines, was_changed):
      new_lines   -- list of 80-char strings; length may differ from input if
                     extra continuations must be added or removed.
      was_changed -- True if any content was modified.
    """
    if not group_lines:
        return [], False

    first = group_lines[0]
    nucid = first[:5]      # NUCID (cols 1-5)
    record_ch = first[7]   # 'L' or 'G'

    # Build joined logical content:
    #   Primary line  (index 0): keep leading space at col 9, strip only trailing
    #   Continuation  (index 1+): strip both ends (pure padding around content)
    parts = []
    for k, line in enumerate(group_lines):
        raw = line[8:]   # everything from col 9 onward
        part = raw.rstrip() if k == 0 else raw.strip()
        if part:
            parts.append(part)

    joined = ' '.join(parts)

    # Apply {I} conversion to the full logical content
    converted = convert_content(joined)
    if converted == joined:
        # No change needed; return original lines padded to 80
        return [ln.ljust(80) for ln in group_lines], False

    # Re-wrap converted content into chunks fitting ENSDF 80-char lines
    chunks = wrap_into_chunks(converted)

    # Build new physical lines
    new_lines = []
    for idx, chunk in enumerate(chunks):
        marker = continuation_marker(idx)
        prefix = nucid + marker + 'c' + record_ch   # exactly 8 chars
        if idx == 0:
            # Primary: chunk already starts with leading space at col 9 (e.g. ' $A2=')
            content_part = chunk
        else:
            # Continuation: add leading space at col 9 as the inter-line separator.
            # This preserves the space that was consumed at the split point when
            # the ENSDF reader re-joins continuation lines by simple concatenation.
            content_part = ' ' + chunk
        physical = (prefix + content_part).ljust(80)
        if len(physical.rstrip()) > 80:
            print(f'WARNING: chunk {idx} still exceeds 80 chars: {repr(physical.rstrip())}',
                  file=sys.stderr)
        new_lines.append(physical)

    return new_lines, True


# ─── File processing ───────────────────────────────────────────────────────────

def _split_ending(raw_line):
    """Return (content_without_ending, ending_str) for a raw line."""
    if raw_line.endswith('\r\n'):
        return raw_line[:-2], '\r\n'
    if raw_line.endswith('\n'):
        return raw_line[:-1], '\n'
    return raw_line, ''


def process_file(filename, write=False, count_only=False):
    """Process an ENSDF file, converting plain uncertainties to {In} format."""
    with open(filename, 'r', encoding='ascii', newline='') as f:
        raw = f.read()

    parsed = [_split_ending(rl) for rl in raw.splitlines(keepends=True)]

    changed_groups = 0
    result = []   # list of (content_80_chars, ending)
    i = 0

    while i < len(parsed):
        line, ending = parsed[i]

        if is_primary_comment(line):
            # Collect this primary line + all immediately following continuations
            group_contents = [line]
            group_endings = [ending]
            j = i + 1
            while j < len(parsed) and is_continuation_comment(parsed[j][0]):
                group_contents.append(parsed[j][0])
                group_endings.append(parsed[j][1])
                j += 1

            new_group, was_changed = process_group(group_contents)

            if was_changed:
                changed_groups += 1
                if not count_only:
                    orig_range = f'{i + 1}' if j == i + 1 else f'{i + 1}-{j}'
                    print(f'\n=== Group at original line(s) {orig_range} ===')
                    for k, orig in enumerate(group_contents):
                        print(f'  BEFORE L{i + 1 + k}: {repr(orig.rstrip())}')
                    for k, neo in enumerate(new_group):
                        label = 'AFTER ' if k < len(group_contents) else 'NEW   '
                        lineno = i + 1 + k
                        print(f'  {label} L{lineno}: {repr(neo.rstrip())}')

            # Store new_group lines, using original endings where available
            for k, new_line in enumerate(new_group):
                use_ending = group_endings[k] if k < len(group_endings) else group_endings[-1]
                result.append((new_line, use_ending))

            i = j  # advance past the entire original group

        else:
            # Non-comment line: pass through unchanged
            result.append((line, ending))
            i += 1

    # Summary
    print(f'\n--- {"WRITE" if write else "DRY RUN"} ---')
    print(f'Groups changed: {changed_groups}')

    if write:
        with open(filename, 'w', encoding='ascii', newline='') as f:
            for content, end in result:
                f.write(content + end)
        print(f'Written: {filename}')

    return changed_groups


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python convert_uncertainties.py file.ens [--write] [--count]')
        sys.exit(1)

    fname = sys.argv[1]
    write_mode = '--write' in sys.argv
    count_mode = '--count' in sys.argv

    n = process_file(fname, write=write_mode, count_only=count_mode)
    sys.exit(0)
