import re

TMP = r"d:\X\ND\ENSDF\.github\temp\quoted_check"
out = open(TMP + r"\errors_clean.txt", encoding="utf-8").read()
targets = {237, 361, 421, 427, 443, 483, 542, 571, 863, 1784, 1785}
for m in re.finditer(r"#(\d+) \[(\w+)\]  line (\d+)\n(.*)\n(.*)", out):
    n = int(m.group(3))
    if n in targets:
        print(f"#{m.group(1)} {m.group(2)} line{n}: {m.group(4).strip()} | {m.group(5).strip()}")
print("---- total", len(re.findall(r"\[(\w+)\]  line", out)))
print("---- block starts present:")
print(sorted(set(int(x) for x in re.findall(r"\]  line (\d+)", out))))
