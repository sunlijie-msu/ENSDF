"""Flag transcript occurrences that sit inside edit tool calls (oldString/newString context)."""
import io

T = r"c:\Users\sun\AppData\Roaming\Code\User\workspaceStorage\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\transcripts\871d2455-0101-4b6a-a2d6-afd68693d02b.jsonl"
txt = io.open(T, encoding="utf-8", errors="replace").read()

def show(needle, win=500):
    i = 0
    found_edit = 0
    while True:
        i = txt.find(needle, i)
        if i < 0:
            break
        ctx = txt[max(0, i - win): i + win]
        is_edit = ('oldString' in ctx) or ('newString' in ctx)
        kind = "EDIT-CALL" if is_edit else "other"
        if is_edit:
            found_edit += 1
            print(f"=== {needle!r} @ {i} -> {kind}")
            print(ctx[:1000].replace("\\n", " / "))
            print()
            if found_edit >= 4:
                break
        i += 1
    if found_edit == 0:
        print(f"--- {needle!r}: NO occurrences inside edit calls")

show("changed later")
show("GS BAND. Will")
show("J$E2 |DJ=2 |g to 0+")
