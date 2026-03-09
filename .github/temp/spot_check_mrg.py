ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'

# For a given G energy, search the mrg for its GAMMA block and show what datasets have data
def check_gamma_in_mrg(mrg_lines, e_str, tolerance=2.0):
    try:
        adp_e = float(e_str)
    except:
        return
    current_e = None
    current_block = []
    for ml in mrg_lines:
        l = ml.rstrip('\n')
        if l.startswith(' GAMMA-'):
            current_block = [l]
            idx = l.find(' 34CL  G')
            if idx >= 0:
                try:
                    current_e = float(l[idx+9:idx+19].strip())
                except:
                    current_e = None
            else:
                current_e = None
        elif l.startswith(' LEVEL') or l.startswith('-----'):
            if current_e is not None and abs(current_e - adp_e) < tolerance:
                print(f"  GAMMA block for E={adp_e} (mrg_E={current_e}):")
                for bl in current_block[:10]:
                    if bl.strip():
                        print(f"    {repr(bl[:100])}")
                return
            current_block = []
            current_e = None
        else:
            current_block.append(l)
    print(f"  No mrg entry found for E={e_str} (within {tolerance} keV)")

mrg_lines = open(MRG_FILE, encoding='utf-8').readlines()

# Check a sample of energies that have no Other
sample_energies = ['4300.2', '1884.4', '2447.7', '1888.3', '5025.2', '3414.9']
for e in sample_energies:
    print(f"\nSearching mrg for G {e}:")
    check_gamma_in_mrg(mrg_lines, e)
