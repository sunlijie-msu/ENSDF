import subprocess, json, sys

SCRIPT = r".github\hooks\scripts\block-root-file-creation.ps1"
CMD = ["powershell", "-ExecutionPolicy", "Bypass", "-NonInteractive", "-File", SCRIPT]

def run_test(name, tool_name, file_path, cwd, expect_deny):
    hook_input = json.dumps({"cwd": cwd, "hookEventName": "PreToolUse",
                              "tool_name": tool_name, "tool_input": {"filePath": file_path}})
    r = subprocess.run(CMD, input=hook_input, capture_output=True, text=True, timeout=15)
    stdout = r.stdout.strip()
    blocked = False
    if stdout:
        try:
            out = json.loads(stdout)
            decision = out.get("hookSpecificOutput", {}).get("permissionDecision", "")
            blocked = (decision == "deny")
        except:
            pass
    ok = (blocked == expect_deny)
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if not ok:
        print(f"       expected deny={expect_deny}, got deny={blocked}")
        print(f"       stdout: {stdout[:300]}")
    return ok

ROOT = "d:/X/ND/ENSDF"
results = []

# --- Workspace root ---
results.append(run_test("Root: create_file",              "create_file",            f"{ROOT}/new_file.ens",               ROOT, True))
results.append(run_test("Root: edit/createFile",          "edit/createFile",        f"{ROOT}/new_file.ens",               ROOT, True))

# --- A<N> trees: known masses ---
results.append(run_test("A34 root level",                 "create_file",            f"{ROOT}/A34/test.ens",               ROOT, True))
results.append(run_test("A35 element subdir",             "create_file",            f"{ROOT}/A35/Cl35/test.ens",          ROOT, True))
results.append(run_test("A35 new/ subdir",                "create_file",            f"{ROOT}/A35/K35/new/test.ens",       ROOT, True))
results.append(run_test("A36 raw/ subdir",                "create_file",            f"{ROOT}/A36/S36/raw/data.txt",       ROOT, True))
results.append(run_test("A60 deep subdir",                "create_file",            f"{ROOT}/A60/Ni60/new/deep.ens",      ROOT, True))

# --- A<N> trees: future unspecified masses ---
results.append(run_test("A100 (future mass) blocked",     "create_file",            f"{ROOT}/A100/Sn100/new/test.ens",    ROOT, True))
results.append(run_test("A208 (future mass) blocked",     "create_file",            f"{ROOT}/A208/Pb208/new/test.ens",    ROOT, True))
results.append(run_test("A7 (future mass) blocked",       "create_file",            f"{ROOT}/A7/Li7/new/test.ens",        ROOT, True))

# --- XUNDL tree ---
results.append(run_test("XUNDL root level",               "create_file",            f"{ROOT}/XUNDL/test.ens",             ROOT, True))
results.append(run_test("XUNDL subdir",                   "create_file",            f"{ROOT}/XUNDL/sub/file.ens",         ROOT, True))

# --- Allowed locations ---
results.append(run_test("ALLOW: .github/temp/",           "create_file",            f"{ROOT}/.github/temp/script.py",     ROOT, False))
results.append(run_test("ALLOW: .github/hooks/",          "create_file",            f"{ROOT}/.github/hooks/new.json",     ROOT, False))
results.append(run_test("ALLOW: .github/scripts/",        "create_file",            f"{ROOT}/.github/scripts/tool.py",    ROOT, False))
results.append(run_test("ALLOW: edit tool (not create)",  "replace_string_in_file", f"{ROOT}/A35/K35/new/test.ens",       ROOT, False))

# --- Edge cases ---
results.append(run_test("Edge: 'A' only folder (allow)",  "create_file",            f"{ROOT}/A/test.ens",                 ROOT, False))  # 'A' with no digits
results.append(run_test("Edge: 'AXUNDL' folder (allow)",  "create_file",            f"{ROOT}/AXUNDL/test.ens",            ROOT, False))  # not XUNDL

passed = sum(results)
total  = len(results)
print(f"\n{passed}/{total} tests passed")
sys.exit(0 if passed == total else 1)
