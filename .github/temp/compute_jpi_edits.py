"""Compute exact 80-char replacement lines for all J$ comment edits."""

def make_cL(cont, text, width=80):
    """Build a cL comment line padded to exactly width chars."""
    cont_str = ' ' if cont == 1 else str(cont)
    header = f' 34CL{cont_str}cL '  # 9 chars
    # text must be <= 71 chars to fit within 80
    body = text.strip()
    if len(header) + len(body) > width:
        raise ValueError(f"Text too long ({len(header)+len(body)}): {body!r}")
    return (header + body).ljust(width)

def show(label, old, new):
    ok = 'OK' if len(new) == 80 else f'ERROR({len(new)})'
    print(f"{label} [{ok}]")
    print(f"  OLD: |{old}|")
    print(f"  NEW: |{new}|")
    print()

# ── Change 1: L461.01 – verbose L=0+2 from 0+ in 32S(a,d) ──────────────────
# Old lines 111-113 (all 80 chars each)
old_111 = ' 34CL cL J$L=2 from 0+ in {+36}Ar(d,|a),(pol d,|a) gives 1+,2+,3+; L-1 transfer '
old_112 = ' 34CL2cL from analyzing power. L=0+2 from 0+ in {+32}S(|a,d): L=0 gives 1+; L=2 '
old_113 = ' 34CL3cL gives 1+,2+,3+. Spin=1 from p|g(|q) in {+32}S({+3}He,p|g).             '
# New: L=0+2 intersection = 1+; reflow 3 lines → 3 lines
new_111 = old_111  # unchanged
new_112 = make_cL(2, 'from analyzing power. L=0+2 from 0+ in {+32}S(|a,d) gives 1+. Spin=1  ')
new_113 = make_cL(3, 'from p|g(|q) in {+32}S({+3}He,p|g).                                   ')
show("C1 L461 line111", old_111, new_111)
show("C1 L461 line112", old_112, new_112)
show("C1 L461 line113", old_113, new_113)

# ── Change 2: L665.57 – verbose L=0+2,2+4 from 0+ in 36Ar ──────────────────
# Old lines 142-144
old_142 = ' 34CL cL J$L=0+2,2+4 from 0+ in {+36}Ar(d,|a),(pol d,|a): L=0 gives 1+; L=2     '
old_143 = ' 34CL2cL gives 1+,2+,3+; L=4 gives 3+,4+,5+. Spin=1 from p|g(|q) in             '
old_144 = ' 34CL3cL {+32}S({+3}He,p|g) and |g(|q) in {+33}S(p,|g).                         '
# New: L=0+2 gives 1+; L=2+4 gives 3+; reflow
new_142 = make_cL(1, 'J$L=0+2,2+4 from 0+ in {+36}Ar(d,|a),(pol d,|a): L=0+2 gives 1+; L=2+4 ')
new_143 = make_cL(2, 'gives 3+. Spin=1 from p|g(|q) in {+32}S({+3}He,p|g) and |g(|q) in      ')
new_144 = make_cL(3, '{+33}S(p,|g).                                                           ')
show("C2 L665 line142", old_142, new_142)
show("C2 L665 line143", old_143, new_143)
show("C2 L665 line144", old_144, new_144)

