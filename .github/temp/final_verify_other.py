import re

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'

DATASET_MAP = {
    '1977Da02': 'A',
    '1983Wa27': 'B',
}

MRG_DATASET_MAP = {
    '1977DA02--->A': 'A',
    '1983Wa27--->B': 'B',
}


def parse_float(text):
    try:
        return float(text)
    except ValueError:
        return None


def parse_adp_g(line):
    return {
        'energy': line[9:19].strip(),
        'ri': line[21:29].strip(),
        'dri': line[29:31].strip(),
    }


def parse_other_comment(line):
    match = re.search(
        r'cG RI\$from\s+(1977Da02|1983Wa27)\. Other:\s*([<>]?)(\d+\.?\d*)(?:\s*\{I([^}]*)\})?\s*\((1977Da02|1983Wa27)\)\.',
        line,
    )
    if not match:
        return None

    source_name = match.group(1)
    prefix = match.group(2)
    other_value = match.group(3)
    unc = match.group(4) or ''
    other_name = match.group(5)

    if prefix == '<':
        other_dri = 'LT'
    elif prefix == '>':
        other_dri = 'GT'
    else:
        other_dri = unc.strip()

    return {
        'source_name': source_name,
        'source_letter': DATASET_MAP[source_name],
        'other_name': other_name,
        'other_letter': DATASET_MAP[other_name],
        'quoted_value': other_value,
        'quoted_dri': other_dri,
    }


def format_other(ri, dri, dataset_name):
    if dri == 'LT':
        return f'Other: <{ri} ({dataset_name}).'
    if dri == 'GT':
        return f'Other: >{ri} ({dataset_name}).'
    if dri:
        return f'Other: {ri} {{I{dri}}} ({dataset_name}).'
    return f'Other: {ri} ({dataset_name}).'


def parse_mrg_tokens(line, marker):
    idx = line.find(marker)
    if idx < 0:
        return []
    return line[idx + len(marker):].strip().split()


def parse_mrg_dataset_g(line):
    if len(line) < 70:
        return None
    if line[39:47] != ' 34CL  G':
        return None
    energy = parse_float(line[48:58].strip())
    ri = line[60:68].strip()
    dri = line[68:70].strip()
    if energy is None or not ri:
        return None
    return {
        'energy': energy,
        'ri': ri,
        'dri': dri,
    }


def parse_mrg():
    with open(MRG_FILE, encoding='utf-8') as handle:
        lines = handle.readlines()

    blocks = []
    current_block = None
    current_gamma = None

    for raw in lines:
        line = raw.rstrip('\n')

        if line.startswith(' LEVEL') and '34CL  L' in line:
            if current_block is not None:
                if current_gamma is not None:
                    current_block['gammas'].append(current_gamma)
                blocks.append(current_block)

            tokens = parse_mrg_tokens(line, '34CL  L')
            current_block = {
                'adopted_energy': parse_float(tokens[0]) if tokens else None,
                'level_dataset_energies': {},
                'gammas': [],
            }
            current_gamma = None
            continue

        if current_block is None:
            continue

        if line.startswith(' GAMMA') and '34CL  G' in line:
            if current_gamma is not None:
                current_block['gammas'].append(current_gamma)

            tokens = parse_mrg_tokens(line, '34CL  G')
            current_gamma = {
                'adopted_energy': parse_float(tokens[0]) if tokens else None,
                'dataset_data': {},
            }
            continue

        if line.startswith('-----'):
            if current_gamma is not None:
                current_block['gammas'].append(current_gamma)
                current_gamma = None
            continue

        for tag, letter in MRG_DATASET_MAP.items():
            if tag not in line:
                continue
            if '34CL  L' in line:
                tokens = parse_mrg_tokens(line, '34CL  L')
                if tokens:
                    current_block['level_dataset_energies'][letter] = parse_float(tokens[0])
            elif current_gamma is not None and '34CL  G' in line:
                parsed = parse_mrg_dataset_g(line)
                if parsed is not None:
                    current_gamma['dataset_data'][letter] = parsed
            break

    if current_block is not None:
        if current_gamma is not None:
            current_block['gammas'].append(current_gamma)
        blocks.append(current_block)

    return blocks


def block_distance(block, adp_level_energy):
    candidates = [block['adopted_energy']]
    candidates.extend(block['level_dataset_energies'].values())
    diffs = [abs(candidate - adp_level_energy) for candidate in candidates if candidate is not None]
    return min(diffs) if diffs else 9999.0


