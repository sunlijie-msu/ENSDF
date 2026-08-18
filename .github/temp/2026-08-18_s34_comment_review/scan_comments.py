import re
import sys
from pathlib import Path

FOLDER = Path(r"A34/S34/new")
SKIP = {"S34_adopted.ens"}

# comment record detection: column 7 = 'c' (or continuation c with col6 alnum)
def is_comment(line: str) -> bool:
    if len(line) < 8:
        return False
    col6 = line[5]
    col7 = line[6]
    if col7 == "c":
        return True
    return False

def review_file(path: Path):
    findings = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not is_comment(raw):
            continue
        line = raw
        text = line[9:]  # comment text starts col 10
        # 1. Unicode leakage
        for ch in text:
            if ord(ch) > 127:
                findings.append((n, "unicode", repr(text[:60]), f"U+{ord(ch):04X}"))
        # 2. Plain isotope tokens: digit(s)+element not braced
        for m in re.finditer(r"(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b", text):
            tok = m.group(0)
            # exclude tokens followed by | (e.g., 2I|g)
            after = text[m.end():m.end()+1]
            if after == "|":
                continue
            findings.append((n, "isotope", tok, text[:70]))
        # 3. Bare I prefix
        for m in re.finditer(r"\bI\d{1,3}\b", text):
            findings.append((n, "bare-I", m.group(0), text[:70]))
        # 4. Extra space after =
        for m in re.finditer(r"=\s[0-9]", text):
            findings.append((n, "space-after-eq", text[max(0,m.start()-15):m.end()+5], text[:70]))
        # 5. Extra space after $
        for m in re.finditer(r"\$\s", text):
            findings.append((n, "space-after-dollar", text[max(0,m.start()-10):m.end()+5], text[:70]))
        # 6. Dittography
        for m in re.finditer(r"\b(\w+)\s+\1\b", text):
            findings.append((n, "dittography", m.group(0), text[:70]))
        # 7. 10{-n} negative exponent-as-subscript
        for m in re.finditer(r"10\{-\d+\}", text):
            findings.append((n, "neg-exp-subscript", m.group(0), text[:70]))
        # 8. non-ENSDF unit spellings
        for m in re.finditer(r"\bug\b|cm2|mg/cm2|\bmm\b(?![a-z])", text):
            findings.append((n, "unit-spelling", m.group(0), text[:70]))
        # 9. mixed symbol-text
        for m in re.finditer(r"\b(?:gamma|beta|mu)-|gamma ray|beta delay", text):
            findings.append((n, "mixed-symbol", m.group(0), text[:70]))
        # 10. leaked record tags
        for m in re.finditer(r"\s(cL|cG|cB|cE|cN|cP|cQ)\s", text):
            findings.append((n, "leaked-tag", m.group(0), text[:70]))
    return findings

def main():
    total = 0
    for path in sorted(FOLDER.glob("*.ens")):
        if path.name in SKIP:
            continue
        finds = review_file(path)
        if not finds:
            continue
        print(f"=== {path.name} ({len(finds)}) ===")
        for n, cat, detail, ctx in finds:
            print(f"  L{n} [{cat}] {detail!r} | {ctx!r}")
        total += len(finds)
    print(f"\nTOTAL FINDINGS: {total}")

if __name__ == "__main__":
    main()