# ── Change 3: L2181.09 – verbose L=2+4 from 0+ in 32S(a,d) ─────────────────
# Old lines 285-288 (J$ block)
old_285 = ' 34CL cL J$L=(2) from 0+ in {+36}Ar(d,|a),(pol d,|a) and L+1 transfer from      '
old_286 = ' 34CL2cL analyzing power gives (3+). L=2+4 from 0+ in {+32}S(|a,d): L=2 gives   '
old_287 = ' 34CL3cL 1+,2+,3+; L=4 gives 3+,4+,5+ for 2175 {I7}. Spin=3 from |g(|q) in      '
old_288 = ' 34CL4cL {+33}S(p,|g).                                                           '
# New: L=2+4 gives 3+; reduce to 3 lines + remove 4cL
new_285 = old_285
new_286 = make_cL(2, 'analyzing power gives (3+). L=2+4 from 0+ in {+32}S(|a,d) gives 3+ for   ')
new_287 = make_cL(3, '2175 {I7}. Spin=3 from |g(|q) in {+33}S(p,|g).                          ')
# old_288 (4cL) to be REMOVED — replace 4-line block with 3-line block
show("C3 L2181 line285", old_285, new_285)
show("C3 L2181 line286", old_286, new_286)
show("C3 L2181 line287", old_287, new_287)
print(f"C3 L2181 line288 REMOVE: |{old_288}|")
print()

# ── Change 4: L2375.67 – verbose L=0+2 in Other: ─────────────────────────────
# Old lines 326-329
old_326 = ' 34CL cL J$spin=4 from p|g(|q) in {+33}S(p,|g) and {+32}S({+3}He,p|g); |p=+ from'
old_327 = ' 34CL2cL 2230|g, M1+E2, to 2+, 1230 level. Other: L=0+2 from 0+ in              '
old_328 = ' 34CL3cL {+36}Ar(d,|a),(pol d,|a): L=0 gives 1+; L=2 gives 1+,2+,3+ for 2382    '
old_329 = ' 34CL4cL {I20}.                                                                  '
# New: L=0+2 gives 1+; reduce 4 lines → 3 lines
new_326 = old_326
new_327 = make_cL(2, '2230|g, M1+E2, to 2+, 1230 level. Other: L=0+2 from 0+ in              ')
new_328 = make_cL(3, '{+36}Ar(d,|a),(pol d,|a) gives 1+ for 2382 {I20}.                       ')
# old_329 (4cL) to be REMOVED
show("C4 L2375 line326", old_326, new_326)
show("C4 L2375 line327", old_327, new_327)
show("C4 L2375 line328", old_328, new_328)
print(f"C4 L2375 line329 REMOVE: |{old_329}|")
print()

# ── Change 5: L2580.30 – verbose L=0+2 from 0+ in 36Ar ─────────────────────
# Old lines 361-363
old_361 = ' 34CL cL J$spin=1 from p|g(|q) in {+33}S(p,|g). L=0 from 3/2+ in                '
old_362 = ' 34CL2cL {+33}S({+3}He,d) gives 1+,2+; L=0+2 from 0+ in {+36}Ar(d,|a),(pol      '
old_363 = ' 34CL3cL d,|a): L=0 gives 1+; L=2 gives 1+,2+,3+.                               '
# New: L=0+2 gives 1+
new_361 = old_361
new_362 = make_cL(2, '{+33}S({+3}He,d) gives 1+,2+; L=0+2 from 0+ in {+36}Ar(d,|a),(pol      ')
new_363 = make_cL(3, 'd,|a) gives 1+.                                                         ')
show("C5 L2580 line361", old_361, new_361)
show("C5 L2580 line362", old_362, new_362)
show("C5 L2580 line363", old_363, new_363)

# ── Change 6: L2721.09 – verbose L=1+3 from 0+ ─────────────────────────────
# Old lines 421-424
old_421 = ' 34CL cL J$spin=2 from |g(|q) in {+31}P(|a,n|g), {+32}S({+3}He,p|g), and        '
old_422 = ' 34CL2cL {+33}S(p,|g); L=1+3 from 0+ in {+36}Ar(d,|a),(pol d,|a) and            '
old_423 = ' 34CL3cL {+32}S(|a,d): L=1 gives 0-,1-,2-; L=3 gives 2-,3-,4-; 2721|g, M2, |DJ=2'
old_424 = ' 34CL4cL to 0+, g.s.                                                             '
# New: L=1+3 gives 2-; collapse 4 → 3 lines
new_421 = old_421
new_422 = make_cL(2, '{+33}S(p,|g); L=1+3 from 0+ in {+36}Ar(d,|a),(pol d,|a) and            ')
new_423 = make_cL(3, '{+32}S(|a,d) gives 2-; 2721|g, M2, |DJ=2 to 0+, g.s.                   ')
# old_424 (4cL) to be REMOVED
show("C6 L2721 line421", old_421, new_421)
show("C6 L2721 line422", old_422, new_422)
show("C6 L2721 line423", old_423, new_423)
print(f"C6 L2721 line424 REMOVE: |{old_424}|")
print()

