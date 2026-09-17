"""Scan the session debug log for hook invocation records (tool names, payload shapes)."""
import re

P = (r"C:\Users\sun\AppData\Roaming\Code\User\workspaceStorage"
     r"\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\debug-logs"
     r"\871d2455-0101-4b6a-a2d6-afd68693d02b\main.jsonl")

pat = re.compile(r"guard_ens|verify_ens")
pat2 = re.compile(r"PreToolUse|PostToolUse|hook")

hits = []
with open(P, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if pat.search(line):
            hits.append((i, "guard/verify", line))

print("lines matching guard_ens/verify_ens:", len(hits))
for i, kind, line in hits[:5]:
    m = pat.search(line)
    s = max(0, m.start() - 300)
    print(f"--- line {i} ---")
    print(line[s:m.start() + 500].replace("\\n", "\n")[:900])

if not hits:
    pat3 = re.compile(r"hookSpecificOutput|permissionDecision")
    n = 0
    with open(P, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if pat3.search(line):
                n += 1
                if n <= 3:
                    m = pat3.search(line)
                    s = max(0, m.start() - 500)
                    print(f"--- perm line {i} ---")
                    print(line[s:m.start() + 500].replace("\\n", "\n")[:1000])
    print("lines matching permissionDecision:", n)
