from pathlib import Path
import re

# === PARSE SOURCES ===
src_2012 = Path(r'd:\X\ND\ENSDF\A34\P34\raw\2012BE11.ens')
src_2018 = Path(r'd:\X\ND\ENSDF\A34\P34\raw\2018LU08.ens')

def parse_ens(path):
    data = {}
    ce = None
    for l in path.read_text().splitlines():
        if len(l)<10: continue
        if l[:5].strip()!='34P': continue
        if l[5]==' ' and l[6]==' ' and l[7]=='L':
            ce = l[9:19].strip()
        elif l[5]==' ' and l[6]==' ' and l[7]=='G' and ce:
            eg = l[9:19].strip()
            de = l[19:21].strip()
            ri = l[22:29].strip()
            dri = l[29:31].strip()
            data[(ce, eg)] = (eg, de, ri, dri)
    return data

data_2012 = parse_ens(src_2012)
data_2018 = parse_ens(src_2018)

# === PARSE TARGET ===
tgt = Path(r'd:\X\ND\ENSDF\A34\P34\new\P34_18o_18o_png_E_24_mev.ens')
tgt_lines = tgt.read_text().splitlines()

# Classify by B flag
b_gammas = []  # (line_idx, ex, eg, tgt_ri, tgt_dri)
nonb_gammas = []
ce = None
for i, l in enumerate(tgt_lines):
    if len(l)<10: continue
    if l[:5].strip()!='34P': continue
    if l[5]==' ' and l[6]==' ' and l[7]=='L':
        ce = l[9:19].strip()
    elif l[5]==' ' and l[6]==' ' and l[7]=='G' and ce:
        eg = l[9:19].strip()
        ri = l[22:29].strip()
        dri = l[29:31].strip()
        if l[76] == 'B':
            b_gammas.append((i, ce, eg, ri, dri))
        else:
            nonb_gammas.append((i, ce, eg, ri, dri))

print('B-flagged gammas (2012Be11): %d' % len(b_gammas))
print('Non-B gammas (2018Lu08): %d' % len(nonb_gammas))

# === MATCH AND CROSS-CHECK ===
def match_level(tex, seg, src_data, tol_ex=1.5, tol_eg=0.5):
    try: tex_f = float(tex); teg_f = float(seg)
    except: return None
    for (sex, seg_key), (seg_val, sde, sri, sdri) in src_data.items():
        try: sex_f = float(sex); seg_f = float(seg_key)
        except: continue
        if abs(sex_f - tex_f) <= tol_ex and abs(seg_f - teg_f) <= tol_eg:
            return (seg_val, sde, sri, sdri)
    return None

print('\n=== CROSS-CHECK B-FLAGGED (vs 2012BE11) ===')
eg_mismatch = 0
ri_mismatch = 0
for idx, ex, eg, tri, tdri in b_gammas:
    m = match_level(ex, eg, data_2012)
    if m:
        s_eg, s_de, s_ri, s_dri = m
        eg_ok = (s_eg == eg and s_de == tdri)  # compare DE
        ri_ok = (s_ri == tri and s_dri == tdri)
        status = 'OK' if (eg_ok and ri_ok) else ('EG_MIS' if not eg_ok else 'RI_MIS')
        if not eg_ok: eg_mismatch += 1
        if not ri_ok: ri_mismatch += 1
        if status != 'OK':
            print('  L%d: G %s  src EG=%s(%s) tgt=%s(%s)  src RI=%s(%s) tgt=%s(%s)  %s' % (
                idx+1, eg, s_eg, s_de, eg, tdri, s_ri, s_dri, tri, tdri, status))
    else:
        print('  L%d: G %s  NO MATCH in 2012BE11!' % (idx+1, eg))
        eg_mismatch += 1

print('\n=== CROSS-CHECK NON-B (vs 2018LU08) ===')
needs_ri_comment = []
for idx, ex, eg, tri, tdri in nonb_gammas:
    m = match_level(ex, eg, data_2018)
    if m:
        s_eg, s_de, s_ri, s_dri = m
        eg_ok = (s_eg == eg and s_de == tdri)
        if not eg_ok:
            print('  L%d: G %s  src EG=%s(%s) tgt=%s(%s)  EG_MISMATCH' % (idx+1, eg, s_eg, s_de, eg, tdri))
            eg_mismatch += 1
        if s_ri != tri or s_dri != tdri:
            needs_ri_comment.append((idx, eg, s_ri, s_dri))
            ri_mismatch += 1
    else:
        print('  L%d: G %s  NO MATCH in 2018LU08!' % (idx+1, eg))
        eg_mismatch += 1

print('\n=== SUMMARY ===')
print('Egamma mismatches: %d' % eg_mismatch)
print('RI differences needing cG RI$: %d' % len(needs_ri_comment))

# === REMOVE OLD cG RI$ LINES ===
new_lines = []
removed = 0
for l in tgt_lines:
    if 'cG RI$' in l[6:11]:
        removed += 1
        continue
    new_lines.append(l)
print('\nRemoved %d old cG RI$ lines' % removed)

# === ADD CORRECT cG RI$ for 2018LU08 gammas ===
insertions = []
for idx, eg, sri, sdri in needs_ri_comment:
    if sri:
        if sdri:
            comment = 'RI$%s {%s} (2018Lu08).' % (sri, 'I'+sdri)
        else:
            comment = 'RI$%s (2018Lu08).' % sri
        cg_line = (' 34P  cG ' + comment).ljust(80)
        insertions.append((idx, cg_line, eg, sri, sdri))

insertions.sort(key=lambda x: x[0], reverse=True)
for g_idx, cg_line, eg, sri, sdri in insertions:
    insert_at = g_idx + 1
    while insert_at < len(new_lines) and new_lines[insert_at][:5].strip()=='34P' and new_lines[insert_at][6:8]=='cG':
        insert_at += 1
    new_lines.insert(insert_at, cg_line)

tgt.write_text('\n'.join(new_lines) + '\n')
print('Added %d cG RI$ comments (from 2018Lu08 only)' % len(insertions))
print('Done.')
