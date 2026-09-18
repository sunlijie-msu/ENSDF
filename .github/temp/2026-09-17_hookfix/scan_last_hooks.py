"""Print the LAST hook events from the session log with tool names."""
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

print("total hook event lines:", len(events))
for i, line in events[-10:]:
    try:
        rec = json.loads(line)
    except Exception:
        print(f"line {i}: (unparsable)")
        continue
    attrs = rec.get("attrs", {})
    inp = attrs.get("input", "")
    # extract tool identity from the nested input JSON
    tool = ""
    m = re.search(r'"tool_name":"([^"]+)"', inp)
    if m:
        tool = m.group(1)
    fp = ""
    m2 = re.search(r'"(?:filePath|file_path|command)":"([^"]{0,80})', inp)
    if m2:
        fp = m2.group(1)
    print(f"line {i} ts={rec.get('ts')} {rec.get('name')} status={rec.get('status')} "
          f"cmd={attrs.get('command','')[:60]} tool={tool} arg={fp}")
