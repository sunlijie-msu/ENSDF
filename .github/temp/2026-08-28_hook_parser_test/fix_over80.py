# Re-pad any line exceeding 80 chars to exactly 80 (content unchanged).
# Target: Va08 strength lines where ' eV ' insertion left 83-char lines.
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read()
# detect current EOL style
if '\r\n' in t:
    eol = '\r\n'
else:
    eol = '\n'
lines = t.replace('\r\n', '\n').replace('\r', '\n').split('\n')

fixed = []
for i, ln in enumerate(lines):
    if len(ln) > 80:
        stripped = ln.rstrip()
        if len(stripped) > 80:
            print(f'WARN line {i+1}: content >80 even stripped ({len(stripped)}): {stripped!r}')
            fixed.append((i + 1, len(ln), len(stripped), 'TRUNCATED'))
            lines[i] = stripped[:80]
        else:
            lines[i] = stripped.ljust(80)
            fixed.append((i + 1, len(ln), 80, 'repadded'))

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(eol.join(lines))

print(f'Fixed {len(fixed)} lines:')
for n, before, after, kind in fixed:
    print(f'   line {n}: {before} -> {after} ({kind})')
