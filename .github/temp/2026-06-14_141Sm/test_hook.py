import json, subprocess, sys

p = json.dumps({
    'tool_name': 'replace_string_in_file',
    'tool_input': {'filePath': 'XUNDL/2026MAAA_CT11001_141Sm.ens'},
    'cwd': r'D:\X\ND\ENSDF'
})
r = subprocess.run([sys.executable, '.github/hooks/scripts/validate_ens.py'],
                   input=p, capture_output=True, text=True)
print('exit=', r.returncode)
out = r.stdout.strip()
if out:
    j = json.loads(out)
    blocked = j.get('decision') == 'block'
    print('blocked=', blocked)
    if blocked:
        reason = j.get('reason', '')
        if 'ASCII' in reason:
            print('BLOCKED: ASCII violation')
        elif '80-column' in reason:
            print('BLOCKED: 80-column validation')
        else:
            print('BLOCKED: other')
else:
    print('PASS (no block)')
