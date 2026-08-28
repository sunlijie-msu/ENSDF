# Test the improved block-root-file-creation parser
import importlib.util
import os

spec = importlib.util.spec_from_file_location(
    "hook", os.path.join(os.path.dirname(__file__), "..", "..", "hooks", "scripts", "block-root-file-creation.py")
)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

tests = [
    # (command, expected_targets_description)
    ('python tool.py file.ens 2>&1 | Select-String x | Select-Object -First 5', "no targets (stream merge + pipeline)"),
    ('python tool.py file.ens 2>&1', "no targets (stream merge)"),
    ('python tool.py file.ens 1>&2', "no targets (stream merge)"),
    ('cmd > output.txt', "output.txt (file redirect)"),
    ('cmd 2> err.txt', "err.txt (stderr file redirect)"),
    ('cmd >output.txt', "output.txt (no-space file redirect)"),
    ('cmd *> all.txt', "all.txt (all-streams file redirect)"),
    ('New-Item root.txt', "root.txt (write command)"),
    ('echo hi | Out-File test.txt', "test.txt (Out-File)"),
    ('cmd >', "EMPTY target (ambiguous, must deny)"),
    ('echo "2>&1"', "no targets (quoted literal preserved)"),
    ('python -c "print(1)" > log.txt', "log.txt (file redirect after -c)"),
]

print("=" * 70)
for cmd, expected in tests:
    targets = hook.extract_terminal_targets(cmd)
    shown = ", ".join(f"{p!r}:{op}" for p, op in targets) if targets else "(none)"
    print(f"CMD : {cmd}")
    print(f"  -> {shown}")
    print(f"  expected: {expected}")
    print("-" * 70)
