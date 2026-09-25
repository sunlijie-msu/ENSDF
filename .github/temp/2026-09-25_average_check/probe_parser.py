"""Probe why Java_Average.py's comment parser drops an input for line 202."""
import io
import re
import sys

sys.path.insert(0, r"d:\X\ND\ENSDF\.github\scripts")
import Java_Average as JA

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
with io.open(AD, newline="") as fh:
    lines = fh.read().replace("\r\n", "\n").split("\n")

raw = lines[201:204]  # lines 202-204 (1-based)
text_in = "\n".join(raw)
print("RAW:")
for r in raw:
    print("  %r" % r)

data, base_unit, dec = JA.parse_comment_data(text_in)
print()
print("parsed points:", len(data))
for d in data:
    print("   ", d)

# replicate cleaning to show intermediate text
cleaned = []
for line in text_in.split("\n"):
    s = re.sub(r'^\s*[0-9]{0,3}[A-Za-z]{1,2}\s*\d?c[Ll]\s*(?:T\$)?\s*', '', line, flags=re.I)
    s = re.sub(r'^\s*\d{1,3}\s*[A-Za-z]{1,2}\s+\d?c[Ll]\s*(?:T\$)?\s*', '', s, flags=re.I)
    cleaned.append(s)
t = " ".join(cleaned)
t = re.sub(r"\s+", " ", t).strip()
print()
print("after prefix strip:", repr(t))
m = re.search(r"\bOthers?\b", t, re.I)
if m:
    print("truncated at Other:", repr(t[:m.start()]))
    t = t[:m.start()]
m = re.search(r"\baverage\s+of\b", t, re.I)
if m:
    t = t[m.end():]
print("after 'average of' cut:", repr(t))
print()
NUMBER_RE = r"(?:\d+\.?\d*|\.\d+)"
UNIT_RE = r"(?:fs|ps|ns|us|ms|eV|keV|MeV|s|m|h|d|y)\b"
PAT = re.compile(r"(" + NUMBER_RE + r")\s*(" + UNIT_RE + r")?\s*(?:\{I([^}]+)\}|\(([^)]+)\))", re.I)
for mm in PAT.finditer(t):
    print("   match:", mm.group(0), "| val=", mm.group(1), "unit=", mm.group(2), "I=", mm.group(3), "paren=", mm.group(4))
