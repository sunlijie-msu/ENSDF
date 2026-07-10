from pathlib import Path

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

# Classify gammas
b_gammas = []
nonb_gammas = []
ce = None
for i, l in enumerate(tgt_lines):
    if len(l)<10: continue
    if l[:5].strip()!='34P': continue
    if l[5]==' ' and l[6]==' ' and l[7]=='L':
        ce = l[9:19].strip()
    elif l[5]==' ' and l[6]==' ' and l[7]=='G' and ce:
        eg = l[9:19].strip()
        de = l[19:21].strip()
        ri = l[22:29].strip()
        dri = l[29:31].strip()
        if l[76] == 'B':
            b_gammas.append((i, ce, eg, de, ri, dri))
        else:
            nonb_gammas.append((i, ce, eg, de, ri, dri))

# === REMOVE ALL EXISTING cG RI$ LINES ===
new_lines = []
removed = 0
for l in tgt_lines:
    if 'cG RI' in l[6:11]:
        removed += 1
        continue
    new_lines.append(l)
print('Removed %d old cG RI$ lines' % removed)

# === CROSS-CHECK NON-B vs 2018LU08 ===
needs_ri = []
eg_mismatches = []
for idx, ex, eg, tde, tri, tdri in nonb_gammas:
    key_match = None
    try: tex_f = float(ex); teg_f = float(eg)
    except: continue
    for (sex, seg), (s_eg, s_de, s_ri, s_dri) in data_2018.items():
        try: sex_f = float(sex); seg_f = float(seg)
        except: continue
        if abs(sex_f - tex_f) <= 1.5 and abs(seg_f - teg_f) <= 0.5:
            key_match = (s_eg, s_de, s_ri, s_dri)
            break
    
    if key_match:
        s_eg, s_de, s_ri, s_dri = key_match
        # Cross-check Egamma
        eg_ok = (s_eg == eg and s_de == tde)
        if not eg_ok:
            eg_mismatches.append((idx+1, eg, s_eg, s_de, eg, tde))
        # RI always differs (scaled), add comment
        if s_ri:
            needs_ri.append((idx, eg, s_ri, s_dri))
    else:
        eg_mismatches.append((idx+1, eg, '?', '?', eg, tde))

# === CROSS-CHECK B-FLAGGED vs 2012BE11 ===
for idx, ex, eg, tde, tri, tdri in b_gammas:
    key_match = None
    try: tex_f = float(ex); teg_f = float(eg)
    except: continue
    for (sex, seg), (s_eg, s_de, s_ri, s_dri) in data_2012.items():
        try: sex_f = float(sex); seg_f = float(seg)
        except: continue
        if abs(sex_f - tex_f) <= 1.5 and abs(seg_f - teg_f) <= 0.5:
            key_match = (s_eg, s_de, s_ri, s_dri)
            break
    
    if key_match:
        s_eg, s_de, s_ri, s_dri = key_match
        eg_ok = (s_eg == eg and s_de == tde)
        ri_ok = (s_ri == tri and s_dri == tdri)
        if not eg_ok:
            eg_mismatches.append((idx+1, eg, s_eg, s_de, eg, tde))
        if not ri_ok:
            pass  # RI differs because target uses scaled values - expected
    else:
        eg_mismatches.append((idx+1, eg, '?', '?', eg, tde))

# === REPORT ===
print('\n=== Egamma MISMATCHES ===')
for ln, eg, s_eg, s_de, t_eg, t_de in eg_mismatches:
    print('  L%d: G %s  src=%s(%s)  tgt=%s(%s)' % (ln, eg, s_eg, s_de, t_eg, t_de))
print('Total Egamma mismatches: %d' % len(eg_mismatches))

print('\n=== ADDING cG RI$ COMMENTS (from 2018Lu08 to non-B gammas) ===')
insertions = []
for idx, eg, sri, sdri in needs_ri:
    if sdri:
        comment = 'RI$%s {I%s} (2018Lu08).' % (sri, sdri)
    else:
        comment = 'RI$%s (2018Lu08).' % sri
    cg_line = (' 34P  cG ' + comment).ljust(80)
    insertions.append((idx, cg_line))
    print('  L%d: G %s -> %s' % (idx+1, eg, cg_line[9:].strip()))

# Insert bottom-up
insertions.sort(key=lambda x: x[0], reverse=True)
for g_idx, cg_line in insertions:
    insert_at = g_idx + 1
    while insert_at < len(new_lines) and new_lines[insert_at][:5].strip()=='34P' and new_lines[insert_at][6:8]=='cG':
        insert_at += 1
    new_lines.insert(insert_at, cg_line)

tgt.write_text('\n'.join(new_lines) + '\n')
print('\nDone: removed %d old, added %d new cG RI$ comments.' % (removed, len(insertions)))
