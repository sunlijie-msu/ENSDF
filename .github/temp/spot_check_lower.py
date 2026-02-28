f = open(r'd:\X\ND\ENSDF\XUNDL\2026BUAA_input_lower_TIE.ens')
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
t = [
    ('6388','4','3.200904'),('6936','2','0.171755'),('7037','2','0.07336'),
    ('7157.5','11','1.29'),('7703','3','0.108122'),('7797','12','0.000412'),
    ('7887','3','0.029192'),('7905','8','0.001861'),('8017','3','0.069893'),
    ('8024','2','0.002536'),('8275','4','0.004309'),('8418','3','0.073363'),
    ('8557','2','0.012235'),('8669','8','0.001232'),('8708','7','0.001966'),
    ('8813','2','0.014232'),('8950','5','0.001564'),('8964','2','0.006938'),
    ('9238','3','0.011928'),('9328','5','0.009797'),('9405','4','0.002336'),
    ('9421','8','0.001909'),('9730','10','0.000012'),
]
print('Levels found:', len(lv))
print('Bidirectional: first=%s dEx=%s TIE=%s  exp=(6388,4,3.200904)  %s' % (
    lv[0][0], lv[0][1], lv[0][2], 'PASS' if lv[0]==t[0] else 'FAIL'))
print('Bidirectional: last=%s dEx=%s TIE=%s  exp=(9730,10,0.000012)  %s' % (
    lv[-1][0], lv[-1][1], lv[-1][2], 'PASS' if lv[-1]==t[-1] else 'FAIL'))
for idx in [0, 10, 16, 20, 22]:
    ok = lv[idx]==t[idx]; st = 'PASS' if ok else 'FAIL'
    print('Spot #%2d: got=%-40s exp=%-40s %s' % (idx+1, str(lv[idx]), str(t[idx]), st))
fails = [i+1 for i in range(23) if lv[i] != t[i]]
if fails:
    for idx in fails:
        print('FAIL row%d: got=%s  exp=%s' % (idx, lv[idx-1], t[idx-1]))
else:
    print('ALL 23/23 PASS - full match with source table')
