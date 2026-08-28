# End-to-end simulation: feed hook input JSON to block-root-file-creation.py
# for the exact command that was previously blocked (2>&1 | pipeline), plus a
# genuine root-file-creation command that must still be denied.
import json
import os
import subprocess
import sys

hook = os.path.join(os.path.dirname(__file__), "..", "..", "hooks", "scripts", "block-root-file-creation.py")

def run_hook(command):
    payload = {
        "tool_name": "run_in_terminal",
        "tool_input": {"command": command},
    }
    proc = subprocess.run(
        [sys.executable, hook],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip(), proc.stderr.strip()

# 1) Previously blocked command (2>&1 + pipeline) -> must now be ALLOWED (no denial JSON)
cmd1 = ('python .github/scripts/column_calibrate.py "A34/S34/new/S34_30si_a_g_a_n_resonances.ens" '
        '--fix --dry-run 2>&1 | Select-String -Pattern "Line" | Select-Object -First 15')
out1, err1 = run_hook(cmd1)
print("CASE 1 (previously blocked, should be ALLOWED):")
print("  stdout:", repr(out1) if out1 else "(empty -> allowed)")
print("  stderr:", repr(err1) if err1 else "(empty)")
print("-" * 60)

# 2) Genuine root file creation -> must still be DENIED
cmd2 = 'New-Item -ItemType File -Path test.ens'
out2, err2 = run_hook(cmd2)
denied2 = "permissionDecision" in out2 and '"deny"' in out2
print("CASE 2 (root file creation, should be DENIED):")
print("  denied:", denied2)
print("  stdout snippet:", out2[:200])
print("-" * 60)

# 3) Redirection to a root file -> must still be DENIED
cmd3 = 'python script.py > root_report.txt'
out3, err3 = run_hook(cmd3)
denied3 = "permissionDecision" in out3 and '"deny"' in out3
print("CASE 3 (redirect to root file, should be DENIED):")
print("  denied:", denied3)
print("  stdout snippet:", out3[:200])

ok = (not out1 and not err1) and denied2 and denied3
print("=" * 60)
print("OVERALL:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
