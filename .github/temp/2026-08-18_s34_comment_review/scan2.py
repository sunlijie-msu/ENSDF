import re
from pathlib import Path

FOLDER = Path(r"A34/S34/new")
SKIP = {"S34_adopted.ens"}

def is_comment(line: str) -> bool:
    return len(line) >= 8 and line[6] == "c"

def review(path: Path):
    out = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not is_comment(raw):
            continue
        text = raw[9:]
        # Unicode
        for ch in text:
            if ord(ch) > 127:
                out.append((n, "unicode", repr(text[:70])))
        # isotope tokens not preceded by {+ and not inside braces already
        for m in re.finditer(r"(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b", text):
            tok = m.group(0)
            if text[m.end():m.end()+1] == "|":
                continue
            # valid element symbols only
            if not re.match(r"^\d{1,3}(H|He|Li|Be|B|C|N|O|F|Ne|Na|Mg|Al|Si|P|S|Cl|Ar|K|Ca|Sc|Ti|V|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Y|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|I|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|W|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|U|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr)$", tok):
                continue
            # exclude tokens that are part of a braced expression (like {+3}He already excluded), also exclude 2J,2J+n patterns (math)
            if re.match(r"^\d{1,3}J", tok):
                continue
            out.append((n, "isotope", f"{tok} | {text[:75]}"))
        # unit spellings
        for m in re.finditer(r"(?<![{|a-zA-Z])\b(ug|cm2|mg/cm2)\b", text):
            out.append((n, "unit", f"{m.group(0)} | {text[:75]}"))
        # bare I (exclude {I...})
        for m in re.finditer(r"(?<!\{)\bI\d{1,3}\b(?!\})", text):
            out.append((n, "bareI", f"{m.group(0)} | {text[:75]}"))
        # dittography
        for m in re.finditer(r"\b(\w+)\s+\1\b", text):
            out.append((n, "ditto", f"{m.group(0)} | {text[:75]}"))
        # extra space after =
        for m in re.finditer(r"=\s[0-9]", text):
            out.append((n, "eqspace", f"{text[max(0,m.start()-10):m.end()+5]} | {text[:75]}"))
        # extra space after $
        for m in re.finditer(r"\$\s", text):
            out.append((n, "dollars", f"{text[max(0,m.start()-6):m.end()+10]} | {text[:75]}"))
        # negative exponent as subscript 10{-n}
        for m in re.finditer(r"10\{-\d+\}", text):
            out.append((n, "negexp", f"{m.group(0)} | {text[:75]}"))
        # mixed symbol text
        for m in re.finditer(r"\b(gamma|beta|mu|alpha)(?:-| ray| delay)", text):
            out.append((n, "mixed", f"{m.group(0)} | {text[:75]}"))
    return out

def main():
    totals = 0
    for path in sorted(FOLDER.glob("*.ens")):
        if path.name in SKIP:
            continue
        f = review(path)
        if not f:
            continue
        print(f"=== {path.name} ({len(f)}) ===")
        for n, cat, det in f:
            print(f"  L{n} [{cat}] {det}")
        totals += len(f)
    print(f"\nTOTAL: {totals}")

if __name__ == "__main__":
    main()
