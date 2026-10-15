import json
import re

ROOT = r'c:\Users\sun\AppData\Local\Programs\Microsoft VS Code\6d62b1d5da\resources\app'
msgs = json.load(open(ROOT + r'\out\nls.messages.json', encoding='utf-8'))
print('nls entries', len(msgs))

for i, s in enumerate(msgs):
    if isinstance(s, str) and re.search(r'Chat with Copilot', s):
        print('NLS', i, repr(s)[:300])

for i in (1917, 1919, 1921, 11759, 11760, 11764, 11765, 11766, 11767, 13322):
    print('SET', i, repr(msgs[i])[:350])

js = open(ROOT + r'\out\vs\workbench\workbench.desktop.main.js', encoding='utf-8').read()
for pat, n in (('function _Xn(', 1800), ('xXn=', 300), ('EXn=', 300)):
    for mm in re.finditer(re.escape(pat), js):
        print('##', pat, mm.start())
        print(js[mm.start():mm.start() + n])
