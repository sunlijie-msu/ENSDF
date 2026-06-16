"""Extract BE2(DOWN) values from ruler.rpt for MIN/MAX and MONTE-CARLO methods.
Target: 17 gammas in the band structure table."""
import re

RPT = r"d:\X\ND\Files\ruler.rpt"

# Define the 17 gammas we care about: (gamma_energy, level_energy)
TARGETS = [
    ("486.7", "4067.0"),
    ("792.4", "4859.4"),
    ("1044.0", "5903.4"),
    ("1239.5", "7142.9"),
    ("1468.0", "8610.9"),
    ("1205.2", "8348.1"),
    ("457.2", "5459.3"),
    ("748.2", "6207.5"),
    ("841.4", "7048.9"),
    ("938.3", "7987.2"),
    ("1040.2", "9027.4"),
    ("1164.1", "10191.5"),
    ("679.9", "7774.1"),
    ("783.7", "8557.8"),
    ("918.8", "9476.6"),
    ("1108.5", "10585.1"),
    ("1328.4", "11913.5"),
]

def parse_ruler(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into level blocks
    blocks = re.split(r'-{3,}', content)
    
    results = {}
    
    for block in blocks:
        # Find level energy
        lev_match = re.search(r'141SM\s+L\s+([\d.]+)', block)
        if not lev_match:
            continue
        lev_e = lev_match.group(1)
        
        # Find gamma energy sections within this block
        gamma_sections = re.split(r'#{10,}', block)
        
        for gs in gamma_sections:
            # Find gamma energy
            eg_match = re.search(r'--->gamma[^:]*:\s*EG=([\d.]+)', gs)
            if not eg_match:
                # Also try: <EG=...> format
                eg_match = re.search(r'<EG=([\d.]+)>', gs)
            if not eg_match:
                continue
            eg = eg_match.group(1)
            
            # Check if this gamma is in our targets
            key = (eg, lev_e)
            if key not in TARGETS:
                # Try partial match on eg only
                matching_targets = [t for t in TARGETS if t[0] == eg]
                if not matching_targets:
                    continue
            
            # Extract MIN/MAX (<2>) BE2(DOWN)
            minmax_section = re.search(r'\*\s*<2>\s*Use uncertainties.*?(?=\*\s*<[23]>)', gs, re.DOTALL)
            if minmax_section:
                mm_text = minmax_section.group(0)
                # Look for BE2(DOWN)=...
                be2d_match = re.search(r'BE2\(DOWN\)=([\d.>]+)\s*([+\-][\d]+-[+\-]?[\d]+)?', mm_text)
                if be2d_match:
                    minmax_val = be2d_match.group(1)
                    minmax_unc = be2d_match.group(2) or ''
                    if minmax_val.startswith('>'):
                        minmax_str = f">{minmax_val[1:]}"
                    else:
                        minmax_str = f"{minmax_val} {minmax_unc}" if minmax_unc else minmax_val
                else:
                    # Try BE2(DOWN)> format
                    be2d_match = re.search(r'BE2\(DOWN\)>([\d.]+)', mm_text)
                    if be2d_match:
                        minmax_str = f">{be2d_match.group(1)}"
                    else:
                        minmax_str = "NOT FOUND"
            else:
                minmax_str = "NOT FOUND"
            
            # Extract MC (<3>) BE2(DOWN)
            mc_section = re.search(r'\*\s*<3>\s*Use uncertainties.*?(?=#{10,}|\*\*\s+suggested|\Z)', gs, re.DOTALL)
            if mc_section:
                mc_text = mc_section.group(0)
                # Check if MC is not suitable
                if 'Monte-Carlo approach is not suitable' in mc_text or 'not suitable' in mc_text:
                    mc_str = "MC not suitable"
                else:
                    be2d_match = re.search(r'BE2\(DOWN\)=([\d.]+)\s*([+\-][\d]+-[+\-]?[\d]+)?', mc_text)
                    if be2d_match:
                        mc_val = be2d_match.group(1)
                        mc_unc = be2d_match.group(2) or ''
                        mc_str = f"{mc_val} {mc_unc}" if mc_unc else mc_val
                    else:
                        mc_str = "NOT FOUND"
            else:
                # Look in the suggested approach section
                sug = re.search(r'####\s*suggested approach.*?BE2DOWN=([\d.]+)\s+([+\-][\d]+-[+\-]?[\d]+)?', gs, re.DOTALL)
                if sug:
                    mc_str = f"{sug.group(1)} {sug.group(2) if sug.group(2) else ''}"
                else:
                    mc_str = "NOT FOUND"
            
            results[(eg, lev_e)] = {
                'minmax': minmax_str.strip(),
                'mc': mc_str.strip()
            }
            print(f"EG={eg:>8s}  LEV={lev_e:>8s}  MIN/MAX: {minmax_str.strip():30s}  MC: {mc_str.strip()}")
    
    return results

results = parse_ruler(RPT)

# Show missing
print(f"\nFound {len(results)} of {len(TARGETS)} targets")
found_keys = set(results.keys())
for t in TARGETS:
    if t not in found_keys:
        print(f"MISSING: EG={t[0]}, LEV={t[1]}")
