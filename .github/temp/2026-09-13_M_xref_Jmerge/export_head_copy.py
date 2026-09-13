"""Write the pre-edit (HEAD) revision of the adopted file into .github/temp for baseline validation."""
import subprocess

OUT = r"D:/X/ND/ENSDF/.github/temp/2026-09-13_M_xref_Jmerge/head_adopted_before.txt"

res = subprocess.run(
    ["git", "show", "HEAD:A34/S34/new/S34_adopted.ens"],
    cwd=r"D:/X/ND/ENSDF",
    capture_output=True,
    check=True,
)
with open(OUT, "wb") as fh:
    fh.write(res.stdout)
print("WROTE", OUT, len(res.stdout), "bytes")
