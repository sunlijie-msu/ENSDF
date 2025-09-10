from __future__ import annotations
import sys
from pathlib import Path

def fix_file(path: Path) -> int:
    txt = path.read_text(encoding='utf-8', errors='replace').splitlines(True)
    changed = 0
    out = []
    for line in txt:
        # Preserve original line and newline by default
        original_line = line
        ln = line.rstrip('\n')
        work = ln
        changed_line = False
        # Pad a working copy to at least 80 for safe slicing
        if len(work) < 80:
            work = work + ' ' * (80 - len(work))
        # Identify true G-record data lines (not cG, B G, etc.)
        if work.startswith(' 35S') and len(work) >= 31 and work[7] == 'G' and work[8] == ' ':
            # Ensure the energy field has digits to avoid touching continuation/info lines
            energy = work[9:19]
            if any(c.isdigit() for c in energy):
                # Column 22 (index 21) must be a readability space
                if work[21] != ' ':
                    # Shift the 22-29 block right by one within itself:
                    # new[21] = ' ', new[22:29] = old[21:28]
                    # Leave DRI (29-30) and rest untouched.
                    work = work[:21] + ' ' + work[21:28] + work[29:]
                    changed += 1
                    changed_line = True
        # Write back: only rewrite changed G lines; otherwise keep byte-for-byte
        if changed_line:
            # Ensure exact 80-column width and add newline
            out.append((work if len(work) >= 80 else work.ljust(80)) + '\n')
        else:
            out.append(original_line)
    Path(path).write_text(''.join(out), encoding='utf-8')
    return changed

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: fix_ri_alignment.py <path-to-ens>')
        sys.exit(2)
    p = Path(sys.argv[1])
    cnt = fix_file(p)
    print(f'Adjusted RI alignment on {cnt} G-record line(s).')
