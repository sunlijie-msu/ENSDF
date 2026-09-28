import pathlib, subprocess, sys, re
blank = b" " * 80
sample = ["A34/merged.ens", "A34/A34_cover.ens", "A34/Al34/new/Al34_adopted.ens",
          "A34/Cl34/new/Cl34_33s_p_g.ens", "A34/S34/new/S34_adopted.ens",
          "A34/Ar34/new/Ar34_35ca_ecp_decay_25.7_ms.ens", "A34/Si34/new/Si34_adopted.ens",
          "A34/P34/new/P34_adopted.ens", "A34/Mg34/new/Mg34_adopted.ens",
          "A34/Ne34/new/Ne34_adopted.ens"]
for f in sample:
    c = subprocess.run([sys.executable, ".github/scripts/column_calibrate.py", f],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    r = subprocess.run([sys.executable, ".github/scripts/ensdf_1line_ruler.py", "--file", f, "--show-only-wrong"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"Summary: (\d+) data records checked, (\d+) errors found", r.stdout or "")
    fails = sorted(set(x.strip() for x in re.findall(r"\[FAIL\] (.+?)\s*$", c.stdout or "", re.M)))
    b = pathlib.Path(f).read_bytes()
    tail = b.rstrip(b"\r\n").endswith(blank)
    print(f"{f:50s} cal_exit={c.returncode} ruler_err={m.group(2) if m else '?'} tail_blank={tail} FAIL={fails}")
