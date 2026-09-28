import pathlib
src = pathlib.Path(r"D:\X\ND\Files\A34\finished")
ws = pathlib.Path("A34")
with_tail = []
for p in sorted(src.rglob("*.ens")):
    lines = p.read_bytes().decode("utf-8", errors="replace").split("\n")
    tail = lines[-2] if len(lines) >= 2 else ""
    if tail == " " * 80:
        with_tail.append(str(p.relative_to(src)))
print(f"source files ending with an 80-space line: {len(with_tail)} / {len(list(src.rglob('*.ens')))}")
for t in with_tail[:5]: print("   ", t)
print()
n = 0
for p in sorted(ws.rglob("*.ens")):
    lines = p.read_bytes().decode("utf-8", errors="replace").split("\n")
    tail = lines[-2] if len(lines) >= 2 else ""
    if tail == " " * 80: n += 1
print(f"workspace files ending with an 80-space line: {n} / {len(list(ws.rglob('*.ens')))}")
m = (ws / "merged.ens").read_bytes().decode("utf-8", errors="replace").split("\n")
print("merged.ens second-to-last line:", repr(m[-2]), "last:", repr(m[-1]))
