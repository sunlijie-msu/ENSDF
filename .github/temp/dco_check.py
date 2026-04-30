#!/usr/bin/env python3
"""DCO consistency check for no-POL G-records in Cl34_27al_12c_ang.ens"""
from pathlib import Path
import re

p = Path(r'A34/Cl34/new/Cl34_27al_12c_ang.ens')
lines = p.read_text().splitlines()

levels_list = []
current_level = None

records = []

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith(' 34CL  L '):
        level_energy = line[9:19].strip()
        level_jpi = line[21:39].strip()
        try:
            ef = float(level_energy.split()[0])
        except:
            ef = 0.0
        current_level = (ef, level_energy, level_jpi)
        levels_list.append(current_level)
    elif line.startswith(' 34CL  G '):
        eg_str = line[9:19].strip()
        m_field = line[32:41].strip()
        mr_field = line[41:49].strip()

        # Collect comment block
        comments = []
        j = i + 1
        while j < len(lines):
            nl = lines[j]
            if nl.startswith(' 34CL  G ') or nl.startswith(' 34CL  L ') or nl.startswith(' 34CL d') or nl.startswith(' 34CL PN'):
                break
            comments.append(nl)
            j += 1
        comment_text = ' '.join(comments)

        # Extract POL
        pol_m = re.search(r'POL=([+-]?\d*\.?\d+)', comment_text)
        pol = float(pol_m.group(1)) if pol_m else None

        # Extract DCO
        dco_q_m = re.search(r'R\{-DCO\}\(Q\)=([\d.]+)', comment_text)
        dco_d_m = re.search(r'R\{-DCO\}\(D\)=([\d.]+)', comment_text)
        dco_q = float(dco_q_m.group(1)) if dco_q_m else None
        dco_d = float(dco_d_m.group(1)) if dco_d_m else None

        if m_field and pol is None:
            try:
                eg_v = float(eg_str.split()[0])
                ei = current_level[0]
                ef_energy = ei - eg_v
                best = None
                best_dist = 999
                for lv in levels_list:
                    d = abs(lv[0] - ef_energy)
                    if d < best_dist:
                        best_dist = d
                        best = lv
                final_level = best if best_dist < 15 else None
            except:
                final_level = None
                eg_v = 0

            records.append({
                'level_e': current_level[1],
                'level_jpi': current_level[2],
                'eg': eg_str,
                'eg_v': eg_v if 'eg_v' in dir() else 0,
                'M': m_field,
                'MR': mr_field,
                'DCO_Q': dco_q,
                'DCO_D': dco_d,
                'final_level': final_level,
                'line': i+1
            })
    i += 1

print(f'G records with M field but no POL: {len(records)}\n')

def parse_j(s):
    s = s.strip().strip('()+- ')
    for part in s.split(','):
        part = part.strip()
        if '/' in part:
            nums = part.split('/')
            try:
                return float(nums[0]) / float(nums[1])
            except:
                pass
        else:
            try:
                return float(part)
            except:
                pass
    return None


def dco_expected(M, dj):
    """Return expected DCO(Q) and DCO(D) ranges based on multipolarity and dJ"""
    # Leading component determines D or Q
    m = M.strip('[]()').split('+')[0].strip()
    if m in ('E1', 'M1', 'D'):
        char = 'D'
    elif m in ('E2', 'M2', 'Q'):
        char = 'Q'
    elif m == 'E3':
        char = 'oct'
    else:
        char = '?'
    return char


print(f"{'#':<3} {'Level':<10} {'Ji':<5} {'Eg':<7} {'Ef':<8} {'Jf':<5} {'dJ':<3} {'M':<12} {'MR':<8} {'DCO(Q)':<8} {'DCO(D)':<8} {'Expected':<10} {'CONSISTENT?'}")
print('-' * 120)

