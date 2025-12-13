# Nuclear Reaction Equation Formatting for ENSDF

## Purpose

Add reaction equation comments to transfer reaction datasets.

## Applicability

Apply to:
- Transfer reactions (stripping and pickup)
- Charge exchange reactions
- Fragmentation reactions

Do NOT apply to:
- Adopted levels datasets
- Decay datasets (IT, EC, beta)
- Coulomb excitation
- Inelastic scattering

## Format Rules

Particles ADDED to target: LEFT side of arrow.
Particles REMOVED from target: RIGHT side of arrow.

```
Added nucleons:   {+A}Target+Xp+Yn|){+B}Product
Removed nucleons: {+A}Target|)Xp+Yn+{+B}Product
Mixed:            {+A}Target+Xp|)Yn+{+B}Product
```

## Reaction Analysis Reference

### Stripping Reactions (add nucleons)

| Reaction | Incoming | Outgoing | Net Transfer |
|----------|----------|----------|--------------|
| (d,p) | 1p+1n | 1p | +1n |
| (d,n) | 1p+1n | 1n | +1p |
| (t,d) | 1p+2n | 1p+1n | +1n |
| (t,p) | 1p+2n | 1p | +2n |
| (3He,d) | 2p+1n | 1p+1n | +1p |
| (3He,n) | 2p+1n | 1n | +2p |
| (3He,p) | 2p+1n | 1p | +1p+1n |
| (a,t) | 2p+2n | 1p+2n | +1p |
| (a,3He) | 2p+2n | 2p+1n | +1n |
| (a,d) | 2p+2n | 1p+1n | +1p+1n |
| (a,p) | 2p+2n | 1p | +1p+2n |
| (a,n) | 2p+2n | 1n | +2p+1n |
| (6Li,d) | 3p+3n | 1p+1n | +2p+2n |
| (12C,8Be) | 6p+6n | 4p+4n | +2p+2n |
| (16O,12C) | 8p+8n | 6p+6n | +2p+2n |
| (7Li,t) | 3p+4n | 1p+2n | +2p+2n |
| (6Li,a) | 3p+3n | 2p+2n | +1p+1n |
| (7Li,a) | 3p+4n | 2p+2n | +1p+2n |
| (9Be,8Be) | 4p+5n | 4p+4n | +1n |
| (13C,12C) | 6p+7n | 6p+6n | +1n |
| (18O,16O) | 8p+10n | 8p+8n | +2n |
| (16O,14C) | 8p+8n | 6p+8n | +2p |
| (p,g) | 1p | 0 | +1p |
| (n,g) | 1n | 0 | +1n |

### Pickup Reactions (remove nucleons)

| Reaction | Incoming | Outgoing | Net Transfer |
|----------|----------|----------|--------------|
| (p,d) | 1p | 1p+1n | -1n |
| (p,t) | 1p | 1p+2n | -2n |
| (p,3He) | 1p | 2p+1n | -1p-1n |
| (p,a) | 1p | 2p+2n | -1p-2n |
| (d,t) | 1p+1n | 1p+2n | -1n |
| (d,3He) | 1p+1n | 2p+1n | -1p |
| (d,a) | 1p+1n | 2p+2n | -1p-1n |
| (t,a) | 1p+2n | 2p+2n | -1p |
| (3He,a) | 2p+1n | 2p+2n | -1n |
| (n,d) | 1n | 1p+1n | -1p |
| (n,t) | 1n | 1p+2n | -1p-1n |
| (n,a) | 1n | 2p+2n | -2p-1n |
| (g,n) | 0 | 1n | -1n |
| (g,p) | 0 | 1p | -1p |
| (g,d) | 0 | 1p+1n | -1p-1n |
| (g,a) | 0 | 2p+2n | -2p-2n |
| (d,6Li) | 1p+1n | 3p+3n | -2p-2n |
| (3He,6He) | 2p+1n | 2p+4n | -3n |
| (a,6He) | 2p+2n | 2p+4n | -2n |
| (12C,13C) | 6p+6n | 6p+7n | -1n |

### Charge Exchange Reactions

| Reaction | Incoming | Outgoing | Net Transfer |
|----------|----------|----------|--------------|
| (p,n) | 1p | 1n | +1p-1n |
| (n,p) | 1n | 1p | +1n-1p |
| (3He,t) | 2p+1n | 1p+2n | +1p-1n |
| (t,3He) | 1p+2n | 2p+1n | +1n-1p |
| (6Li,6He) | 3p+3n | 2p+4n | +1p-1n |

## Equation Examples

```
Stripping (+1p+1n):    {+32}S+1p+1n|){+34}Cl
Stripping (+1p):       {+33}S+1p|){+34}Cl
Stripping (+2p+2n):    {+31}P+2p+2n|){+35}Cl
Pickup (-1n):          {+35}Cl|)1n+{+34}Cl
Pickup (-1p):          {+35}Ar|)1p+{+34}Cl
Pickup (-1p-1n):       {+36}Ar|)1p+1n+{+34}Cl
Pickup (-2n):          {+37}Cl|)2n+{+35}Cl
Charge exchange:       {+34}S+1p|)1n+{+34}Cl
Fragmentation:         {+37}Ca|)3p+{+34}Cl
```

## Placement

Insert after compilation credit, before experimental details.

## Target Ground State Spin and Parity

| Target | J pi |
|--------|------|
| 31P | 1/2+ |
| 32S | 0+ |
| 33S | 3/2+ |
| 34S | 0+ |
| 35Cl | 3/2+ |
| 36Ar | 0+ |
| 37Cl | 3/2+ |

## Validation

1. Count incoming particle protons and neutrons
2. Count outgoing particle protons and neutrons
3. Calculate net transfer correctly
4. Place added particles LEFT of arrow
5. Place removed particles RIGHT of arrow
6. Verify target ground state spin and parity
7. Confirm 80 column line length
