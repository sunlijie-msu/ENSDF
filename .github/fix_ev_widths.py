from __future__ import annotations
from pathlib import Path
import sys

# ENSDF columns are 1-based; Python indices are 0-based
# L-record fields of interest:
#   T  field: cols 40-49  -> indices 39:49
#   DT field: cols 50-55  -> indices 49:55
# We will only blank these when the T field contains 'EV' (e.g., '0.025 EV  1').
# All other content must remain exactly unchanged; only rewrite changed lines.

def process(path: Path) -> int:
    lines = path.read_text(encoding='utf-8', errors='replace').splitlines(True)
    out: list[str] = []
    changed = 0
    for line in lines:
        original = line
        body = line.rstrip('\n')
        work = body
        # Only consider true L-records: NUCID in cols 1-5, 'L' at col 8, blanks at 7 & 9 typically
        if len(work) >= 9 and work.startswith(' 35S') and work[7] == 'L' and work[8] == ' ':
            # Ensure we can slice safely
            if len(work) < 80:
                work = work + ' ' * (80 - len(work))
            t_field = work[39:49]
            dt_field = work[49:55]
            # If T field contains 'EV', we blank both T and DT (cols 40-55) with spaces
            if 'EV' in t_field:
                work = work[:39] + (' ' * 16) + work[55:]
                # Keep 80 columns
                work = work[:80]
                out.append(work + '\n')
                changed += 1
                continue
        # Default: keep original line exactly
        out.append(original)
    path.write_text(''.join(out), encoding='utf-8')
    return changed

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: fix_ev_widths.py <path-to-ens>')
        sys.exit(2)
    p = Path(sys.argv[1])
    c = process(p)
    print(f'Removed EV widths on {c} L-record line(s).')