for idx, r in enumerate(records, 1):
    fi = r['final_level']
    jf_str = fi[2] if fi else '?'
    ef_str = f"{fi[0]:.1f}" if fi else '?'

    ji = parse_j(r['level_jpi'])
    jf = parse_j(jf_str)
    dj = abs(ji - jf) if (ji is not None and jf is not None) else None
    dj_str = str(int(dj)) if (dj is not None and dj == int(dj)) else (f'{dj:.1f}' if dj is not None else '?')

    M = r['M']
    dco_q = r['DCO_Q']
    dco_d = r['DCO_D']
    mr = r['MR']

    # Determine leading multipolarity character
    m_bare = M.strip('[]()').split('+')[0].strip()
    if m_bare in ('E1', 'M1', 'D'):
        lead = 'D'
    elif m_bare in ('E2', 'M2', 'Q'):
        lead = 'Q'
    elif m_bare == 'E3':
        lead = 'oct'
    else:
        lead = '?'

    # Check DCO consistency
    consistent = '?'
    notes = ''
    if dco_q is not None:
        if lead == 'D' and dj == 1:
            # Stretched dipole: DCO(Q) ~ 0.5
            if 0.3 <= dco_q <= 0.7:
                consistent = 'OK'
            else:
                consistent = 'FLAG'
                notes = f'DCO(Q)={dco_q} expected~0.5 for D dJ=1'
        elif lead == 'Q' and dj == 2:
            # Stretched quadrupole: DCO(Q) ~ 1.0
            if 0.7 <= dco_q <= 1.3:
                consistent = 'OK'
            else:
                consistent = 'FLAG'
                notes = f'DCO(Q)={dco_q} expected~1.0 for Q dJ=2'
        elif lead == 'Q' and dj == 0:
            # Unstretched dipole or quadrupole: DCO(Q) ~ 1.0
            if 0.7 <= dco_q <= 1.3:
                consistent = 'OK'
            else:
                consistent = 'FLAG'
                notes = f'DCO(Q)={dco_q} expected~1.0 for Q dJ=0'
        elif lead == 'D' and dj == 2:
            # Pure dipole but dJ=2: expect DCO(Q)~0.5? Actually D+Q for dJ=2 from D perspective
            consistent = 'REVIEW'
            notes = f'D leading but dJ=2'
        elif 'D+Q' in M or '+' in M:
            # Mixed: DCO between 0.5 and 1.0 for DCO(Q)
            if 0.3 <= dco_q <= 1.3:
                consistent = 'OK(mixed)'
            else:
                consistent = 'FLAG'
                notes = f'DCO(Q)={dco_q} unusual for mixed'
        else:
            consistent = 'REVIEW'
            notes = f'dJ={dj_str} lead={lead}'
    elif dco_d is not None:
        if lead == 'D' and dj == 1:
            # Stretched dipole: DCO(D) ~ 1.0
            if 0.7 <= dco_d <= 1.4:
                consistent = 'OK'
            else:
                consistent = 'FLAG'
                notes = f'DCO(D)={dco_d} expected~1.0 for D dJ=1'
        elif lead == 'Q' and dj == 2:
            # Stretched quadrupole: DCO(D) ~ 2.0
            if 1.5 <= dco_d <= 2.5:
                consistent = 'OK'
            else:
                consistent = 'FLAG'
                notes = f'DCO(D)={dco_d} expected~2.0 for Q dJ=2'
        elif 'D+Q' in M or '+' in M:
            # Mixed: DCO(D) between 1.0 and 2.0
            if 0.7 <= dco_d <= 2.2:
                consistent = 'OK(mixed)'
            else:
                consistent = 'FLAG'
                notes = f'DCO(D)={dco_d} unusual for mixed'
        else:
            consistent = 'REVIEW'
            notes = f'dJ={dj_str} lead={lead}'
    else:
        consistent = 'NO DCO'

    dco_q_s = f'{dco_q}' if dco_q else '-'
    dco_d_s = f'{dco_d}' if dco_d else '-'

    print(f"{idx:<3} {r['level_e']:<10} {r['level_jpi']:<5} {r['eg']:<7} {ef_str:<8} {jf_str:<5} {dj_str:<3} {M:<12} {mr:<8} {dco_q_s:<8} {dco_d_s:<8} {lead:<10} {consistent}  {notes}")
