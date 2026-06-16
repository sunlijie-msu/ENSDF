"""Final extraction of BE2(DOWN) MIN/MAX and MC values for 17 target gammas."""
import re

with open(r'd:\X\ND\Files\ruler.rpt', 'r') as f:
    content = f.read()

# Target gammas: (Eg, band)
TARGETS = {
    "486.7": "QB1",
    "792.4": "QB1", 
    "1044.0": "QB1",
    "1239.5": "QB1",
    "1468.0": "QB1",
    "1205.2": "QB1",
    "457.2": "QB2",
    "748.2": "QB2",
    "841.4": "QB2",
    "938.3": "QB2",
    "1040.2": "QB2",
    "1164.1": "QB2",
    "679.9": "QB3",
    "783.7": "QB3",
    "918.8": "QB3",
    "1108.5": "QB3",
    "1328.4": "QB3",
}

sections = re.split(r'--->gamma', content)

results = {}

for sec in sections:
    eg_m = re.search(r'EG=([\d.]+)', sec)
    if not eg_m:
        continue
    eg = eg_m.group(1)
    if eg not in TARGETS:
        continue
    
    # Extract MIN/MAX (<2>) BE2(DOWN)
    # Find the <2> block within this section
    mm_block = re.search(r'<\s*2\s*>.*?(?=<\s*3\s*>|#{10,}|\*\*\s+suggested)', sec, re.DOTALL)
    mm_val = None
    mm_unc = None
    mm_limit = False
    
    if mm_block:
        mm_text = mm_block.group(0)
        # Try "BE2(DOWN)=VALUE +UPPER-LOWER" pattern
        m = re.search(r'BE2\(DOWN\)=([\d.]+)\s+([+-][\d]+-[+-]?[\d]+)', mm_text)
        if m:
            mm_val = m.group(1)
            mm_unc = m.group(2).replace('+-', '+')
        else:
            # Try "BE2(DOWN)>VALUE" pattern
            m = re.search(r'BE2\(DOWN\)>([\d.]+)', mm_text)
            if m:
                mm_val = m.group(1)
                mm_limit = True
    
    # Extract MC (<3>) BE2(DOWN)
    mc_val = None
    mc_unc = None
    mc_limit = False
    mc_not_suitable = False
    
    if 'Monte-Carlo approach is not suitable' in sec or 'not suitable' in sec.lower():
        mc_not_suitable = True
    else:
        mc_block = re.search(r'<\s*3\s*>.*?(?=#{10,}|\*\*\s+suggested)', sec, re.DOTALL)
        if mc_block:
            mc_text = mc_block.group(0)
            m = re.search(r'BE2\(DOWN\)=([\d.]+)\s+([+-][\d]+-[+-]?[\d]+)', mc_text)
            if m:
                mc_val = m.group(1)
                mc_unc = m.group(2).replace('+-', '+')
            else:
                # Try symmetrized format: "VALUE UNC" after BE2(DOWN)=
                m = re.search(r'BE2\(DOWN\)=([\d.]+)\s+(\d+)', mc_text)
                if m:
                    mc_val = m.group(1)
                    # symmetric uncertainty
                    mc_unc = '+' + m.group(2) + '-' + m.group(2)
        
        # If still no MC value, try suggested approach
        if mc_val is None:
            sug = re.search(r'suggested.*?BE2DOWN=([\d.]+)\s+([+-][\d]+-[+-]?[\d]+)?', sec, re.DOTALL)
            if sug:
                mc_val = sug.group(1)
                if sug.group(2):
                    mc_unc = sug.group(2).replace('+-', '+')
    
    band = TARGETS[eg]
    
    # Format MIN/MAX
    if mm_limit:
        mm_str = f">{mm_val}"
    elif mm_val:
        mm_str = f"{mm_val} {mm_unc}"
    else:
        mm_str = "N/A"
    
    # Format MC
    if mc_not_suitable:
        mc_str = "MC not suitable"
    elif mc_val:
        mc_str = f"{mc_val} {mc_unc}" if mc_unc else mc_val
    else:
        mc_str = "N/A"
    
    results[eg] = {
        'band': band,
        'minmax': mm_str,
        'mc': mc_str,
    }
    print(f"{eg:>8s} | {band:3s} | MIN/MAX: {mm_str:35s} | MC: {mc_str}")

print(f"\nFound {len(results)} of {len(TARGETS)} targets")
for eg in sorted(TARGETS.keys()):
    if eg not in results:
        print(f"MISSING: {eg}")
