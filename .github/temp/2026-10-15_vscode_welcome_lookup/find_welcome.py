import json
import os
import re

APP = r'c:\Users\sun\AppData\Local\Programs\Microsoft VS Code\6d62b1d5da\resources\app'
EXT_USER = r'c:\Users\sun\.vscode\extensions'
NEEDLE = 'Chat with Copilot'
EXTS = ('.js', '.json', '.md', '.html', '.txt', '.mjs', '.cjs')

msgs = json.load(open(APP + r'\out\nls.messages.json', encoding='utf-8'))
print('--- nls entries matching /Chat with|Welcome to Copilot|Ask Copilot|Copilot harness/i')
for i, s in enumerate(msgs):
    if isinstance(s, str) and re.search(r'Chat with|Welcome to Copilot|Copilot harness|Copilot SDK', s, re.I):
        print(i, repr(s)[:260])

print('--- filesystem search for', NEEDLE)
for base in (APP, EXT_USER):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in ('.git',)]
        for fn in filenames:
            if not fn.lower().endswith(EXTS):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 80_000_000:
                    continue
                t = open(p, encoding='utf-8', errors='ignore').read()
            except OSError:
                continue
            for m in re.finditer(re.escape(NEEDLE), t):
                s = max(0, m.start() - 120)
                print(p.replace(base, '<' + os.path.basename(base) + '>'), m.start(), '|', t[s:m.start() + 160].replace('\n', ' '))
                break
