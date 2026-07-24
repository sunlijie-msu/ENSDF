"""Generate replacement pairs for remaining S34 levels."""
with open(r'A34\S34\new\S34_32s_t_p.ens', 'r') as f:
    content = f.read()
    lines = content.split('\n')

# Config data for remaining levels (from earlier parse)
configs = {
    0: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=100, (I,I')=100;",
        "(s{-1/2}){+2} (I,I)=13.8, (I,I')=13.0."
    ],
    2128: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=11.8, (I,I')=11.5;",
        "d{-3/2},s{-1/2} (I,I)=1.62, (I,I')=1.52."
    ],
    3308: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=9.12, (I,I')=8.79;",
        "d{-3/2},s{-1/2} (I,I)=1.18, (I,I')=1.12."
    ],
    3915: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=3.62, (I,I')=3.33;",
        "(s{-1/2}){+2} (I,I)=0.48, (I,I')=0.42;",
        "(f{-7/2}){+2} (I,I)=1.75, (I,I')=2.18."
    ],
    4121: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=4.50, (I,I')=4.24;",
        "d{-3/2},s{-1/2} (I,I)=0.59, (I,I')=0.53;",
        "(f{-7/2}){+2} (I,I)=2.25, (I,I')=2.61."
    ],
    4623: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "d{-3/2},f{-7/2} (I,I)=33.8, (I,I')=33.3;",
        "d{-3/2},p{-3/2} (I,I)=2.62, (I,I')=2.67."
    ],
    4690: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(f{-7/2}){+2} (I,I)=2.00, (I,I')=1.88;",
        "d{-3/2},f{-7/2} (I,I)=0.48, (I,I')=0.48."
    ],
    4888: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=3.50, (I,I')=3.30;",
        "(f{-7/2}){+2} (I,I)=1.88, (I,I')=1.88."
    ],
    5225: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(d{-3/2}){+2} (I,I)=5.38, (I,I')=4.85;",
        "(f{-7/2}){+2} (I,I)=3.38, (I,I')=3.64;",
        "(p{-3/2}){+2} (I,I)=0.29, (I,I')=0.28."
    ],
    5679: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "d{-3/2},p{-3/2} (I,I)=3.25, (I,I')=3.18;",
        "d{-3/2},f{-7/2} (I,I)=2.12, (I,I')=2.18."
    ],
    5759: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01): d{-3/2},p{-3/2} (I,I)=9.38, (I,I')=8.18."
    ],
    5859: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01): (f{-7/2}){+2} (I,I)=15.0."
    ],
    6008: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "(f{-7/2}){+2} (I,I)=33.75, (I,I')=33.33;",
        "(p{-3/2}){+2} (I,I)=3.75, (I,I')=3.03."
    ],
    6128: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01): (f{-7/2}){+2} (I,I)=7.75, (I,I')=7.88."
    ],
    6179: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "d{-3/2},p{-3/2} (I,I)=0.22, (I,I')=0.21;",
        "d{-3/2},f{-7/2} (I,I)=3.12, (I,I')=2.73."
    ],
    6349: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01): d{-3/2},p{-3/2} (I,I)=6.38, (I,I')=5.76."
    ],
    7112: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "d{-3/2},f{-7/2} (I,I)=11.25, (I,I')=10.00;",
        "d{-3/2},p{-3/2} (I,I)=0.78, (I,I')=0.67;",
        "(f{-7/2}){+2} (I,I)=6.50, (I,I')=6.67;",
        "(p{-3/2}){+2} (I,I)=0.62, (I,I')=0.55."
    ],
    7245: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "d{-3/2},f{-7/2} (I,I)=22.50, (I,I')=20.61;",
        "d{-3/2},p{-3/2} (I,I)=1.62, (I,I')=1.52."
    ],
    7621: [
        "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):",
        "d{-3/2},f{-7/2} (I,I)=23.75, (I,I')=23.03;",
        "d{-3/2},p{-3/2} (I,I)=1.88, (I,I')=1.61."
    ],
}

# Build replacements: for each level, find its L-record and the next line
# Format: cL prefix + comment text, padded to 80 chars
def fmt_cl(prefix, text):
    """Format a cL comment line to exactly 80 chars."""
    line = f" 34S {prefix} {text}"
    if len(line) > 80:
        line = line[:80]
    else:
        line = line.ljust(80)
    return line

for e_kev in sorted(configs.keys()):
    # Find the L-record line
    e_str = str(e_kev)
    l_idx = None
    for i, line in enumerate(lines):
        if len(line) >= 19 and line[7] == 'L' and line[8] == ' ':
            e_field = line[9:19].strip()
            if e_field == e_str or (e_field and int(float(e_field)) == e_kev):
                l_idx = i
                break
    
    if l_idx is None:
        print(f"NOT FOUND: {e_kev}")
        continue
    
    l_line = lines[l_idx]
    next_line = lines[l_idx + 1] if l_idx + 1 < len(lines) else ''
    
    parts = configs[e_kev]
    
    # Build new cL lines
    cl_lines = []
    for j, part in enumerate(parts):
        if j == 0:
            prefix = "cL"
        else:
            prefix = f"{j+1}cL" if j < 9 else f"{chr(ord('a')+j-9)}cL"
        cl_lines.append(fmt_cl(prefix, part))
    
    old_str = l_line + '\n' + next_line
    new_str = l_line + '\n' + '\n'.join(cl_lines) + '\n' + next_line
    
    print(f"E={e_kev} L={l_idx+1}:")
    print(f"  OLD: [{l_line.rstrip()}] + [{next_line.rstrip()}]")
    print(f"  NEW cL lines: {len(cl_lines)}")
    for cl in cl_lines:
        print(f"    [{cl.rstrip()}]")
    print()
