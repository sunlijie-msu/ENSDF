"""Robust provenance: find tool-call occurrences of the 3 non-flag changes."""
import io

T = r"c:\Users\sun\AppData\Roaming\Code\User\workspaceStorage\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\transcripts\871d2455-0101-4b6a-a2d6-afd68693d02b.jsonl"
txt = io.open(T, encoding="utf-8", errors="replace").read()
print("len:", len(txt))

NEEDLES = ["BAND. Will be changed later.",
           "G 10406        100       (E2)",
           "J$E2 |DJ=2 |g to 0+, g.s."]

for nd in NEEDLES:
    idxs = []
    i = txt.find(nd)
    while i >= 0:
        idxs.append(i)
        i = txt.find(nd, i + 1)
    edit_hits = []
    for i in idxs:
        prev = txt[max(0, i - 300):i]
        if ('newString\\":\\"' in prev) or ('oldString\\":\\"' in prev):
            edit_hits.append(i)
    print(f"\n{nd!r}: total={len(idxs)} | first={idxs[0] if idxs else None} | in-edit-hits={edit_hits[:6]}")
    if edit_hits:
        i = edit_hits[0]
        print("  context:", txt[max(0, i - 220): i + 160].replace("\\n", " / "))
