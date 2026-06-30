import pathlib

p = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md")
lines = p.read_text(encoding="utf-8").splitlines()
new_lines = []

NEW_HEADER = "| $E_1$ | $E_{\\gamma1}$ | $E_{\\gamma2}$ | $A_0$ | $A_2$ | $A_4$ | $E_2$ | $E_3$ | $J_1$ | $J_2$ | $J_3$ | $\\delta_1$ |"
NEW_SEP    = "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"

for line in lines:
    s = line.strip()
    # Detect old 10-col header (starts with $E_1$ or $E_i$, has J_1)
    if (s.startswith("| $E_1$") or s.startswith("| $E_i$")) and "$J_1$" in s:
        new_lines.append(NEW_HEADER)
    elif s.startswith("| :---") and ":--- | :--- | :--- |" in s:
        # Only replace the 10-col separator, not the already-fixed 12-col one
        pipes = s.count("|")
        if pipes <= 11:  # 10-col has 11 pipes
            new_lines.append(NEW_SEP)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
print("Fixed. First 5 lines:")
for l in new_lines[:5]:
    print(l)
print("...")
print(f"Total lines: {len(new_lines)}")
