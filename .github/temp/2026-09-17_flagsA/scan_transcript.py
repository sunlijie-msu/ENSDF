"""Scan conversation transcript for the 3 non-flag working-tree changes."""
import io

T = r"c:\Users\sun\AppData\Roaming\Code\User\workspaceStorage\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\transcripts\871d2455-0101-4b6a-a2d6-afd68693d02b.jsonl"
txt = io.open(T, encoding="utf-8", errors="replace").read()
print("transcript chars:", len(txt))
for needle in ["changed later", "GS BAND. Will", "J$E2 |DJ=2 |g to 0+",
               "(E2)                                            ",
               "G 10406"]:
    n = txt.count(needle)
    print(f"count {n:4d} | {needle!r}")
