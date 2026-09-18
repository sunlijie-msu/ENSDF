"""Strict classification: group hook events by attrs.command and find dropouts."""
import json
import re

P = (r"C:\Users\sun\AppData\Roaming\Code\User\workspaceStorage"
     r"\1d09f37e75fd559520849ccc67488430\GitHub.copilot-chat\debug-logs"
     r"\871d2455-0101-4b6a-a2d6-afd68693d02b\main.jsonl")

events = []
with open(P, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if '"type":"hook"' in line and '"attrs"' in line:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            attrs = rec.get("attrs", {})
            cmd = attrs.get("command", "")
            if not cmd:
                continue
            tool = re.search(r'"tool_name":"([^"]+)"', attrs.get("input", ""))
            events.append({
                "i": i, "ts": rec.get("ts"), "name": rec.get("name"),
                "status": rec.get("status"), "cmd": cmd,
                "tool": tool.group(1) if tool else "?",
            })

print("parsed hook invocations:", len(events))

print("\n=== last event per command ===")
seen = {}
for e in events:
    seen[e["cmd"]] = e
for cmd, e in seen.items():
    print(f"{e['ts']} {e['name']:11s} {e['status']:5s} {cmd} last-tool={e['tool']}")

print("\n=== guard/verify strict invocations, last 12 ===")
strict = [e for e in events if "guard_ens_edit" in e["cmd"] or "verify_ens_edit" in e["cmd"]]
for e in strict[-12:]:
    loc = "guard" if "guard_" in e["cmd"] else "verify"
    print(f"line {e['i']} ts={e['ts']} {loc:6s} {e['name']:11s} status={e['status']:5s} tool={e['tool']}")

print("\n=== events after the LAST guard/verify strict invocation ===")
if strict:
    last_ts = strict[-1]["ts"]
    after = [e for e in events if e["ts"] > last_ts]
    print("count after:", len(after))
    for e in after[:14]:
        print(f"  {e['ts']} {e['name']:11s} {e['cmd']} tool={e['tool']}")
