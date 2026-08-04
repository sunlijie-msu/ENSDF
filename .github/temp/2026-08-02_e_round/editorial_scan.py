"""Editorial review regex sweeps on Cl34_34cl_it_decay_31.99_m.ens comment lines."""
import re

PATH = r"A34\Cl34\new\Cl34_34cl_it_decay_31.99_m.ens"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

def is_comment(ln):
    return len(ln) >= 9 and ln[6] == "c"

print("=== NON-ASCII ===")
for i, ln in enumerate(lines, 1):
    bad = [c for c in ln if ord(c) > 127]
    if bad:
        print(f"L{i}: {bad}")

print("=== PLAIN ISOTOPE TOKENS (regex) ===")
pat = re.compile(r"(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b")
for i, ln in enumerate(lines, 1):
    if not is_comment(ln):
        continue
    for m in pat.finditer(ln):
        tok = m.group(0)
        # skip tokens followed by | (e.g., 2I|g) and valid spin/NSR patterns
        after = ln[m.end():m.end()+1]
        if after == "|":
            continue
        print(f"L{i}: '{tok}' ctx=[{ln[max(0,m.start()-12):m.end()+8]}]")

print("=== DITTOGRAPHY ===")
for i, ln in enumerate(lines, 1):
    if not is_comment(ln):
        continue
    for m in re.finditer(r"\b(\w+)\s+\1\b", ln):
        print(f"L{i}: '{m.group(0)}'")

print("=== '=' followed by space ===")
for i, ln in enumerate(lines, 1):
    if not is_comment(ln):
        continue
    for m in re.finditer(r"=\s[0-9]", ln):
        print(f"L{i}: [{m.group(0)}] ctx=[{ln[max(0,m.start()-15):m.end()+8]}]")

print("=== '$' followed by space ===")
for i, ln in enumerate(lines, 1):
    if not is_comment(ln):
        continue
    for m in re.finditer(r"\$\s", ln):
        print(f"L{i}: ctx=[{ln[max(0,m.start()-10):m.end()+15]}]")

print("=== LEAKED TAGS ===")
for i, ln in enumerate(lines, 1):
    if not is_comment(ln):
        continue
    if re.search(r"\s(cL|cG| c )\s|\b cL \$|\b cG \$", ln):
        print(f"L{i}: {ln[:60]}")

print("=== 10{-n} subscript-as-exponent ===")
for i, ln in enumerate(lines, 1):
    for m in re.finditer(r"10\{-\d+\}", ln):
        print(f"L{i}: {m.group(0)}")
print("done")
