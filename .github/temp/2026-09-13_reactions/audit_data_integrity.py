#!/usr/bin/env python3
"""Audit: byte-for-byte compare ten L-records (current vs HEAD).

Also reports each line's total length. PASS requires:
  * byte-identical to HEAD
  * exactly 80 characters long
"""
import subprocess

TARGET = "A34/S34/new/S34_adopted.ens"
REPO = r"d:\X\ND\ENSDF"
WANTED = [11506, 11712, 12460, 12660, 12985.5, 13590, 13790, 14430, 14576.5, 15244.4]


def head_bytes():
    return subprocess.run(
        ["git", "show", f"HEAD:{TARGET}"], cwd=REPO,
        capture_output=True,
    ).stdout.split(b"\n")


def cur_bytes():
    with open(rf"{REPO}\A34\S34\new\S34_adopted.ens", "rb") as f:
        return f.read().split(b"\n")


def is_level_record(b: bytes) -> bool:
    # cols 1-5 NUCID, col 6 cont, col 7 blank, col 8 'L', col 9 blank
    return len(b) >= 9 and b[6:7] == b" " and b[7:8] == b"L" and b[8:9] == b" "


def efield(b: bytes) -> float | None:
    try:
        return float(b[9:19].decode().strip())
    except ValueError:
        return None


def index(lines):
    d = {}
    for i, b in enumerate(lines):
        if is_level_record(b):
            e = efield(b)
            if e is not None:
                d[round(e, 1)] = (i + 1, b)
    return d


head = index(head_bytes())
cur = index(cur_bytes())

print(f"{'E':>10} | {'HEAD L#':>7} {'CUR L#':>6} | {'HEADlen':>7} {'CURlen':>6} | "
      f"{'BYTE-IDENTICAL':>14} | {'==80':>4}")
print("-" * 78)
allpass = True
for e in WANTED:
    key = round(e, 1)
    h = head.get(key)
    c = cur.get(key)
    if h is None or c is None:
        print(f"{e:>10} | {'MISSING':>7} {'':>6} |  HEAD={h is not None} CUR={c is not None}")
        allpass = False
        continue
    hl, hb = h
    cl, cb = c
    ident = hb == cb
    len80 = len(cb) == 80
    allpass &= ident and len80
    print(f"{e:>10} | {hl:>7} {cl:>6} | {len(hb):>7} {len(cb):>6} | "
          f"{str(ident):>14} | {str(len80):>4}")

print("-" * 78)
print("ALL TEN PASS" if allpass else "FAIL")

print("\n=== Raw current lines (repr, to expose trailing spaces) ===")
for e in WANTED:
    c = cur.get(round(e, 1))
    if c:
        print(f"{e:>10} L{c[0]}: {c[1]!r}")

print("\n=== Raw HEAD lines (repr) ===")
for e in WANTED:
    h = head.get(round(e, 1))
    if h:
        print(f"{e:>10} L{h[0]}: {h[1]!r}")
