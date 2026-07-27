"""Reformat S34 resonance cL comments to ENSDF standard {I} notation."""
import re

with open(r'A34\S34\new\S34_n_g_n_n_resonances.ens', 'r', encoding='utf-8', newline='') as f:
    raw = f.read()
    le = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.split(le)

def reformat_cl(line):
    """Reformat a single cL comment line."""
    # Extract prefix (cols 1-9) and text (col 10+)
    if len(line) < 10:
        return line
    prefix = line[:9]  # " 34S  cL " or " 34S 2cL "
    text = line[9:].strip()
    
    if not text:
        return line
    
    # Check if this is a cL line we need to reformat
    # Type A: gGnGg/G only, already has {I} notation
    # Type B: Detailed params with $ separator and space-uncertainty
    # Type C: |G|g=1.5 EV $ (fictitious level special)
    # Type D: Other (E$, T$, S$ label comments - skip these)
    
    # Skip non-parameter comments
    if any(text.startswith(s) for s in ['E$', 'T$', 'S$', 'J|p', 'g=statistical']):
        return line
    
    # Handle Type C: |G|g=1.5 EV $
    if text.startswith('|G|g='):
        # "|G|g=1.5 EV $"
        m = re.match(r'\|G\|g\s*=\s*([\d.]+)\s*(EV|KEV|MEV)\s*\$', text)
        if m:
            val, unit = m.group(1), m.group(2).lower()
            text = f"$|G|g={val} {unit}."
            return (prefix + text).ljust(80)
    
    # Handle Type A: gGnGg/G only
    if text.startswith('$g|G{-n}|G{-|g}/|G='):
        # Already has {I} notation, just ensure proper ending
        # "$g|G{-n}|G{-|g}/|G=0.086 {I6}"
        # Check if already ends with period
        if not text.endswith('.'):
            text = text + '.'
        return (prefix + text).ljust(80)
    
    # Handle Type B: Detailed params
    if text.startswith('$|G{-n}=') or text.startswith('$|G{-|a}=') or text.startswith('$g|G'):
        # Parse all parameters: split by "$"
        # Format: $|G{-n}=75.0 EV 8 $ |G|g=0.21 EV 5 $ |G{-|a}=41 EV 5
        # Remove leading $
        if text.startswith('$'):
            text = text[1:]
        
        # Split by " $ " or " $" to get individual params
        # Actually, the params are separated by "$ "
        params_raw = re.split(r'\s*\$\s*', text)
        params_raw = [p.strip() for p in params_raw if p.strip()]
        
        new_params = []
        for p in params_raw:
            # Parse: |G{-n}=75.0 EV 8  or  |G|g=0.21 EV 5  or  |G{-|a}=41 EV 5
            # Pattern: name=value UNIT uncertainty
            m = re.match(r'(\|G(?:\{-.+?\}|\|g|\{\|g\}))\s*=\s*([\d.]+)\s*(EV|KEV|MEV)\s*(\d+)', p)
            if m:
                name, val, unit, unc = m.group(1), m.group(2), m.group(3).lower(), m.group(4)
                new_params.append(f"{name}={val} {unit} {'{I' + unc + '}'}")
            else:
                # Maybe single value without unit? (shouldn't happen in this file)
                new_params.append(p)
        
        # Rejoin with ". " separator
        text = "$" + ". ".join(new_params) + "."
        return (prefix + text).ljust(80)
    
    # If we can't parse, return unchanged
    return line

# Process all lines
new_lines = []
for line in lines:
    # Check if this is a cL comment
    if len(line) >= 9 and line[6] == 'c' and line[7] == 'L':
        new_lines.append(reformat_cl(line))
    else:
        new_lines.append(line)

new_content = le.join(new_lines)

# Write
with open(r'.github\temp\2026-07-26_s34_resonance\reformatted.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(new_content)

# Show changes
print("Reformatted cL lines:")
for i, (old, new) in enumerate(zip(lines, new_lines)):
    if old != new:
        print(f"  Line {i+1}:")
        print(f"    OLD: [{old.rstrip()}]")
        print(f"    NEW: [{new.rstrip()}]")
        print()
