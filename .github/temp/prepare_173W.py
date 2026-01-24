import textwrap

original_comments = """214-225-MeV, 70-ns pulsed, {+50}Ti beams were produced from the 88-inch
cyclotron and bombarded a 1-mg/cm2 {+128}Te target backed by 50-mg/cm2
{+nat}Pb. Experiment at Argonne National Laboratory: 220-MeV pulsed
{+50}Ti beam was produced from the ATLAS accelerator and bombarded
235-370-|mg/cm2 {+126}Te self-supporting foils sandwiched between
500-|mg/cm2 and 50-|mg/cm2 Au. States in 173W were populated via the
128TE(50TI,5N) channel, and the deexciting |g rays were detected using
the Gammasphere array, which consists of 91 and 100 Compton-suppressed
high-purity germanium detectors in the two experiments, respectively.
Measured E|g, I|g, |g|g-coin, |g|g(|q). Deduced levels, J, |p, |g-ray
multipolarities, bands, lifetimes using the delayed and anti-delayed
coincidence techniques. Comparisons with the
configuration-interaction-shell-model calculations."""

# Clean up newlines for wrapping
text = original_comments.replace('\n', ' ')
# Fix units
text = text.replace('214-225-MeV', '214-225 MeV')
text = text.replace('1-mg/cm2', '1 mg/cm{+2}')
text = text.replace('50-mg/cm2', '50 mg/cm{+2}')
text = text.replace('220-MeV', '220 MeV')
text = text.replace('235-370-|mg/cm2', '235-370 |mg/cm{+2}')
text = text.replace('500-|mg/cm2', '500 |mg/cm{+2}')
text = text.replace('50-|mg/cm2', '50 |mg/cm{+2}')
# Remove extra spaces
text = ' '.join(text.split())

# Wrap
wrapper = textwrap.TextWrapper(width=71) # 80 - 9 for "173W nc  "
lines = wrapper.wrap(text)

print("NEW COMMENTS:")
for i, line in enumerate(lines):
    val = i + 2
    if val < 10:
        c_char = str(val)
    else:
        c_char = chr(ord('A') + val - 10)
    
    out_line = f"173W {c_char}c  {line}"
    print(f"{out_line:<80}")

# Data
raw_data = """165.2(3) 2042.9 8 → 7 21/2+ → 19/2+ 100(11)
186.3(5) 2229.2 7 → 8 23/2+ → 21/2+ 79(10)
205.5(3) 2434.7 8 → 7 25/2+ → 23/2+ 70(9)
220.6(2) 2655.3 7 → 8 27/2+ → 25/2+ 84(9)
243.0(2) 2898.3 8 → 7 29/2+ → 27/2+ 88(9)
351.4(4) 2229.2 7 → 7 23/2+ → 19/2+ 18(6)
391.4(3) 2434.7 8 → 8 25/2+ → 21/2+ 73(10)
425.9(2) 2655.3 7 → 7 27/2+ → 23/2+ 84(12)
463.5(4) 2898.3 8 → 8 29/2+ → 25/2+ 95(11)
503.9(5) 3159.2 7 → 7 31/2+ → 27/2+ 63(12)
186.0(5) 2346.0 10 → 9 25/2− → 23/2− 88(6)
210.4(3) 2556.4 9 → 10 27/2− → 25/2− 100(6)
233.6(4) 2790.0 10 → 9 29/2− → 27/2− 98(7)
254.8(3) 3044.8 9 → 10 31/2− → 29/2− 74(4)
274.1(5) 3318.9 10 → 9 33/2− → 31/2− 55(3)
290.6(6) 3609.5 9 → 10 35/2− → 33/2− 53(3)
306.2(7) 3915.7 10 → 9 37/2− → 35/2− 35(2)
320.4(5) 4236.1 9 → 10 39/2− → 37/2− 44(2)
334.7(6) 4570.8 10 → 9 41/2− → 39/2− 28(2)
348.9(4) 4919.7 9 → 10 43/2− → 41/2− 32(2)
362.8(5) 5282.4 10 → 9 45/2− → 43/2− 21(3)
377.4(2) 5659.8 9 → 10 47/2− → 45/2− 16(3)
392.2(3) 6051.8 10 → 9 49/2− → 47/2− 6(1)
396.6(5) 2556.4 9 → 9 27/2− → 23/2− unmeasured
406.2(4) 6457.7 9 → 10 51/2− → 49/2− 5(1)
444.2(5) 2790.0 10 → 10 29/2− → 25/2− unmeasured
488.7(3) 3044.8 9 → 9 31/2− → 27/2− - unmeasured
528.7(5) 3318.9 10 → 10 33/2− → 29/2− 41(3)
564.4(4) 3609.5 9 → 9 35/2− → 31/2− 49(4)
596.7(5) 3915.7 10 → 10 37/2− → 33/2− 76(5)
626.4(5) 4236.1 9 → 9 39/2− → 35/2− 51(5)
655.0(4) 4570.8 10 → 10 41/2− → 37/2− 48(4)
683.4(6) 4919.7 9 → 9 43/2− → 39/2− 52(4)
711.4(4) 5282.4 10 → 10 45/2− → 41/2− 46(4)
740.1(4) 5659.8 9 → 9 47/2− → 43/2− 43(4)
769.4(4) 6051.8 10 → 10 49/2− → 45/2− 33(7)
797.9(4) 6457.7 9 → 9 51/2− → 47/2− 29(6)"""

