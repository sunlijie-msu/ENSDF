from pathlib import Path
import json

p = Path("A34/Cl34/new/Cl34_adopted.ens")
lines = p.read_text(encoding="utf-8").splitlines()

records = []
current_l = None
for i, line in enumerate(lines, start=1):
    if len(line) >= 9 and line[5] == " " and line[6] == " " and line[7] == "L" and line[8] == " ":
        current_l = {
            "line": i,
            "text": line,
            "T": line[39:49],
            "DT": line[49:55],
            "E": line[9:19].strip(),
        }

    if len(line) >= 10 and line[6] == "c" and line[7] == "L" and "T$" in line:
        block = [{"line": i, "text": line.rstrip()}]
        j = i
        while j < len(lines):
            nxt = lines[j]
            # continuation comment lines: 2cL, 3cL, ... have CONT at idx 5, 'c' at idx 6, 'L' at idx 7
            if len(nxt) >= 8 and nxt[5] != " " and nxt[6] == "c" and nxt[7] == "L":
                block.append({"line": j + 1, "text": nxt.rstrip()})
                j += 1
            else:
                break
        records.append({"L": current_l, "block": block})

out = Path(".github/temp/2026-04-27_cl34_t_checks/cl34_t_blocks.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(records, indent=2), encoding="utf-8")

print(f"wrote {len(records)} blocks to {out}")
for k, rec in enumerate(records[:30], start=1):
    l = rec["L"]
    print(
        f"{k:02d}. L{l['line'] if l else 'NA'} E={l['E'] if l else '?'} "
        f"T={l['T'].strip() if l else '?'} DT={l['DT'].strip() if l else '?'} "
        f"cL={rec['block'][0]['line']}"
    )
