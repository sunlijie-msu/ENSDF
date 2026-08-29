path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

P = {'c': ' 34S  c  ', '2c': ' 34S 2c  ', '3c': ' 34S 3c  ', '4c': ' 34S 4c  ',
     '5c': ' 34S 5c  ', '6c': ' 34S 6c  ', '7c': ' 34S 7c  ', '8c': ' 34S 8c  '}

# ---- ground-states block (lines 5-7) ----
gs = [
    ('c', 'The ground states of {+30}Si, |a, and {+34}S are all 0+; therefore, the'),
    ('2c', 'resonances in {+34}S populated in {+30}Si+|a have natural parity, and'),
    ('3c', 'the |g transitions to the {+34}S g.s. are most likely electric.'),
]
# ---- 1967Wi01 block (lines 8-15) ----
w1 = [
    ('c', '1967Wi01: {+30}Si(|a,|g) and (|a,n) with 3.25-4.95 MeV |a beams from'),
    ('2c', 'the 5.5 MeV Van de Graaff accelerator of the Southern Universities'),
    ('3c', 'Nuclear Institute, South Africa. Targets were 15-40 |mg/cm{+2},'),
    ('4c', '45%-95% enriched {+30}Si targets on tantalum backings. |g rays were'),
    ('5c', 'detected using NaI(Tl) detectors. Neutrons were detected using a'),
    ('6c', 'Harwell-form neutron detector. Measured E|g, I|g, |g(|q), |g|g(|q),'),
    ('7c', 'E{-n}, I{-n}, and yields. Deduced resonance levels, J, |p,'),
    ('8c', 'multipolarities, mixing ratios, and resonance strengths.'),
]

def pad(content):
    return content + ' ' * (80 - len(content))

print('=== ground-states (5-7) ===')
for k, txt in gs:
    line = pad(P[k] + txt)
    print(len(line), repr(line))
print('=== 1967Wi01 (8-15) ===')
for k, txt in w1:
    line = pad(P[k] + txt)
    print(len(line), repr(line))

# current lines to replace
print()
print('=== current lines 5-15 ===')
for i in range(4, 15):
    print(i + 1, 'len', len(ls[i]), repr(ls[i]))

# build old/new blocks and verify match
old_gs = '\n'.join(ls[4:7])
new_gs = '\n'.join(pad(P[k] + txt) for k, txt in gs)
old_w1 = '\n'.join(ls[7:15])
new_w1 = '\n'.join(pad(P[k] + txt) for k, txt in w1)
print()
print('old_gs in t:', old_gs in t)
print('old_w1 in t:', old_w1 in t)
print('all new 80:', all(len(pad(P[k] + txt)) == 80 for k, txt in gs) and all(len(pad(P[k] + txt)) == 80 for k, txt in w1))
