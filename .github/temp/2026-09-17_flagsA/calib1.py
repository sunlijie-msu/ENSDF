"""Calibrate my hand-typed literal against the file (one probe per intent).

Prints: total length, position of 'A', pre-A run length, match count.
"""
P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")

SUF = "\n 34S X L XREF=L         "

# --- probe: intent = 56 spaces before A, then "A" + 3 spaces ---
V = " 34S   L 10447     5                                                        A   " + SUF

print("len:", len(V))
a = V.index("A")
print("A pos:", a, " pre-A run:", a - 20, " tail-after-A:", len(V) - a - 1 - len(SUF))
print("count in file:", raw.count(V))
print("repr head:", repr(V[:40]))
print("repr mid :", repr(V[75:110]))
