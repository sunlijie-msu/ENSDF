import json, subprocess, sys, tempfile, os

# Test 1: file with Unicode minus in comment line (simulates post-edit state)
tf1 = tempfile.NamedTemporaryFile(mode='w', suffix='.ens', delete=False, encoding='utf-8')
tf1.write('141SM cG $R{-DCO}=0.98 {I1}, POL=+\u22120.33 {I11}.\n')  # Unicode minus in COMMENT
tf1.write('141SM  L 810.6     2  15/2-\n')
tf1.write('141SM  G 634.6     2  1000      E2\n')
tf1.close()

p1 = json.dumps({
    'tool_name': 'replace_string_in_file',
    'tool_input': {'filePath': tf1.name, 'oldString': 'old', 'newString': 'new'},
    'cwd': os.getcwd()
})
r1 = subprocess.run([sys.executable, '.github/hooks/scripts/validate_ens.py'],
                    input=p1, capture_output=True, text=True)
out1 = r1.stdout.strip()
blocked1 = 'decision' in out1 and '"block"' in out1
ascii1 = 'ASCII' in out1
print(f'Test 1 (Unicode minus in comment): blocked={blocked1} ascii={ascii1}')

# Test 2: clean file
tf2 = tempfile.NamedTemporaryFile(mode='w', suffix='.ens', delete=False, encoding='utf-8')
tf2.write('141SM cG $R{-DCO}=0.98 {I1}, POL=+0.33 {I11}.\n')
tf2.write('141SM  L 810.6     2  15/2-\n')
tf2.write('141SM  G 634.6     2  1000      E2\n')
tf2.close()

p2 = json.dumps({
    'tool_name': 'replace_string_in_file',
    'tool_input': {'filePath': tf2.name, 'oldString': 'old', 'newString': 'new'},
    'cwd': os.getcwd()
})
r2 = subprocess.run([sys.executable, '.github/hooks/scripts/validate_ens.py'],
                    input=p2, capture_output=True, text=True)
out2 = r2.stdout.strip()
blocked2 = 'decision' in out2 and '"block"' in out2
ascii2 = 'ASCII' in out2
print(f'Test 2 (clean file): blocked={blocked2} ascii={ascii2}')

os.unlink(tf1.name)
os.unlink(tf2.name)

if ascii1 and not blocked2:
    print('PASS: ASCII catch on comment; clean file passes')
elif ascii1 and blocked2:
    print('PARTIAL: ASCII blocked correctly, clean file also blocked (ruler issue with temp file)')
else:
    print('FAIL')
