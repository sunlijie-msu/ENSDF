import importlib.util
from pathlib import Path

ROOT = Path(r'd:\X\ND\ENSDF')
VERIFY_PATH = ROOT / '.github' / 'temp' / 'final_verify_other.py'
ADP_PATH = ROOT / 'A34' / 'Cl34' / 'raw' / '1977DA02_1983WA27.adp'
PATCH_PATH = ROOT / '.github' / 'temp' / 'other_fix.patch'


def load_verifier():
    spec = importlib.util.spec_from_file_location('final_verify_other', VERIFY_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    verifier = load_verifier()

    with open(ADP_PATH, encoding='utf-8') as handle:
        adp_lines = handle.readlines()

    blocks = verifier.parse_mrg()
    targets = verifier.collect_adp_targets(adp_lines)

    replacements = []

    for target in targets:
        parsed_comment = target['parsed_comment']
        block = verifier.find_matching_block(blocks, target['level_energy'])
        if block is None:
            continue

        gamma = verifier.find_matching_gamma(block, target['gamma'], parsed_comment['source_letter'])
        if gamma is None:
            continue

        other_data = gamma['dataset_data'].get(parsed_comment['other_letter'])
        if other_data is None:
            continue

        expected_comment = verifier.format_other(other_data['ri'], other_data['dri'], parsed_comment['other_name'])
        current_line = target['comment_line']
        if expected_comment in current_line:
            continue

        new_line = current_line
        start = new_line.find('Other:')
        end = new_line.rfind('.')
        if start < 0 or end < start:
            continue
        new_line = new_line[:start] + expected_comment + new_line[end + 1:]
        new_line = new_line.ljust(len(current_line))

        replacements.append((target['line_number'], current_line, new_line))

    patch_lines = ['*** Begin Patch', f'*** Update File: {ADP_PATH}']
    for line_number, old_line, new_line in replacements:
        patch_lines.append(f'@@')
        if line_number > 1:
            patch_lines.append(adp_lines[line_number - 2].rstrip('\n'))
        patch_lines.append(f'-{old_line}')
        patch_lines.append(f'+{new_line}')
        if line_number < len(adp_lines):
            patch_lines.append(adp_lines[line_number].rstrip('\n'))
    patch_lines.append('*** End Patch')

    with open(PATCH_PATH, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write('\n'.join(patch_lines) + '\n')

    print(f'Wrote patch with {len(replacements)} replacements to {PATCH_PATH}')


if __name__ == '__main__':
    main()