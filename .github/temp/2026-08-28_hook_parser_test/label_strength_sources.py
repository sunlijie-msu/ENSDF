# Add source-literature labels to (2J+1)|G{g}|G{a}/|G resonance-strength cL comments.
# Subscript convention (per user):
#   |G{-|g}            -> 1964Va08 (Table 1, Strength column)
#   |G{-|g0} (Mc07)    -> 1965Mc07 (Table 2)
#   |G{-|g1} or g0     -> 1967Wi01 (Table 4, Main decay mode)
# Z-levels (1975DeZS, eV values) left untouched.
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'

# level_energy -> (value fragment, source label)
ADD = {
    # ---- 1964Va08 (|g, no subscript) ----
    '9981':  ('=0.2',     '(1964Va08)'),
    '10097': ('=(0.2)',   '(1964Va08)'),
    '10169': ('=0.7',     '(1964Va08)'),
    '10249': ('=0.9',     '(1964Va08)'),
    '10317': ('=0.4',     '(1964Va08)'),
    '10408': ('=0.2',     '(1964Va08)'),
    '10494': ('=2',       '(1964Va08)'),
    '10587': ('=4',       '(1964Va08)'),
    '10625': ('=2',       '(1964Va08)'),
    '10670': ('=2',       '(1964Va08)'),
    '10768': ('=0.7',     '(1964Va08)'),
    '10791': ('=9',       '(1964Va08)'),
    # ---- 1965Mc07 (|g0) ----
    '11025': ('=3.9 eV',  '(1965Mc07)'),
    '11088': ('=0.5 eV',  '(1965Mc07)'),
    '11142': ('=6.2 eV',  '(1965Mc07)'),
    '11165': ('=2.1 eV',  '(1965Mc07)'),
    '11220': ('=0.2 eV',  '(1965Mc07)'),
    '11233': ('=1.2 eV',  '(1965Mc07)'),
    '11315': ('=0.2 eV',  '(1965Mc07)'),
    '11323': ('=3.1 eV',  '(1965Mc07)'),
    # ---- 1967Wi01 (|g1) ----
    '11458': ('=2.4 eV',  '(1967Wi01)'),
    '11473': ('=1.2 eV',  '(1967Wi01)'),
    '11506': ('=0.74 eV', '(1967Wi01)'),
    '11712': ('=0.63 eV', '(1967Wi01)'),
    '11922': ('=2.1 eV',  '(1967Wi01)'),
    '11957': ('=1.9 eV',  '(1967Wi01)'),
    # ---- 1967Wi01 (|g0) ----
    '11932': ('=5.2 eV',  '(1967Wi01)'),
    '12034': ('=2.1 eV',  '(1967Wi01)'),
    '12100': ('=1.5 eV',  '(1967Wi01)'),
    '12194': ('=3.5 eV',  '(1967Wi01)'),
}

with open(path, 'r', encoding='utf-8', newline='') as f:
    lines = f.read().split('\r\n')

def is_L(ln):
    return len(ln) >= 9 and ln[5:9] == '  L '

def is_strength(ln):
    return '$(2J+1)|G{-|g' in ln or ('2cL (2J+1)|G{-|g' in ln and len(ln) >= 9 and ln[6:9] == 'cL ')

changed = []
i = 0
while i < len(lines):
    ln = lines[i]
    if is_L(ln):
        e = ln[9:19].strip()
        if e in ADD:
            frag, src = ADD[e]
            j = i + 1
            done = False
            while j < len(lines) and len(lines[j]) >= 9 and lines[j][6:9] == 'cL ':
                t = lines[j][9:]
                if '$(2J+1)|G{-|g' in t and frag in t and '(' not in t[t.index(frag)+len(frag):]:
                    # strip trailing spaces, append source, repad to 80
                    base = lines[j].rstrip()
                    new = (base + ' ' + src).ljust(80)
                    assert len(new) <= 80, new
                    lines[j] = new
                    changed.append((j + 1, e, frag, src))
                    done = True
                    break
                j += 1
            if not done:
                print(f'WARN: no match for E={e} frag={frag}')
            i = j
            continue
    i += 1

# line 43 special: '=0.14 (1964Va08).' -> remove trailing period
for idx, ln in enumerate(lines):
    if '=0.14 (1964Va08).' in ln:
        lines[idx] = ln.replace('=0.14 (1964Va08).', '=0.14 (1964Va08)')
        changed.append((idx + 1, '9932', '=0.14', 'period removed'))

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(lines))

print(f'Changed {len(changed)} lines:')
for lineno, e, frag, src in changed:
    print(f'   line {lineno}: E={e} {frag} -> {src}')
