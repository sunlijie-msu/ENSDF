"""Report exact current state of all flag-target L-records (byte-exact, with repr)."""
P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

FIX = ['10140', '10201', '10236', '10447', '10528', '10617', '10869']
NEW = ['10895', '10917', '10931', '10994', '11088', '11108', '11142', '11165',
       '11180', '11194', '11220', '11233', '11272', '11289', '11315', '11323',
       '11358', '11372', '11381', '11398', '11405', '11420', '11979', '12271']
EE = ['10430', '10800', '11350', '11500']

for tag, group in (("FIX", FIX), ("NEW", NEW), ("E", EE)):
    for e in group:
        hit = [ln for ln in lines if ln[5:8] == '  L' and ln[9:19].strip() == e]
        if len(hit) != 1:
            print(f"{tag:4s} {e:7s} MATCHES={len(hit)}")
            continue
        ln = hit[0]
        flag = None
        for col in (76, 77, 78):
            ch = ln[col - 1] if len(ln) >= col else ' '
            if ch.isalpha():
                flag = (col, ch)
        print(f"{tag:4s} {e:7s} len={len(ln):3d} flag={flag} content_end={len(ln.rstrip()):3d}")
        print(f"     repr: {repr(ln)}")
