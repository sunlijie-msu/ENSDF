"""Report exact bytes of target comment lines + global comment stats (check-only)."""
import sys

P = r"A34/S34/new/S34_34s_e_eP.ens"
raw = open(P, encoding="utf-8", newline="").read()
print("has CR:", "\r" in raw)
lines = raw.split("\n")
print("total split parts:", len(lines))


def is_comment(l):
    return len(l) > 7 and l[6] == "c"


print("--- header/comment region lines 1-20 ---")
for i in range(1, 21):
    if i - 1 >= len(lines):
        break
    ln = lines[i - 1]
    print(i, len(ln), repr(ln))

print("--- all comment lines: anomalies ---")
ncom = 0
for i, ln in enumerate(lines, 1):
    if is_comment(ln):
        ncom += 1
        flags = []
        if len(ln) > 80:
            flags.append("LEN>80")
        if any(ord(ch) > 127 for ch in ln):
            flags.append("NONASCII")
        if "**" in ln or "\\\\" in ln or "_{" in ln or "^" in ln:
            flags.append("MD/LATEX")
        if "\t" in ln:
            flags.append("TAB")
        if flags:
            print(i, len(ln), flags, repr(ln[:120]))
print("comment lines:", ncom)

print("--- tail lines ---")
for i in range(max(1, len(lines) - 4), len(lines) + 1):
    ln = lines[i - 1]
    print(i, len(ln), repr(ln))
