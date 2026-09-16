"""Final verification: every converted level carries its expected width comment; no WIDTH records remain."""
from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()

EXPECT = {
    "10494": ["|G{-|g}=0.84 eV", "{+30}Si"],
    "10587": ["|G{-|g}>1.3 eV", "{+30}Si"],
    "10625": ["|G{-|g}>0.7 eV", "{+30}Si"],
    "10670": ["|G{-|g}=0.73 eV", "{+30}Si"],
    "10790": ["|G{-|g}=3 eV", "{+30}Si"],
    "11088": ["|G{-|g}=0.2 eV", "{+30}Si"],
    "11142": ["|G{-|g}=2.6 eV", "{+30}Si"],
    "11165": ["|G{-|g}=1.7 eV", "{+30}Si"],
    "11220": ["|G{-|g}=0.2 eV", "{+30}Si"],
    "11233": ["|G{-|g}=2.8 eV", "{+30}Si"],
    "11315": ["|G{-|g}=0.08 eV", "{+30}Si"],
    "11323": ["|G{-|g}=2.2 eV", "{+30}Si"],
    "11358": ["|G{-|g}=1.4 eV", "{+30}Si"],
    "11372": ["|G{-|g}=1.5 eV", "{+30}Si"],
    "11381": ["|G{-|g}=0.1 eV", "{+30}Si"],
    "11411.31": ["|G{-|g}=1.5 eV", "{+33}S"],
    "11420": ["|G{-|g}=4.4 eV", "{+30}Si"],
    "11545": ["|G{-|g}=1.0 eV", "{+30}Si"],
    "11643": ["|G{-|g}=2.3 eV", "{+30}Si"],
    "11430.3": ["|G{-n}=75.0 eV {I8}", "|G{-|g}=0.21 eV {I5}", "|G{-|a}=41 eV {I5}", "{+33}S"],
    "11434.3": ["|G{-n}=39.1 eV {I8}", "|G{-|g}=0.90 eV {I5}", "{+33}S"],
    "11440.4": ["|G{-n}=16.0 eV {I9}", "|G{-|g}=1.44 eV {I10}", "|G{-|a}=2.5 eV {I3}", "{+33}S"],
    "11474.51": ["|G{-n}=275 eV {I5}", "|G{-|g}=1.08 eV {I7}", "|G{-|a}=0.17 keV {I5}", "{+33}S"],
    "11490": ["|G{-n}=65 eV {I10}", "|G{-|a}=0.11 keV {I6}", "|G{-|g}=0.6 eV", "{+30}Si"],
    "11492.7": ["|G{-n}=507 eV {I13}", "|G{-|g}=2.11 eV {I14}", "{+33}S"],
    "11496.2": ["|G{-n}=705 eV {I19}", "|G{-|g}=0.94 eV {I6}", "|G{-|a}=4 eV {I2}", "{+33}S"],
    "11499.6": ["|G{-n}=1.33 keV {I8}", "|G{-|a}=4.0 keV {I6}", "{+33}S"],
    "11502.3": ["|G{-n}=280 eV {I20}", "|G{-|g}=2.11 eV {I14}", "|G{-|a}=10 eV {I5}", "{+33}S"],
    "11515.3": ["|G{-n}=1.260 keV {I25}", "|G{-|g}=1.48 eV {I13}", "{+33}S"],
    "11541": ["|G{-n}=0.36 keV {I4}", "|G{-|g}=1.4 eV {I4}", "|G{-|a}=0.27 keV {I6}", "{+33}S"],
    "11581": ["|G{-n}=3.42 keV {I8}", "|G{-|g}=2.6 eV {I3}", "{+33}S"],
    "11590": ["|G{-n}=0.76 keV {I4}", "|G{-|g}=0.87 eV {I11}", "{+33}S"],
    "11608": ["|G{-n}=0.61 keV {I3}", "|G{-|g}=1.33 eV {I12}", "{+33}S"],
    "11614": ["|G{-n}=2.09 keV {I8}", "|G{-|g}=2.17 eV {I20}", "|G{-|a}=14 eV {I5}", "{+33}S"],
    "11632": ["|G{-n}=0.69 keV {I7}", "|G{-|g}=1.2 eV {I4}", "|G{-|a}=55 eV {I20}", "{+33}S"],
    "11634": ["|G{-n}=4.4 keV {I9}", "|G{-|a}=0.9 keV {I3}", "{+33}S"],
    "11638.93": ["|G{-n}=0.76 keV {I5}", "|G{-|g}=0.81 eV {I13}", "|G{-|a}=0.20 keV {I3}", "{+33}S"],
    "11648.64": ["|G{-n}=0.46 keV {I3}", "|G{-|g}=1.82 eV {I20}", "{+33}S"],
    "11669": ["|G{-n}=0.67 keV {I6}", "|G{-|g}=2.4 eV {I2}", "{+33}S"],
    "11670": ["|G{-n}=0.23 keV {I7}", "|G{-|g}=2.1 eV {I3}", "{+33}S"],
}


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


ok = bad = 0
for lev, needles in EXPECT.items():
    idx = next((i for i, s in enumerate(L, 1) if is_lrec(s) and s[9:19].strip() == lev), None)
    if idx is None:
        print(f"FAIL {lev}: level not found")
        bad += 1
        continue
    blk = []
    for j in range(idx + 1, len(L) + 1):
        s = L[j - 1]
        if is_lrec(s):
            break
        if s[6:8] in ("cL",) or s[6:8].endswith("cL"):
            blk.append(s)
    joined = "\n".join(blk)
    missing = [n for n in needles if n not in joined]
    if missing:
        print(f"FAIL {lev}: missing {missing}")
        bad += 1
    else:
        ok += 1
print(f"\nlevels verified OK: {ok}   FAIL: {bad}")

print("\nWIDTH records remaining:", sum(1 for s in L if s[7:8] == "L" and s[5:6] == "2" and "WIDTH" in s))
print("total lines:", len(L))
