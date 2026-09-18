"""Scan the tail of the session debug log for hook lifecycle events."""
import re

P = (r"C:\Users\sun\AppData\Roaming\Code\User\workspaceStorage"
     r"\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\debug-logs"
     r"\871d2455-0101-4b6a-a2d6-afd68693d02b\main.jsonl")

pat = re.compile(r'hook', re.IGNORECASE)
tail = []
with open(P, encoding="utf-8", errors="replace") as f:
    for line in f:
        tail.append(line)
    tail = tail[-4000:]

hits = 0
for i, line in enumerate(tail):
    m = pat.search(line)
    if not m:
        continue
    # skip lines that are file-content dumps (contain "def deny" etc.)
    if "def deny" in line or "hookSpecificOutput" in line and "guard_ens" in line:
        continue
    hits += 1
    if hits <= 25:
        s = max(0, m.start() - 150)
        seg = line[s:m.start() + 350]
        print(f"--- tail-line {i}: {seg[:480]}")
print("total hook-ish lines in tail:", hits)
