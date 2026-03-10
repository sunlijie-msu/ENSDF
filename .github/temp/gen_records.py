
def p(s):
    return s.ljust(80)

records = [
    p(' 34CL  G 1145.4       0.84   20'),
    p(' 34CL cG RI$weighted average of 1.01 {I51} (1977Da02) and 0.81 {I20} (1983Wa27) '),
    p(' 34CL  G 1710.1       2.0    LT'),
    p(' 34CL  G 1914.7       4      LT'),
    p(' 34CL  G 2229.3       100.00 20'),
    p(' 34CL cG RI$other: 100.0 {I5} (1977Da02)'),
    p(' 34CL  G 2375.7       2.0    LT')
]

for r in records:
    print(r)
