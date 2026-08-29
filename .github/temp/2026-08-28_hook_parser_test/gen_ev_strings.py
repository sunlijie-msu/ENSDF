# READ-ONLY: print exact OLD/NEW (with L-record context) for the 12 eV additions.
import re
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(path, encoding='utf-8', newline='').read().replace('\r\n','\n').replace('\r','\n').split('\n')

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '
targets = ['9932','9981','10097','10169','10249','10317','10408','10494','10587','10625','10670','10768']
for i, ln in enumerate(lines):
    if is_L(ln) and ln[9:19].strip() in targets:
        e = ln[9:19].strip()
        j = i + 1
        # include L-record line as context, then lines up to strength cL
        block = [ln]
        j = i + 1
        while j < len(lines):
            block.append(lines[j])
            if lines[j].startswith(' 34S  cL ') and '|G{-|g}|G{-|a}/|G=' in lines[j] and '(1964Va08)' in lines[j]:
                break
            j += 1
        old = block
        new = list(block)
        # eV insert + repad on last line
        last = new[-1]
        last2 = last.replace(' (1964Va08)', ' eV (1964Va08)', 1).rstrip().ljust(80)
        new[-1] = last2
        print(f'=== L{e} ===')
        for o in old:
            print(f'OLD|{o}|')
        print('---')
        for n in new:
            print(f'NEW|{n}|')
        print()