def find_matching_block(blocks, adp_level_energy):
    ranked = sorted(blocks, key=lambda block: block_distance(block, adp_level_energy))
    if not ranked:
        return None
    return ranked[0] if block_distance(ranked[0], adp_level_energy) <= 3.0 else None


def gamma_energy_distance(gamma, adp_gamma_energy):
    diffs = []
    if gamma['adopted_energy'] is not None:
        diffs.append(abs(gamma['adopted_energy'] - adp_gamma_energy))
    for dataset_data in gamma['dataset_data'].values():
        if dataset_data.get('energy') is not None:
            diffs.append(abs(dataset_data['energy'] - adp_gamma_energy))
    return min(diffs) if diffs else 9999.0


def find_matching_gamma(block, adp_gamma, source_letter):
    ranked = []
    for gamma in block['gammas']:
        source_data = gamma['dataset_data'].get(source_letter)
        if source_data is None:
            continue

        exact_source_ri = source_data['ri'] == adp_gamma['ri']
        exact_source_dri = source_data['dri'] == adp_gamma['dri']
        distance = gamma_energy_distance(gamma, parse_float(adp_gamma['energy']))

        ranked.append((
            0 if exact_source_ri and exact_source_dri else 1,
            distance,
            gamma,
        ))

    if not ranked:
        return None

    ranked.sort(key=lambda item: (item[0], item[1]))
    best = ranked[0]
    if best[0] == 1 and best[1] > 3.0:
        return None
    return best[2]


def collect_adp_targets(adp_lines):
    targets = []
    current_level_energy = None
    current_gamma = None

    for idx, line in enumerate(adp_lines):
        if '34CL  L' in line:
            current_level_energy = parse_float(line[9:19].strip())
            current_gamma = None
            continue

        if '34CL  G' in line:
            current_gamma = parse_adp_g(line)
            continue

        if 'cG RI$from ' in line and 'Other:' in line and current_level_energy is not None and current_gamma is not None:
            parsed_comment = parse_other_comment(line)
            if parsed_comment is not None:
                targets.append({
                    'line_number': idx + 1,
                    'level_energy': current_level_energy,
                    'gamma': current_gamma,
                    'comment_line': line.rstrip('\n'),
                    'parsed_comment': parsed_comment,
                })

    return targets


def main():
    with open(ADP_FILE, encoding='utf-8') as handle:
        adp_lines = handle.readlines()

    blocks = parse_mrg()
    targets = collect_adp_targets(adp_lines)

    mismatches = []

    for target in targets:
        parsed_comment = target['parsed_comment']
        block = find_matching_block(blocks, target['level_energy'])
        if block is None:
            mismatches.append({
                'line_number': target['line_number'],
                'reason': 'no_block',
                'comment_line': target['comment_line'],
            })
            continue

        gamma = find_matching_gamma(block, target['gamma'], parsed_comment['source_letter'])
        if gamma is None:
            mismatches.append({
                'line_number': target['line_number'],
                'reason': 'no_gamma',
                'comment_line': target['comment_line'],
            })
            continue

        other_data = gamma['dataset_data'].get(parsed_comment['other_letter'])
        if other_data is None:
            mismatches.append({
                'line_number': target['line_number'],
                'reason': 'no_other_dataset_value',
                'comment_line': target['comment_line'],
            })
            continue

        expected_comment = format_other(other_data['ri'], other_data['dri'], parsed_comment['other_name'])
        if expected_comment not in target['comment_line']:
            mismatches.append({
                'line_number': target['line_number'],
                'reason': 'mismatch',
                'comment_line': target['comment_line'],
                'expected_comment': expected_comment,
                'adp_level_energy': target['level_energy'],
                'adp_gamma_energy': target['gamma']['energy'],
                'source_dataset': parsed_comment['source_name'],
            })

    print(f'Checked {len(targets)} cG RI$from ... Other: lines')
    print(f'Mismatches: {len(mismatches)}')
    print()

    for item in mismatches:
        print(f"L{item['line_number']} {item['reason']}")
        if item['reason'] == 'mismatch':
            print(f"  Level: {item['adp_level_energy']}")
            print(f"  Gamma: {item['adp_gamma_energy']}")
            print(f"  Source RI dataset: {item['source_dataset']}")
            print(f"  Current:  {item['comment_line']}")
            print(f"  Expected: {item['expected_comment']}")
        else:
            print(f"  Current:  {item['comment_line']}")
        print()


if __name__ == '__main__':
    main()