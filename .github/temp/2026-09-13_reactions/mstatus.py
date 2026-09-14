path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
print("=== remaining 'E,RI$from {+31}P' comments ===")
for i, ln in enumerate(lines, 1):
    if "E,RI$from {+31}P" in ln:
        print("  line %-5d %s" % (i, ln.rstrip()))
print()
print("=== the 10 targets: length / col77 / following comment ===")
for e in ["1856", "2043", "3428", "4604", "2176", "2242", "4737", "3809", "4985", "7111"]:
    for i, ln in enumerate(lines):
        if len(ln) > 7 and ln[7] == "G" and ln[6] == " " and ln[9:19].strip() == e:
            nxt = lines[i + 1].rstrip() if i + 1 < len(lines) else ""
            print("  E=%-6s line %-5d len=%-3d col77=%r |%s|" % (e, i + 1, len(ln), ln[76:77], nxt))
            break
print()
print("=== any malformed G record (energy field not ending at col 19) ===")
import re
for i, ln in enumerate(lines, 1):
    if len(ln) > 7 and ln[7] == "G" and ln[6] == " ":
        e = ln[9:19]
        if e.strip() and not re.match(r"^[ ]*[0-9.]+[A-Za-z0-9]*\s*$", e):
            print("  line %-5d col10-19=%r |%s|" % (i, e, ln.rstrip()[:40]))
