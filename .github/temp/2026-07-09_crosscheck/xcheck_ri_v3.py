from pathlib import Path

# === PARSE SOURCES ===
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
            ri = l[22:29].strip()
            dri = l[29:31].strip()
            data[(ce, eg)] = (ri, dri)
    return data

data_2018 = parse_ens(src_2018)

# === PARSE TARGET ===
tgt = Path(r'd:\X\ND\ENSDF\A34\P34\new\P34_18o_18o_png_E_24_mev.ens')
tgt_lines = tgt.read_text().splitlines()

# Build: for each non-B gamma, find its G-record line index in ORIGINAL and its source RI
# Store: (original_line_idx, src_ri, src_dri)
to_add = []
ce = None
for i, l in enumerate(tgt_lines):
    if len(l)<10: continue
    if l[:5].strip()!='34P': continue
    if l[5]==' ' and l[6]==' ' and l[7]=='L':
        ce = l[9:19].strip()
    elif l[5]==' ' and l[6]==' ' and l[7]=='G' and ce:
        eg = l[9:19].strip()
        flag = l[76]
        if flag == 'B':
            continue  # skip B-flagged (from 2012Be11)
        # Match to 2018LU08
        try: tex_f = float(ce); teg_f = float(eg)
        except: continue
        for (sex, seg), (sri, sdri) in data_2018.items():
            try: sex_f = float(sex); seg_f = float(seg)
            except: continue
            if abs(sex_f - tex_f) <= 1.5 and abs(seg_f - teg_f) <= 0.5:
                if sri:
                    to_add.append((i, eg, sri, sdri))
                break

print('Non-B gammas to add RI$ comments: %d' % len(to_add))

# === REMOVE ALL EXISTING cG RI$ LINES ===
new_lines = []
removed = 0
for l in tgt_lines:
    if len(l) >= 11 and l[:5].strip()=='34P' and l[6:9]=='cG ' and 'RI$' in l[9:12]:
        removed += 1
        continue
    new_lines.append(l)
print('Removed %d old cG RI$ lines' % removed)

# === RE-LOCATE G-RECORDS IN NEW_LINES AND INSERT ===
# Build map: (ex, eg) -> line_index in new_lines
new_idx_map = {}
ce = None
for i, l in enumerate(new_lines):
    if len(l)<10: continue
    if l[:5].strip()!='34P': continue
    if l[5]==' ' and l[6]==' ' and l[7]=='L':
        ce = l[9:19].strip()
    elif l[5]==' ' and l[6]==' ' and l[7]=='G' and ce:
        eg = l[9:19].strip()
        key = (ce, eg)
        if key not in new_idx_map:
            new_idx_map[key] = i

# Now build insertions with CORRECT indices in new_lines
insertions = []
for old_idx, eg, sri, sdri in to_add:
    # Need to find the corresponding G-record in new_lines
    # We know the old_idx, and we know lines were only deleted above old_idx
    # Count how many lines were removed before old_idx
    removed_before = sum(1 for j in range(old_idx) if 'cG RI' in tgt_lines[j][6:11])
    new_idx = old_idx - removed_before
    
    # Verify: look up by key in new_idx_map
    # Find ce for this gamma... need to re-scan
    ce_for_g = None
    for j in range(old_idx, -1, -1):
        if len(tgt_lines[j])>=10 and tgt_lines[j][:5].strip()=='34P' and tgt_lines[j][5]==' ' and tgt_lines[j][6]==' ' and tgt_lines[j][7]=='L':
            ce_for_g = tgt_lines[j][9:19].strip()
            break
    
    if ce_for_g:
        verify_key = (ce_for_g, eg)
        if verify_key in new_idx_map:
            new_idx = new_idx_map[verify_key]
    
    # Build cG RI$ line
    if sdri:
        comment = 'RI$%s {I%s} (2018Lu08).' % (sri, sdri)
    else:
        comment = 'RI$%s (2018Lu08).' % sri
    cg_line = (' 34P  cG ' + comment).ljust(80)
    
    # Insert AFTER the G-record, before any existing cG comments
    insert_at = new_idx + 1
    while (insert_at < len(new_lines) and 
           new_lines[insert_at][:5].strip()=='34P' and 
           new_lines[insert_at][6:8]=='cG'):
        insert_at += 1
    
    insertions.append((insert_at, cg_line, eg, sri, sdri))

# Insert bottom-up
insertions.sort(key=lambda x: x[0], reverse=True)
for insert_at, cg_line, eg, sri, sdri in insertions:
    new_lines.insert(insert_at, cg_line)
    print('  Inserted after G %s at L%d: %s' % (eg, insert_at+1, cg_line[9:].strip()))

tgt.write_text('\n'.join(new_lines) + '\n')
print('\nDone: removed %d old, added %d cG RI$ after corresponding G-records.' % (removed, len(insertions)))
