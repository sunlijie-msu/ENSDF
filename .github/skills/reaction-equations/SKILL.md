---
name: reaction-equations
description: >
  Use this skill when adding nuclear reaction equation comments to transfer
  reaction dataset headers in ENSDF files. Covers stripping, pickup, charge
  exchange, and fragmentation reactions. Determines net nucleon transfer and
  formats with added nucleons LEFT of arrow and removed nucleons RIGHT of
  arrow. Includes reference table for 40+ common reactions and target ground
  state spin-parity table.
argument-hint: [ENSDF file or reaction type]
---

# Nuclear Reaction Equation Formatting for ENSDF

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

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

| Reaction | Net Transfer |
|----------|--------------|
| (d,p) | +1n |
| (d,n) | +1p |
| (t,d) | +1n |
| (t,p) | +2n |
| (3He,d) | +1p |
| (3He,n) | +2p |
| (3He,p) | +1p+1n |
| (a,t) | +1p |
| (a,3He) | +1n |
| (a,d) | +1p+1n |
| (a,p) | +1p+2n |
| (a,n) | +2p+1n |
| (6Li,d) | +2p+2n |
| (12C,8Be) | +2p+2n |
| (16O,12C) | +2p+2n |
| (7Li,t) | +2p+2n |
| (6Li,a) | +1p+1n |
| (7Li,a) | +1p+2n |
| (9Be,8Be) | +1n |
| (13C,12C) | +1n |
| (18O,16O) | +2n |
| (16O,14C) | +2p |
| (p,g) | +1p |
| (n,g) | +1n |

### Pickup Reactions (remove nucleons)

| Reaction | Net Transfer |
|----------|--------------|
| (p,d) | -1n |
| (p,t) | -2n |
| (p,3He) | -1p-1n |
| (p,a) | -1p-2n |
| (d,t) | -1n |
| (d,3He) | -1p |
| (d,a) | -1p-1n |
| (t,a) | -1p |
| (3He,a) | -1n |
| (n,d) | -1p |
| (n,t) | -1p-1n |
| (n,a) | -2p-1n |
| (g,n) | -1n |
| (g,p) | -1p |
| (g,d) | -1p-1n |
| (g,a) | -2p-2n |
| (d,6Li) | -2p-2n |
| (3He,6He) | -3n |
| (a,6He) | -2n |
| (12C,13C) | -1n |

### Charge Exchange Reactions

| Reaction | Net Transfer |
|----------|--------------|
| (p,n) | +1p-1n |
| (n,p) | +1n-1p |
| (3He,t) | +1p-1n |
| (t,3He) | +1n-1p |
| (6Li,6He) | +1p-1n |

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
| 38Ar | 0+ |
| 39K | 3/2+ |
| 40Ca | 0+ |
