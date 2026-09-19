import glob
import os
import re
import sys

raw = open(r"A34\S34\raw\XREF.log", "r", encoding="utf-8", errors="replace").read().splitlines()
key = {}
for l in raw:
    m = re.match(r"\s*34S\s+X\s+(\S+)\s+(.*?)\s*$", l)
    if m:
        key[m.group(1)] = m.group(2).strip()

files = {}
for p in glob.glob(r"A34\S34\new\S34_*.ens"):
    base = os.path.basename(p)
    for k, v in key.items():
        norm = re.sub(r"[^A-Za-z0-9]", "", v).lower()
        fb = re.sub(r"[^A-Za-z0-9]", "", base.replace("S34_", "")).lower()
        if norm[:12] and norm[:12] in fb:
            files[k] = p
    files.setdefault("?", p)


def levels(path):
    ls = open(path, "rb").read().decode().split("\r\n")
    out = []
    for i, l in enumerate(ls):
        if len(l) > 7 and l[6] == " " and l[7] == "L" and l[5] == " ":
            out.append((i + 1, l[9:19].strip(), l[19:21].strip(), l[22:39].strip()))
    return out


ds = {}
for k, p in sorted(files.items()):
    ds[k] = (p, levels(p))

print("letter -> file")
for k, (p, lv) in sorted(ds.items()):
    print("  %-2s %-60s %d levels" % (k, os.path.basename(p), len(lv)))
