"""Precise re-audit of the 40 converted width values: comment text <-> source datasets."""
import re
from pathlib import Path

WORK = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()
SRC = {
    "L": Path("A34/S34/new/S34_30si_a_g_a_n_resonances.ens").read_text(encoding="utf-8"),
    "Q": Path("A34/S34/new/S34_33s_n_g_n_n_resonances.ens").read_text(encoding="utf-8"),
}
EXPECT = {
    "10494": ([("=0.84 eV", "L")]),
    "10587": ([(">1.3 eV", "L")]),
    "10625": ([(">0.7 eV", "L")]),
    "10670": ([("=0.73 eV", "L")]),
    "10790": ([("=3 eV", "L")]),
    "11088": ([("=0.2 eV", "L")]),
    "11142": ([("=2.6 eV", "L")]),
    "11165": ([("=1.7 eV", "L")]),
    "11220": ([("=0.2 eV", "L")]),
    "11233": ([("=2.8 eV", "L")]),
    "11315": ([("=0.08 eV", "L")]),
    "11323": ([("=2.2 eV", "L")]),
    "11358": ([("=1.4 eV", "L")]),
    "11372": ([("=1.5 eV", "L")]),
    "11381": ([("=0.1 eV", "L")]),
    "11420": ([("=4.4 eV", "L")]),
    "11545": ([("=1.0 eV", "L")]),
    "11643": ([("=2.3 eV", "L")]),
    "11411.31": ([("=1.5 eV", "Q")]),
    "11430.3": ([("|G{-n}=75.0 eV", "Q"), ("|G{-|g}=0.21 eV", "Q"), ("|G{-|a}=41 eV", "Q")]),
    "11434.3": ([("|G{-n}=39.1 eV", "Q"), ("|G{-|g}=0.90 eV", "Q")]),
    "11440.4": ([("|G{-n}=16.0 eV", "Q"), ("|G{-|g}=1.44 eV", "Q"), ("|G{-|a}=2.5 eV", "Q")]),
    "11474.51": ([("|G{-n}=275 eV", "Q"), ("|G{-|g}=1.08 eV", "Q"), ("|G{-|a}=0.17 keV", "Q")]),
    "11490": ([("|G{-n}=65 eV", "Q"), ("|G{-|a}=0.11 keV", "Q"), ("|G{-|g}=0.6 eV", "L")]),
    "11492.7": ([("|G{-n}=507 eV", "Q"), ("|G{-|g}=2.11 eV", "Q")]),
    "11496.2": ([("|G{-n}=705 eV", "Q"), ("|G{-|g}=0.94 eV", "Q"), ("|G{-|a}=4 eV", "Q")]),
    "11499.6": ([("|G{-n}=1.33 keV", "Q"), ("|G{-|a}=4.0 keV", "Q")]),
    "11502.3": ([("|G{-n}=280 eV", "Q"), ("|G{-|g}=2.11 eV", "Q"), ("|G{-|a}=10 eV", "Q")]),
    "11515.3": ([("|G{-n}=1.260 keV", "Q"), ("|G{-|g}=1.48 eV", "Q")]),
    "11541": ([("|G{-n}=0.36 keV", "Q"), ("|G{-|g}=1.4 eV", "Q"), ("|G{-|a}=0.27 keV", "Q")]),
    "11581": ([("|G{-n}=3.42 keV", "Q"), ("|G{-|g}=2.6 eV", "Q")]),
    "11590": ([("|G{-n}=0.76 keV", "Q"), ("|G{-|g}=0.87 eV", "Q")]),
    "11608": ([("|G{-n}=0.61 keV", "Q"), ("|G{-|g}=1.33 eV", "Q")]),
    "11614": ([("|G{-n}=2.09 keV", "Q"), ("|G{-|g}=2.17 eV", "Q"), ("|G{-|a}=14 eV", "Q")]),
    "11632": ([("|G{-n}=0.69 keV", "Q"), ("|G{-|g}=1.2 eV", "Q"), ("|G{-|a}=55 eV", "Q")]),
    "11634": ([("|G{-n}=4.4 keV", "Q"), ("|G{-|a}=0.9 keV", "Q")]),
    "11638.93": ([("|G{-n}=0.76 keV", "Q"), ("|G{-|g}=0.81 eV", "Q"), ("|G{-|a}=0.20 keV", "Q")]),
    "11648.64": ([("|G{-n}=0.46 keV", "Q"), ("|G{-|g}=1.82 eV", "Q")]),
    "11669": ([("|G{-n}=0.67 keV", "Q"), ("|G{-|g}=2.4 eV", "Q")]),
    "11670": ([("|G{-n}=0.23 keV", "Q"), ("|G{-|g}=2.1 eV", "Q")]),
}


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


ok = absent = bad = 0
for level, fields in EXPECT.items():
    idx = next((i for i, s in enumerate(WORK, 1) if is_lrec(s) and s[9:19].strip() == level), None)
    if idx is None:
        print(f"ABSENT {level:9s} level not in working file (user-edited region - not touched)")
        absent += 1
        continue
    comments = " ".join(WORK[j - 1].rstrip() for j in range(idx + 1, len(WORK) + 1)
                        if not is_lrec(WORK[j - 1]) and WORK[j - 1][6:8] == "cL")
    missing = [(f, src) for f, src in fields if f not in comments]
    for f, src in fields:
        value = re.search(r"\d+\.?\d*", f.split("=", 1)[-1]).group(0)
        if value not in SRC[src]:
            missing.append((f"source:{value}", src))
    if missing:
        print(f"FAIL    {level:9s} {missing}")
        bad += 1
    else:
        ok += 1
print(f"\nlevels OK {ok} | absent(user region) {absent} | FAIL {bad}")
