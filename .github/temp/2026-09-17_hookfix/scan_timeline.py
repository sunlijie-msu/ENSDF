"""Timeline: when did guard_ens_edit stop firing? Last 40 events + last guard/verify events."""
import json
import re

P = (r"C:\Users\sun\AppData\Roaming\Code\User\workspaceStorage"
     r"\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\debug-logs"
     r"\871d2455-0101-4b6a-a2d6-afd68693d02b\main.jsonl")

events = []
with open(P, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if '"type":"hook"' in line:
            events.append((i, line))

def parse(line):
    try:
        rec = json.loads(line)
    except Exception:
        return None
    attrs = rec.get("attrs", {})
    inp = attrs.get("input", "")
    tool = re.search(r'"tool_name":"([^"]+)"', inp)
    return {
        "ts": rec.get("ts"), "name": rec.get("name"), "status": rec.get("status"),
        "cmd": (attrs.get("command", "") or "")[:55],
        "tool": tool.group(1) if tool else "",
        "inp": inp,
    }

print("=== last 24 events ===")
for i, line in events[-24:]:
    r = parse(line)
    if r:
        print(f"{r['ts']} {r['name']:11s} {r['status']:5s} {r['cmd']:45s} tool={r['tool']}")

print("\n=== last guard_ens_edit events ===")
guard_events = [(i, parse(line)) for i, line in events if "guard_ens_edit" in line]
for i, r in guard_events[-6:]:
    if r:
        print(f"line {i} {r['ts']} {r['name']} status={r['status']} tool={r['tool']}")

print("\n=== last verify_ens_edit events ===")
ver_events = [(i, parse(line)) for i, line in events if "verify_ens_edit" in line]
for i, r in ver_events[-6:]:
    if r:
        print(f"line {i} {r['ts']} {r['name']} status={r['status']} tool={r['tool']}")
