from pathlib import Path
import re

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Unbound.csv')

# Ei precise mapping from adopted + current reaction ENS files.
ei_map = {
    '5576': '5576.9', '5635': '5635.7', '5672': '5672.9', '5763': '5763.2',
    '5785': '5785.5', '5805': '5805.9', '5852': '5852.8', '5896': '5897.2',
    '5940': '5940.8', '6029': '6030.0', '6090': '6088.91', '6136': '6136.2',
    '6141': '6141.7', '6168': '6169.0', '6180': '6181.27', '6206': '6207.1',
    '6228': '6228.5', '6266': '6266.5', '6272': '6273.3', '6322': '6322.3',
    '6369': '6369.8', '6450': '6450.4', '6488': '6488.3', '6547': '6547.8',
    '6576': '6576.1', '6626': '6626.2', '6640': '6640.91', '6724': '6724.2',
    '6738': '6737.9', '6790': '6790.8', '6798': '6798.4', '6829': '6829.8',
    '6842': '6842.7', '6852': '6852.4', '6871': '6871.0', '6887': '6887.9',
    '6901': '6901.7', '6917': '6917.9', '6931': '6931.5', '7058': '7059.0',
    '7080': '7078.92',
}

other_map = {
    '2.18': '2181.10', '2.38': '2375.7', '2.58': '2580.4', '2.61': '2611.05',
    '2.72': '2721.1', '3.13': '3129.13', '3.33': '3334.0', '3.38': '3383.3',
    '3.55': '3545.07', '3.60': '3600.27', '3.63': '3631.8', '3.65': '3646.3',
    '3.66': '3660.0', '3.77': '3773.84', '3.79': '3791.7', '3.94': '3940.1',
    '3.96': '3964.1', '3.98': '3983.5', '4.08': '4076.3', '4.14': '4139.8',
    '4.15': '4147.8', '4.33': '4325.91', '4.35': '4354.3', '4.42': '4417.4',
    '4.45': '4446.6', '4.46': '4461.4', '4.52': '4515.8', '4.606': '4605.8',
    '4.610': '4609.7', '4.64': '4638.9', '4.70': '4695.7', '4.72': '4717.4',
    '4.82': '4824.5', '4.94': '4941.9', '4.96': '4957.3', '5.00': '4995.6',
    '5.17': '5171.6', '5.39': '5386.8', '5.54': '5540.8',
}
# Intentionally unresolved due ambiguity / no source match.
unresolved_tokens = {'4.61', '13.80'}

lines = csv_path.read_text(encoding='ascii').splitlines()
new_lines = []
for idx, line in enumerate(lines):
    if idx < 2:
        new_lines.append(line)
        continue

    parts = line.split(',')
    if len(parts) >= 2 and parts[1] in ei_map:
        parts[1] = ei_map[parts[1]]

    if parts:
        last = parts[-1]
        def repl(match):
            token = match.group(1)
            if token in other_map:
                return other_map[token] + '('
            return token + '('
        last = re.sub(r'(?<!unknown Ef \()\b(\d+(?:\.\d+)?)\(', repl, last)
        parts[-1] = last

    new_lines.append(','.join(parts))

out_path = Path(r'd:\X\ND\ENSDF\.github\temp\1983WA27_Unbound_preview.csv')
out_path.write_text('\n'.join(new_lines) + '\n', encoding='ascii')

print('Preview written:', out_path)
print('Unresolved tokens intentionally unchanged:', sorted(unresolved_tokens))
for token in sorted(unresolved_tokens):
    print(token, 'count=', sum(line.count(token + '(') for line in new_lines))
