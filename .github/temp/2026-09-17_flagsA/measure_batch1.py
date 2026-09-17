"""Measure actual A position and line lengths for batch-1 edited lines."""
P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
targets = [1084, 1089, 1111, 1119, 1168, 1172, 1176, 1183, 1186, 1195, 1198, 1237, 1276]
for n in targets:
    ln = lines[n - 1]
    idxs = [i + 1 for i, ch in enumerate(ln) if ch != " "]
    apos = [i + 1 for i, ch in enumerate(ln) if ch == "A"]
    print(f"line {n:5d} len={len(ln):3d} A at cols={apos} last-nonspace={idxs[-1] if idxs else None} |{ln}|")
