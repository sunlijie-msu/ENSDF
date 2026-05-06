import glob
import re

ELEMENTS = {
    "H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y",
    "Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce",
    "Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir",
    "Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn",
}

TOKEN_RE = re.compile(r"(?<!\{\+)\b(\d{1,3})([A-Z][a-z]?)(?!\|)\b")

for path in sorted(glob.glob(r"A35/**/new/*.ens", recursive=True)):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            if len(line) < 10:
                continue
            if line[6] != "c":
                continue
            text = line[9:]
            bad = []
            for m in TOKEN_RE.finditer(text):
                token = m.group(0)
                elem = m.group(2)
                if elem in ELEMENTS:
                    bad.append(token)
            if bad:
                uniq = ",".join(sorted(set(bad)))
                print(f"{path}\t{i}\t{uniq}\t{line.rstrip()}")