# Processing Logic
def parse_uncertainty(val_str):
    if '(' not in val_str:
        return val_str, ""
    val, unc = val_str.split('(')
    unc = unc.replace(')', '')
    return val, unc

def format_record(Ei, Jpi_i, gammas):
    l_line = "173W  L {:<10}  {:<17}".format(Ei, Jpi_i)
    # Pad L line to 80
    print(f"{l_line:<80}")
    
    for g in gammas:
        eg_val, eg_unc = parse_uncertainty(g['Eg'])
        
        # Handle unmeasured Ig
        if 'unmeasured' in g['Ig']:
             ig_val, ig_unc = "", ""
        else:
             ig_val, ig_unc = parse_uncertainty(g['Ig'])

        # G Record Format
        eg_field = "{:<10}".format(eg_val)
        de_field = "{:<2}".format(eg_unc)
        
        if ig_val:
            ri_field = "{:<7}".format(ig_val)
            dri_field = "{:<2}".format(ig_unc)
        else:
            ri_field = "       "
            dri_field = "  "

        g_line = f"173W  G {eg_field}{de_field} {ri_field}{dri_field}"
        print(f"{g_line:<80}")
        
        band_i = g['Bandi']
        band_f = g['Bandf']
        comment = f"Band {band_i} -> Band {band_f}"
        if 'unmeasured' in g['Ig']:
             comment += ", I|g unmeasured"

        cg_line = f"173W  cG {comment}"
        print(f"{cg_line:<80}")

lines = raw_data.split('\n')
parsed_data = {} 

for l in lines:
    if not l.strip(): continue
    parts = l.split()
    Eg_raw = parts[0]
    Ei = parts[1]
    Bandi = parts[2]
    Bandf = parts[4]
    Jpi_i = parts[5]
    Jpi_f = parts[7]
    Ig_rest = parts[8:]
    Ig_raw = " ".join(Ig_rest)
    if Ig_raw == "- unmeasured": Ig_raw = "unmeasured"
    
    Jpi_i = Jpi_i.replace('−', '-')
    Jpi_f = Jpi_f.replace('−', '-')
    
    entry = {
       'Eg': Eg_raw,
       'Ei': Ei,
       'Bandi': Bandi,
       'Bandf': Bandf,
       'Jpi_i': Jpi_i,
       'Jpi_f': Jpi_f,
       'Ig': Ig_raw
    }
    
    if Ei not in parsed_data:
        parsed_data[Ei] = {'Jpi': Jpi_i, 'gammas': []}
    parsed_data[Ei]['gammas'].append(entry)

sorted_levels = sorted(parsed_data.keys(), key=lambda x: float(x))

print("NEW DATA:")
for Ei in sorted_levels:
    lvl = parsed_data[Ei]
    gammas = sorted(lvl['gammas'], key=lambda x: float(parse_uncertainty(x['Eg'])[0]))
    format_record(Ei, lvl['Jpi'], gammas)