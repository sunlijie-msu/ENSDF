"""Count guard/verify invocations by tool - confirms which tools fire hooks when active."""
import json
import re
from collections import Counter

P = (r"C:\Users\sun\AppData\Roaming\Code\User\workspaceStorage"
     r"\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\debug-logs"
     r"\871d2455-0101-4b6a-a2d6-afd68693d02b\main.jsonl")

counts = Counter()
read_events = []
with open(P, encoding="utf-8", errors="replace") as f:
    for line in f:
        if '"type":"hook"' not in line or '"attrs"' not in line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        cmd = rec.get("attrs", {}).get("command", "")
        if "guard_ens_edit" not in cmd and "verify_ens_edit" not in cmd:
            continue
        tool_m = re.search(r'"tool_name":"([^"]+)"', rec.get("attrs", {}).get("input", ""))
        tool = tool_m.group(1) if tool_m else "?"
        which = "guard" if "guard_" in cmd else "verify"
        counts[(which, tool)] += 1
        if tool in ("read_file", "readFile", "read/readFile"):
            read_events.append((rec.get("ts"), which))

print("=== guard/verify invocations by tool ===")
for k, v in sorted(counts.items()):
    print(f"{k[0]:6s} {k[1]:30s} {v}")

print("\n=== read-tool hook events while active ===")
print("count:", len(read_events))
for ts, which in read_events[-8:]:
    print(f"  {ts} {which}")
