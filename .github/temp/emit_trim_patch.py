from pathlib import Path

ADP_PATH = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp')
PATCH_PATH = Path(r'd:\X\ND\ENSDF\.github\temp\trim_fix.patch')
TARGETS = [232, 572, 578, 580, 597, 741, 752, 796, 1088, 1094, 1271, 1279, 1369]


def main():
    lines = ADP_PATH.read_text(encoding='utf-8').splitlines()
    patch_lines = ['*** Begin Patch', f'*** Update File: {ADP_PATH}']

    for line_number in TARGETS:
        old_line = lines[line_number - 1]
        new_line = old_line[:80]
        patch_lines.append('@@')
        patch_lines.append(lines[line_number - 2])
        patch_lines.append(f'-{old_line}')
        patch_lines.append(f'+{new_line}')
        if line_number < len(lines):
            patch_lines.append(lines[line_number])

    patch_lines.append('*** End Patch')
    PATCH_PATH.write_text('\n'.join(patch_lines) + '\n', encoding='utf-8', newline='\n')
    print(f'Wrote trim patch to {PATCH_PATH}')


if __name__ == '__main__':
    main()