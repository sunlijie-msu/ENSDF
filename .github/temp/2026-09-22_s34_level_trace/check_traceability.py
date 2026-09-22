import re, json, os

base = r"d:\X\ND\ENSDF\A34\S34\new"

letter_to_file = {
    'A': 'S34_34p_beta_decay_12.43_s.ens',
    'B': 'S34_34cl_ec_decay_1.5266_s.ens',
    'C': 'S34_34cl_ec_decay_31.99_m.ens',
    'D': 'S34_3h_32s_pg.ens',
    'E': 'S34_3h_35cl_ag.ens',
    'F': 'S34_4he_30si_a_resonances.ens',
    'G': 'S34_12c_24mg_34sg.ens',
    'H': 'S34_24mg_16o_a2pg.ens',
    'I': 'S34_27al_10b_2png.ens',
    'J': 'S34_27al_12c_apg.ens',
    'K': 'S34_28si_34s_34sPg.ens',
    'L': 'S34_30si_a_g_a_n_resonances.ens',
    'M': 'S34_31p_a_pg.ens',
    'N': 'S34_32s_t_p.ens',
    'O': 'S34_32s_a_2he.ens',
    'P': 'S34_ng_E_thermal.ens',
    'Q': 'S34_33s_n_g_n_n_resonances.ens',
    'R': 'S34_33s_d_p.ens',
    'S': 'S34_34s_g_gP_pol_g_gP.ens',
    'T': 'S34_34s_e_eP.ens',
    'U': 'S34_34s_pi+_pi+P_pi-_pi-P.ens',
    'V': 'S34_34s_n_n_n_nP.ens',
    'W': 'S34_34s_p_pP_pol_p_pP.ens',
    'X': 'S34_34s_p_pPg.ens',
    'Y': 'S34_34s_pol_d_d_pol_d_dP.ens',
    'Z': 'S34_34s_a_a_a_aP_a_aPg.ens',
    'a': 'S34_35cl_g_p.ens',
    'b': 'S34_35cl_n_d.ens',
    'c': 'S34_35cl_d_3he.ens',
    'd': 'S34_37cl_p_ag.ens',
    'e': 'S34_206pb_34s_34sPg.ens',
    'f': 'S34_208pb_34s_34sP.ens',
    'g': 'S34_208pb_36s_34sg.ens',
}

def parse_levels(fpath):
    """Return list of (E_float, E_str, DE_str, lineno) for plain L records."""
    levels = []
    if not os.path.exists(fpath):
        return levels
    with open(fpath, encoding="utf-8", errors="replace") as f:
        for i, l in enumerate(f):
            l = l.rstrip("\n")
            if len(l) < 8:
                continue
            if l[5] == ' ' and l[6] == ' ' and l[7] == 'L':
                e_field = l[9:19].strip()
                de_field = l[19:21].strip()
                if not e_field:
                    continue
                # strip trailing non-numeric junk like SN, SP labels etc
                m = re.match(r'^-?\d+\.?\d*', e_field)
                if not m:
                    continue
                try:
                    ef = float(m.group(0))
                except ValueError:
                    continue
                levels.append((ef, e_field, de_field, i+1))
    return levels

dataset_levels = {}
for letter, fn in letter_to_file.items():
    dataset_levels[letter] = parse_levels(os.path.join(base, fn))

print("Dataset level counts:")
for letter, fn in letter_to_file.items():
    print(f"  {letter}: {fn}: {len(dataset_levels[letter])} levels")

with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\dataset_levels.json", "w") as f:
    json.dump(dataset_levels, f, indent=1)
