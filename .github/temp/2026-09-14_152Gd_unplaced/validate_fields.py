"""Full-field validation of the inserted unplaced-G block against the parsed Table VI source,
plus bidirectional positional check and a 15% random spot check (source markdown line -> target record)."""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
ENS = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
MD = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md"

rows = json.load(open(os.path.join(HERE, 'table_vi_rows.json')))

# ---- 1. Bidirectional positional check on the SOURCE markdown -------------
mdlines = open(MD, encoding='utf-8').read().split('\n')
data_lines = [l for l in mdlines if l.startswith('|') and '---' not in l][1:]  # drop header row
assert len(data_lines) == len(rows), (len(data_lines), len(rows))
fwd = [l for l in data_lines]
rev = [l for l in reversed(data_lines)]
bad_bidi = 0
for i in range(len(fwd)):
    if fwd[i].strip() != rev[len(rev) - 1 - i].strip():
        bad_bidi += 1
print("BIDIRECTIONAL (source md, forward vs reverse indexing): %d/%d rows identical" % (len(fwd) - bad_bidi, len(fwd)))
print("source md data rows:", len(data_lines), "| md record line numbers:", rows[0]['line'], "-", rows[-1]['line'])

# ---- 2. Pull the inserted block out of the target .ens --------------------
lines = open(ENS, encoding='ascii').read().split('\n')
pn = next(i for i, s in enumerate(lines) if s[6:8] == 'PN')
block = []
i = pn + 1
while i < len(lines):
    t = lines[i][6:8].strip() if len(lines[i]) >= 8 else ''
    if t == 'G':
        block.append((i + 1, lines[i]))
    elif t == 'L':
        break
    i += 1
assert len(block) == len(rows) == 348, (len(block), len(rows))

# ---- 3. Field-by-field comparison ----------------------------------------
errs = []


def check(cond, msg):
    if not cond:
        errs.append(msg)


prev_e = -1.0
for k, (r, (lineno, s)) in enumerate(zip(rows, block)):
    tag = "row %d (source md line %d, target line %d)" % (k + 1, r['line'], lineno)
    check(len(s) == 80, tag + ": length %d != 80" % len(s))
    check(s[:9] == '152GD  G ', tag + ": cols1-9 = %r" % s[:9])
    e_f, de_f = s[9:19], s[19:21]
    check(e_f == r['e'].ljust(10), "%s: E field %r != %r" % (tag, e_f, r['e'].ljust(10)))
    check(de_f == r['de'].ljust(2), "%s: DE field %r != %r" % (tag, de_f, r['de'].ljust(2)))
    check(s[21] == ' ', tag + ": col22 not blank")
    check(s[31] == ' ', tag + ": col32 not blank")
    ri_f, dri_f = s[22:29], s[29:31]
    if r['ri'] is None:
        check(ri_f.strip() == '' and dri_f.strip() == '', "%s: RI %r/DRI %r should be blank" % (tag, ri_f, dri_f))
    else:
        if 'E' in ri_f:
            same = abs(float(ri_f) - float(r['ri'])) <= 1e-12 * float(r['ri'])
            check(same, "%s: E-notation RI %r != source %r" % (tag, ri_f, r['ri']))
        else:
            check(ri_f == r['ri'].ljust(7), "%s: RI field %r != %r" % (tag, ri_f, r['ri'].ljust(7)))
        check(dri_f == r['dri'].ljust(2), "%s: DRI field %r != %r" % (tag, dri_f, r['dri'].ljust(2)))
    check(s[32:76] == ' ' * 44, tag + ": cols33-76 not blank: %r" % s[32:76])
    flag = s[76]
    want_flag = 'X' if r['coinc'] == '*' else ' '
    check(flag == want_flag, "%s: col77 %r != %r (source coincidence %r)" % (tag, flag, want_flag, r['coinc']))
    check(s[77:80] == '   ', tag + ": cols78-80 = %r" % s[77:80])
    e_val = float(r['e'])
    check(e_val > prev_e, tag + ": energy not ascending")
    prev_e = e_val

print("FIELD-BY-FIELD: %d records, %d errors" % (len(block), len(errs)))
for e in errs[:20]:
    print("  ERR", e)

# ---- 4. Random spot check (15%) ------------------------------------------
n = int(round(0.15 * len(rows)))
random.seed(20260914)
picks = sorted(random.sample(range(len(rows)), n))
print("\nRANDOM SPOT CHECK: %d of %d rows (seed 20260914)" % (n, len(rows)))
sp_err = 0
for k in picks:
    r = rows[k]
    lineno, s = block[k]
    src = mdlines[r['line'] - 1]
    cells = [c.strip() for c in src.strip().strip('|').split('|')]
    e_cells = cells[0].split()
    ri_cells = cells[1].split()
    tgt_e, tgt_de = s[9:19].rstrip(), s[19:21].rstrip()
    tgt_ri, tgt_dri = s[22:29].rstrip(), s[29:31].rstrip()
    tgt_flag = 'X' if s[76] == 'X' else '-'
    checks = [
        tgt_e == e_cells[0],
        tgt_de == e_cells[1].strip('()'),
        tgt_flag == ('X' if '*' in cells[2] else '-'),
    ]
    if ri_cells:
        want_ri = ri_cells[0]
        ri_ok = (abs(float(tgt_ri) - float(want_ri)) <= 1e-12 * float(want_ri)) if 'E' in tgt_ri else (tgt_ri == want_ri)
        checks.append(ri_ok)
        checks.append(tgt_dri == ri_cells[1].strip('()'))
    else:
        checks.append(tgt_ri == '' and tgt_dri == '')
    ok = all(checks)
    if not ok:
        sp_err += 1
    print("  md line %3d | %-24s src E=%-8s DE=%-3s RI=%-9s DRI=%-3s flag=%s" % (
        r['line'], src.strip(), e_cells[0], e_cells[1].strip('()'),
        ri_cells[0] if ri_cells else '-', ri_cells[1].strip('()') if ri_cells else '-',
        'X' if '*' in cells[2] else '-'))
    print("  target %4d | E=%-8s DE=%-3s RI=%-9s DRI=%-3s flag=%s | %s" % (
        lineno, tgt_e, tgt_de, tgt_ri or '-', tgt_dri or '-', tgt_flag, "OK" if ok else "*** MISMATCH ***"))
print("SPOT-CHECK: %d rows compared, %d mismatches" % (len(picks), sp_err))
print("\nRESULT: %s" % ("ALL CHECKS PASS" if (not errs and not sp_err) else "FAILURES PRESENT"))
