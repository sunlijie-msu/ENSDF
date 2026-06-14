import json, subprocess, sys, tempfile, os

# Create temp .ens file with non-ASCII in a COMMENT line
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.ens', delete=False, encoding='utf-8')
tf_path = tf.name
# Write a comment line with Unicode minus
tf.write('141SM cG $R{-DCO}=0.98 {I1}, POL=+0.33 {I11}.\n')  # clean comment
tf.write('141SM  L 810.6     2  15/2-\n')  # clean data record
tf.write('141SM  G 634.6     2  1000      E2\n')  # clean data
tf.close()

# Test 1: comment-only edit (oldString → newString only changes comment line)
p1 = json.dumps({
    'tool_name': 'replace_string_in_file',
    'tool_input': {
        'filePath': tf_path,
        'oldString': '141SM cG $R{-DCO}=0.98 {I1}, POL=+0.33 {I11}.',
        'newString': '141SM cG $R{-DCO}=0.98 {I1}, POL=+\u22120.33 {I11}.'  # Unicode minus!
    },
    'cwd': os.getcwd()
})
r1 = subprocess.run([sys.executable, '.github/hooks/scripts/validate_ens.py'],
                    input=p1, capture_output=True, text=True)
out1 = r1.stdout.strip()
blocked1 = '"decision": "block"' in out1
ascii_blocked1 = 'ASCII' in out1 if blocked1 else False
print(f'Test 1 (comment-only edit with Unicode minus): blocked={blocked1}, ascii={ascii_blocked1}')

# Test 2: clean comment-only edit (no non-ASCII)
p2 = json.dumps({
    'tool_name': 'replace_string_in_file',
    'tool_input': {
        'filePath': tf_path,
        'oldString': '141SM cG $R{-DCO}=0.98 {I1}, POL=+0.33 {I11}.',
        'newString': '141SM cG $R{-DCO}=0.98 {I1}, POL=+0.33 {I11}.  (unchanged but valid)'
    },
    'cwd': os.getcwd()
})
r2 = subprocess.run([sys.executable, '.github/hooks/scripts/validate_ens.py'],
                    input=p2, capture_output=True, text=True)
out2 = r2.stdout.strip()
blocked2 = '"decision": "block"' in out2
ascii_blocked2 = 'ASCII' in out2 if blocked2 else False
print(f'Test 2 (clean comment-only edit): blocked={blocked2}, ascii={ascii_blocked2}')

# Cleanup
os.unlink(tf_path)

if ascii_blocked1 and not blocked2:
    print('PASS: ASCII check catches non-ASCII in comments, clean edit passes')
else:
    print('FAIL')
