p = r"d:\X\ND\ENSDF\.github\temp\quoted_check\simulated.ens"
t = open(p, "rb").read().decode("ascii")
lines = t.split("\r\n")
# shorten one cL comment line by 5 chars (simulate a transcription pad error)
for i, l in enumerate(lines):
    if l[6:8] == "cL":
        lines[i] = l.rstrip()
        print("shortened line", i + 1, "to", len(lines[i]))
        break
open(r"d:\X\ND\ENSDF\.github\temp\quoted_check\sim_probe.ens", "wb").write(
    "\r\n".join(lines).encode("ascii"))
