import json

with open('XUNDL/2025LAAA_CH11036_127I_gamma_energies.json', 'r') as f:
    data = json.load(f)

print('2025LAAA Gamma Energies:')
for i, gamma in enumerate(data['gamma_transitions'], 1):
    energy = gamma['energy']['value']
    print(f'{i:2d}. {energy:6.1f} keV')

print(f'Total: {len(data["gamma_transitions"])} gammas')
