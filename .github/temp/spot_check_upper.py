f = open(r'd:\X\ND\ENSDF\XUNDL\2026BUAA_input_upper_TIE.ens')
lines = f.readlines()
f.close()
lv = []
i = 0
while i < len(lines):
    l = lines[i].rstrip('\n')
    if len(l) >= 8 and l[7] == 'L' and l[6] == ' ':
        for j in range(i+1, min(i+10, len(lines))):
            e = lines[j].rstrip('\n')
            if len(e) >= 8 and e[7] == 'E' and e[6] == ' ':
                lv.append((l[9:19].strip(), l[19:21].strip(), e[64:74].strip()))
                break
    i += 1
# Note: 8418 TIE source = 0.117392671 (11 chars) stored as 0.11739267 (10 chars, truncated to fit field)
t = [
    ('6388','4','3.560904'),('6936','2','0.233936'),('7037','2','0.101163'),
    ('7157.5','11','1.33'),('7703','3','0.175852'),('7797','12','0.000683'),
    ('7887','3','0.047624'),('7905','8','0.003521'),('8017','3','0.112109'),
    ('8024','2','0.005055'),('8275','4','0.009782'),('8418','3','0.11739267'),
    ('8557','2','0.018693'),('8669','8','0.002535'),('8708','7','0.003808'),
    ('8813','2','0.02681'),('8950','5','0.018176'),('8964','2','0.011235'),
    ('9238','3','0.019375'),('9328','5','0.024736'),('9405','4','0.004326'),
    ('9421','8','0.005801'),('9730','10','0.001016'),
]
print('Levels found:', len(lv))
print('Bidirectional: first=%s dEx=%s TIE=%s  exp=(6388,4,3.560904)  %s' % (
    lv[0][0], lv[0][1], lv[0][2], 'PASS' if lv[0]==t[0] else 'FAIL'))
print('Bidirectional: last=%s dEx=%s TIE=%s  exp=(9730,10,0.001016)  %s' % (
    lv[-1][0], lv[-1][1], lv[-1][2], 'PASS' if lv[-1]==t[-1] else 'FAIL'))
for idx in [0, 11, 15, 20, 22]:
    ok = lv[idx]==t[idx]; st = 'PASS' if ok else 'FAIL'
    print('Spot #%2d: got=%-40s exp=%-40s %s' % (idx+1, str(lv[idx]), str(t[idx]), st))
fails = [i+1 for i in range(23) if lv[i] != t[i]]
if fails:
    for idx in fails:
        print('FAIL row%d: got=%s  exp=%s' % (idx, lv[idx-1], t[idx-1]))
else:
    print('ALL 23/23 PASS - full match with stored values')
