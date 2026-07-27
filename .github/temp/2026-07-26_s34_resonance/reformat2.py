"""Reformat S34 resonance cL comments to ENSDF standard {I} notation. V2."""
import re

with open(r'A34\S34\new\S34_n_g_n_n_resonances.ens', 'r', encoding='utf-8', newline='') as f:
    raw = f.read()
    le = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.split(le)

UNIT_MAP = {'EV': 'eV', 'KEV': 'keV', 'MEV': 'MeV'}

def reformat_cl(line):
    if len(line) < 10: return line
    prefix = line[:9]
    text = line[9:].strip()
    if not text: return line
    
    # Skip label/header comments
    if any(text.startswith(s) for s in ['E$', 'T$', 'S$', 'J|p', 'g=statistical',
                                          'LABEL=', 'From E{-c']):
        return line
    
    # Type C: $|G|g=1.5 EV $ (fictitious level, no uncertainty)
    if text.startswith('$|G|g='):
        m = re.match(r'\$\|G\|g\s*=\s*([\d.]+)\s*(EV|KEV|MEV)\s*\$', text)
        if m:
            val, unit_raw = m.group(1), m.group(2)
            unit = UNIT_MAP.get(unit_raw, unit_raw.lower())
            text = f"$|G|g={val} {unit}."
            return (prefix + text).ljust(80)
    
    # Type A: gGnGg/G only (already {I} notation)
    if text.startswith('$g|G{-n}|G{-|g}/|G='):
        if not text.endswith('.'):
            text = text + '.'
        return (prefix + text).ljust(80)
    
    # Type B: Detailed params with $ separator
    if text.startswith('$|G{-n}=') or text.startswith('$|G{-|a}=') or text.startswith('$g|G'):
        if text.startswith('$'):
            text = text[1:]
        
        # Split by " $ " separator
        params_raw = re.split(r'\s*\$\s*', text)
        params_raw = [p.strip() for p in params_raw if p.strip()]
        
        new_params = []
        for p in params_raw:
            # |G{-n}=75.0 EV 8 or |G|g=0.21 EV 5 or |G{-|a}=41 EV 5
            m = re.match(r'(\|G(?:\{-.+?\}|\|g|\{\|g\}))\s*=\s*([\d.]+)\s*(EV|KEV|MEV)\s*(\d+)', p)
            if m:
                name, val, unit_raw, unc = m.group(1), m.group(2), m.group(3), m.group(4)
                unit = UNIT_MAP.get(unit_raw, unit_raw.lower())
                new_params.append(f"{name}={val} {unit} {{I{unc}}}")
            else:
                new_params.append(p)
        
        text = "$" + ". ".join(new_params) + "."
        return (prefix + text).ljust(80)
    
    return line

new_lines = [reformat_cl(l) for l in lines]
new_content = le.join(new_lines)

with open(r'.github\temp\2026-07-26_s34_resonance\reformatted.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(new_content)

# Show first few changes
count = 0
for i, (old, new) in enumerate(zip(lines, new_lines)):
    if old != new:
        print(f"L{i+1}: OLD=[{old.rstrip()}]")
        print(f"L{i+1}: NEW=[{new.rstrip()}]")
        print()
        count += 1
        if count >= 5: break
print(f"... {sum(1 for o,n in zip(lines,new_lines) if o!=n)} total changed")