# ── Change 7: L3129.11 – verbose L=0+2 from 0+ in 36Ar (single J$ line) ──
# Old lines 463-464
old_463 = ' 34CL cL J$L=0+2 from 0+ in {+36}Ar(d,|a),(pol d,|a): L=0 gives 1+; L=2 gives   '
old_464 = ' 34CL2cL 1+,2+,3+.                                                               '
# New: just 1 line
new_463 = make_cL(1, 'J$L=0+2 from 0+ in {+36}Ar(d,|a),(pol d,|a) gives 1+.                 ')
# old_464 (2cL) to be REMOVED
show("C7 L3129 line463", old_463, new_463)
print(f"C7 L3129 line464 REMOVE: |{old_464}|")
print()

# ── Change 8: L4786.00 – L=1+3,3,4 verbose: fix L=1+3 sub-clause ──────────
# Old lines 973-974
old_973 = ' 34CL cL J$L=1+3,3,4 from 0+ in {+32}S(|a,d): L=1 gives 0-,1-,2-; L=3 gives     '
old_974 = ' 34CL2cL 2-,3-,4-; L=4 gives 3+,4+,5+.                                          '
# New: L=1+3 gives 2- (intersection); L=3 and L=4 kept
new_973 = make_cL(1, 'J$L=1+3,3,4 from 0+ in {+32}S(|a,d): L=1+3 gives 2-; L=3 gives         ')
new_974 = make_cL(2, '2-,3-,4-; L=4 gives 3+,4+,5+.                                          ')
show("C8 L4786 line973", old_973, new_973)
show("C8 L4786 line974", old_974, new_974)

# ── Group B: Missing "gives" for L=0+2 from 3/2+ (no verbose sub-clauses) ──

# L2718, L4075, L4136.6, L4211, L4325.89 all have:
# " 34CL cL J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a)."
# Need to add "gives 1+,2+"

cases_B = [
    ("L2718  (407)", 'J$L=2 from 3/2+ in {+35}Cl({+3}He,|a).',
                     'J$L=2 from 3/2+ in {+35}Cl({+3}He,|a) gives 0+,1+,2+,3+,4+.      '),
    ("L4075  (720)", 'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a).',
                     'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a) gives 1+,2+.              '),
    ("L4136  (742)", 'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a).',
                     'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a) gives 1+,2+.              '),
    ("L4211  (776)", 'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a).',
                     'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a) gives 1+,2+.              '),
    ("L4325  (784)", 'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a).',
                     'J$L=0+2 from 3/2+ in {+35}Cl({+3}He,|a) gives 1+,2+.              '),
]
for label, old_text, new_text in cases_B:
    old_line = (' 34CL cL ' + old_text).ljust(80)
    new_line = (' 34CL cL ' + new_text).ljust(80)
    # Trim if over 80
    if len(new_line) > 80:
        new_line = new_line[:80]
    show(f"B {label}", old_line, new_line)

# Also L234 E=1923.30 and L407 E=2718.00 single-L missing gives
print("--- Single-L adds ---")
# L234 E=1923.30
old_234 = ' 34CL cL J$L=2 from 3/2+ in {+33}S({+3}He,d).                                  '
new_234 = make_cL(1, 'J$L=2 from 3/2+ in {+33}S({+3}He,d) gives 0+,1+,2+,3+,4+.          ')
show("L1923 (234)", old_234, new_234)
