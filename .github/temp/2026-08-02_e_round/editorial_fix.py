"""Build corrected comment lines for editorial review, verify 80 chars."""
PATH = r"A34\Cl34\new\Cl34_34cl_it_decay_31.99_m.ens"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

def rep(lineno, old, new):
    """Replace old with new in line, re-pad to 80."""
    ln = lines[lineno - 1]
    assert old in ln, f"L{lineno}: '{old}' not found: {ln!r}"
    fixed = ln.rstrip().replace(old, new, 1)
    assert len(fixed) <= 80, f"L{lineno}: too long {len(fixed)}"
    return fixed.ljust(80)

# (lineno, old, new)
edits = [
    (5, "of {+34}Cl 146-keV", "of the {+34}Cl 146-keV"),
    (8, "Al forils", "Al foils"),
    (9, "Deduced 34S", "Deduced {+34}S"),
    (28, "Mass separated sources", "Mass-separated sources"),
    (31, "Viliigen", "Villigen"),
    (67, "the 34Cl{+m} and 34Cl g.s.", "the {+34}Cl{+m} and {+34}Cl g.s."),
]

for no, old, new in edits:
    out = rep(no, old, new)
    print(f"L{no}: len={len(out)}")
    print(f"  OLD [{lines[no-1]}]")
    print(f"  NEW [{out}]")
    print()
