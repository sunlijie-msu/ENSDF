import subprocess

p = r"A34\S34\new\S34_34s_e_eP.ens"
b = open(p, "rb").read()
print("file bytes:", len(b))
print("CRLF count:", b.count(b"\r\n"), "| lone LF count:", b.replace(b"\r\n", b"").count(b"\n"))
lines = b.split(b"\r\n")
if lines and lines[-1] == b"":
    lines = lines[:-1]
print("new total lines:", len(lines))
bad = [(i, len(l)) for i, l in enumerate(lines, 1) if len(l) != 80]
print("new non-80 lines:", len(bad), bad[:20])
na = [i for i, l in enumerate(lines, 1) if any(c > 127 for c in l)]
print("new non-ASCII lines:", len(na), na[:10])
for tok in [b"**", b"\\", b"^", b"_", b"circ", b"Lambda", b"frac", b"left", b"mathrm"]:
    hits = [i for i, l in enumerate(lines, 1) if tok in l]
    if hits:
        print("TOKEN FOUND:", tok, hits)
print("token scan done (only found tokens listed)")

seq = []
for i, l in enumerate(lines, 1):
    if l[6:7] == b"c":
        seq.append(str(i) + ":" + l[5:6].decode("ascii", "replace") + "c")
print("comment label seq:", " ".join(seq))

print("lines 16-24 (rstripped repr):")
for i in range(15, min(24, len(lines))):
    print(i + 1, repr(lines[i].rstrip(b" ").decode("ascii", "replace")))

oldb = subprocess.run(["git", "show", "HEAD:A34/S34/new/S34_34s_e_eP.ens"], capture_output=True).stdout
oldlines = [x.rstrip("\r") for x in oldb.decode("utf-8", "replace").split("\n")]
if oldlines and oldlines[-1] == "":
    oldlines = oldlines[:-1]
print("OLD total lines:", len(oldlines))
print("OLD >80 lines:", [(i, len(l)) for i, l in enumerate(oldlines, 1) if len(l) > 80][:5])
print("OLD Magnetic lines:", [(i, len(l)) for i, l in enumerate(oldlines, 1) if "Magnetic" in l])

d = subprocess.run(["git", "diff", "--", "A34/S34/new/S34_34s_e_eP.ens"], capture_output=True).stdout.decode("utf-8", "replace")
added = [l[1:] for l in d.split("\n") if l.startswith("+") and not l.startswith("+++")]
removed = [l[1:] for l in d.split("\n") if l.startswith("-") and not l.startswith("---")]
print("diff added:", len(added), "| all col7=c:", all(len(l) >= 7 and l[6] == "c" for l in added))
print("diff removed:", len(removed), "| all col7=c:", all(len(l) >= 7 and l[6] == "c" for l in removed))
for l in added:
    print("ADDED", repr(l[5:7]), "len", len(l), "head:", l[:70])
for l in removed:
    print("REMOVED", repr(l[5:7]), "len", len(l), "head:", l[:70])
