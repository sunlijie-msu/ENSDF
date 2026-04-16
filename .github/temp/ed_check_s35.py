import re

fname = r"d:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens"
lines = open(fname, encoding="utf-8").read().splitlines()

def is_comment(ln):
    if len(ln) < 10: return False
    return ln[7] == "c" or ln[6] == "c"

results = []

for i, ln in enumerate(lines, 1):
    if not is_comment(ln): continue
    text = ln[9:80]

    # Inconsistent A-coefficient subscript notation
    has_sub = bool(re.search(r"A\{-[246]\}", text))
    has_plain = bool(re.search(r"\bA[246]=", text))
    if has_sub and has_plain:
        results.append(f"[Subscript inconsistency] Line {i}: {text.strip()}")

    # Unclosed brace (mid-token line break candidate)
    if text.count("{") > text.count("}"):
        results.append(f"[Unclosed brace] Line {i}: {text.rstrip()}")

    # Gamma ray (unhyphenated adjective before noun)
    bad = re.findall(r"\bgamma ray (spectrum|detector|measurement|analysis|coincidence|transition|emission)\b", text, re.IGNORECASE)
    for b in bad:
        results.append(f"[Hyphenation] Line {i}: 'gamma ray {b}' -> 'gamma-ray {b}'")

    # Spelling errors
    tl = text.lower()
    for bad, good in [("deexiting", "deexciting"), ("striped", "stripped"),
                      ("ohter", "other"), ("usign", "using"),
                      ("coeffcients", "coefficients"), ("multiporities", "multipolarities"),
                      ("paretheses", "parentheses"), ("cockroft", "cockcroft")]:
        if bad in tl:
            results.append(f"[Spelling] Line {i}: '{bad}' -> '{good}'")

    # NSR key + non-s verb
    m6 = re.findall(
        r"[12][0-9]{3}[A-Z][a-z][0-9A-Z]{2}\s+"
        r"(measure|report|observe|calculate|deduce|find|show|confirm|suggest|assign|place|determine|identify|establish|note|list|give|provide|use)\b(?!s|d|ing)",
        text)
    for v in m6:
        results.append(f"[Subject-Verb] Line {i}: verb='{v}' needs '{v}s'  -- {text.strip()[:70]}")

    # Dittography
    m = re.search(r"\b(\w+)\s+\1\b", text, re.IGNORECASE)
    if m:
        results.append(f"[Dittography] Line {i}: '{m.group()}'")

    # Bad superscript: element inside braces
    for bad in re.findall(r"\{[+-][0-9]+[A-Z][a-z]?\}", text):
        results.append(f"[ENSDF Notation] Line {i}: '{bad}' -- element must be outside braces")

if not results:
    print("NO FINDINGS -- file is clean")
else:
    for r in results:
        print(r)
