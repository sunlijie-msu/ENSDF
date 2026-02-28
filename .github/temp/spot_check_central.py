f = open(r'd:\X\ND\ENSDF\XUNDL\2026BUAA_input_central_TIE.ens')
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
    ('6388','4','3.380904'),('6936','2','0.2021'),('7037','2','0.086941'),
    ('7157.5','11','1.31'),('7703','3','0.141675'),('7797','12','0.000545'),
    ('7887','3','0.037739'),('7905','8','0.002677'),('8017','3','0.090033'),
    ('8024','2','0.003774'),('8275','4','0.007007'),('8418','3','0.094608'),
    ('8557','2','0.015392'),('8669','8','0.001863'),('8708','7','0.002841'),
    ('8813','2','0.020322'),('8950','5','0.009796'),('8964','2','0.008936'),
    ('9238','3','0.015596'),('9328','5','0.017335'),('9405','4','0.003258'),
    ('9421','8','0.003847'),('9730','10','0.000513'),
]
print('Levels found:', len(lv))
fails = [i+1 for i in range(23) if lv[i] != t[i]]
if fails:
    for idx in fails:
        print('FAIL row%d: got=%s  exp=%s' % (idx, lv[idx-1], t[idx-1]))
else:
    print('ALL 23/23 PASS - full match with source table')
