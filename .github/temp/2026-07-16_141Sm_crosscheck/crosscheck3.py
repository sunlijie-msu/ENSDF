import re

with open(r'd:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens','r',encoding='utf-8') as f:
    content = f.read()

table = [
('4482.0(6)','33/2','858.1(4)','27.2(12)','','1.68(17)','','Q'),
('4769.1(6)','35/2','287.1(2)','24.6(19)','','0.98(11)','','D+Q'),
('5096.9(6)','37/2','327.8(2)','21.6(14)','','1.12(15)','','D+Q'),
('5366.2(6)','(35/2-)','573.0(4)','2.3(6)','','0.73(7)','','D+Q'),
('5433.9(6)','39/2','337.0(3)','20.8(15)','','0.88(10)','','D+Q'),
('5576.3(6)','37/2','716.9(5)','26.5(15)','0.78(7)','0.90(8)','','D+Q'),
('5641.1(6)','37/2(-)','318.0(3)','26.2(14)','0.88(7)','0.78(7)','','D+Q'),
('6350.3(7)','41/2','447.0(4)','16.3(11)','','0.91(10)','','D+Q'),
('6350.3(7)','41/2','773.9(5)','22.3(15)','','1.41(16)','','Q'),
('6413.4(7)','41/2(-)','473.0(4)','41.2(20)','0.76(7)','0.89(10)','','D+Q'),
('6894.8(7)','43/2(-)','481.4(4)','38.2(12)','0.92(5)','','','D+Q'),
('7376.3(7)','45/2','1026.0(7)','32.3(17)','','1.45(14)','','Q'),
('7384.9(7)','45/2(-)','490.0(4)','23.0(11)','0.79(6)','','','D+Q'),
('8284.3(9)','49/2','908.0(8)','18.3(15)','','1.85(18)','','Q'),
('8610.9(8)','47/2(-)','1468.0(9)*','2.8(2)','0.96(9)','1.63(16)','','Q'),
('12009.0(11)','67/2(+)','772.0(6)*','2.0(1)','1.10(11)','1.53(17)','','Q'),
('13499.5(12)','69/2(+)','1586.0(9)*','4.0(3)','0.94(9)','1.71(16)','','Q'),
('14565.2(12)','71/2(-)','1611.0(10)*','1.5(2)','1.05(10)','1.76(19)','','Q'),
('15377.5(12)','73/2(+)','1878.0(10)*','3.3(3)','0.92(9)','1.52(17)','','Q'),
]

mismatches = 0
for i, row in enumerate(table):
    Ex, Jpi, Eg, RI, RDCO, Rtheta, P, M = row
    eg_val = Eg.split('(')[0].rstrip('*')
    
    idx = content.find('G '+eg_val)
    if idx < 0:
        print(f'ROW {i+1}: Eg={Eg} NOT FOUND')
        mismatches += 1
        continue
    
    ctx = content[idx:idx+200]
    lines = ctx.split('\n')
    g_line = lines[0]
    
    ens_M = g_line[32:41].strip()
    tbl_M = M
    m_ok = (tbl_M == 'Q' and ens_M in ['Q','(E2)','E2']) or (tbl_M == 'D+Q' and ens_M in ['D+Q','(M1+E2)','M1+E2'])
    m_flag = 'OK' if m_ok else 'MISMATCH'
    if not m_ok:
        mismatches += 1
    
    cg_lines = ' '.join(l.strip() for l in lines[1:3] if 'cG' in l)
    
    dco_ok = True
    if RDCO:
        m = re.search(r'([\d.]+)\((\d+)\)', RDCO)
        if m:
            val = m.group(1)
            dco_ok = ('R{-DCO}='+val) in cg_lines
            if not dco_ok:
                mismatches += 1
    
    ado_ok = True
    if Rtheta:
        m = re.search(r'([\d.]+)\((\d+)\)', Rtheta)
        if m:
            val = m.group(1)
            ado_ok = ('R{-ADO}='+val) in cg_lines
            if not ado_ok:
                mismatches += 1
    
    dco_flag = 'OK' if dco_ok else 'MISS'
    ado_flag = 'OK' if ado_ok else 'MISS'
    print(f'Row {i+1}: Eg={Eg} M={tbl_M}->{ens_M} [{m_flag}] DCO={RDCO} [{dco_flag}] ADO={Rtheta} [{ado_flag}]')

print(f'\nTOTAL MISMATCHES: {mismatches}')
