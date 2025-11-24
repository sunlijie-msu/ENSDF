# Nuclear Physics Angular Momentum Coupling Guide

This document provides the theoretical background and practical usage guide for the `angular_momentum_coupling.py` utility. This tool calculates allowed final nuclear states based on quantum mechanical selection rules.

## 1. Theoretical Basis

The code implements the **Channel Spin Coupling Scheme**, which is a standard method for determining angular momentum conservation in nuclear reactions.

### Conservation Laws
In any nuclear reaction **Target** + **Particle** → **Final_State**, the following quantities are conserved:

1.  **Total Angular Momentum (J)**:
    **J**_final = **J**_target + **s**_particle + **ℓ**

2.  **Parity (π)**:
    π_final = π_target × π_particle × (-1)^ℓ

Where:
*   **J**_target: Spin of the target nucleus.
*   **s**_particle: Intrinsic spin of the interacting particle (projectile or transferred cluster).
*   **ℓ**: Relative orbital angular momentum between the target and the particle.

### Coupling Scheme Used in Code
The code performs the vector addition in two steps (Channel Spin representation):

1.  **Calculate Channel Spin (S)**:
    Couples the target spin and particle spin.
    **S** = **J**_target + **s**_particle
    Possible values: |J_target - s_particle| ≤ S ≤ J_target + s_particle

2.  **Calculate Final Spin (J_final)**:
    Couples the channel spin with the orbital angular momentum.
    **J**_final = **S** + **ℓ**
    Possible values: |S - ℓ| ≤ J_final ≤ S + ℓ

---

## 2. Application to Different Reaction Types

To use the code correctly, you must identify the correct "Particle" input based on the reaction mechanism.

### A. Resonance and Capture Reactions
*Examples: (p, γ), (n, γ), (p, p')*

In these reactions, a projectile fuses with the target to form a compound nucleus (resonance).

*   **Target Input**: Spin/Parity of the target nucleus.
*   **Particle Input**: Spin/Parity of the **projectile**.

| Reaction | Projectile | Particle Input |
| :--- | :--- | :--- |
| ⁵⁹Cu(p, γ)⁶⁰Zn | Proton | `1/2+` |
| ¹²C(n, γ)¹³C | Neutron | `1/2+` |
| ¹⁶O(α, γ)²⁰Ne | Alpha | `0+` |

### B. Single-Nucleon Transfer Reactions
*Examples: (d, p), (p, d), (³He, d), (α, t)*

In these reactions, a single nucleon is transferred between the projectile and the target. You must input the properties of the **transferred nucleon**, not the beam.

*   **Target Input**: Spin/Parity of the target nucleus.
*   **Particle Input**: Spin/Parity of the **transferred nucleon** (n or p).

| Reaction Type | Example | Transferred Object | Particle Input |
| :--- | :--- | :--- | :--- |
| Pickup | ¹³C(p, d)¹²C | Neutron | `1/2+` |
| Stripping | ⁴⁰Ca(³He, d)⁴¹Sc | Proton | `1/2+` |

> **Note on j-transfer**: In transfer physics, we often discuss the transferred total angular momentum *j* (where **j** = **ℓ** + **s**). The code lists results by Channel Spin *S*. The set of allowed final Jπ values is identical regardless of the coupling order.

### C. Two-Nucleon Transfer Reactions
*Examples: (p, t), (t, p), (³He, n), (α, d)*

In these reactions, a pair of nucleons is transferred. The total spin of this pair depends on the coupling of the two nucleons.

#### 1. Identical Nucleon Transfer (2n or 2p)
*Reactions: (p, t), (t, p) (2n transfer); (³He, n) (2p transfer)*

For the transfer of two identical nucleons (2n or 2p) in the same shell model orbit, the Pauli Exclusion Principle dictates that they must be in a singlet state (S=0) if they are in a relative s-state (which is the dominant transfer mode).

*   **ENSDF Policy**: For (p, t), (t, p), and (³He, n) reactions, it is standard to assume the transferred pair is in an **anti-parallel spin state (S=0)**.
*   **Particle Input**: `0+`

#### 2. Neutron-Proton Transfer (1n1p)
*Reactions: (α, d), (d, α)*

For the transfer of a neutron-proton pair (a deuteron), the Pauli principle does not restrict the spin to S=0. The deuteron itself has spin S=1.

*   **Spin Configurations**: Both singlet (S=0) and triplet (S=1) transfers are possible.
*   **Particle Input**:
    *   If assuming singlet transfer: `0+`
    *   If assuming triplet transfer (e.g., deuteron-like): `1+`
    *   *Note: Selection rules often require analyzing both possibilities.*

| Transfer Type | Transferred Pair | Spin Assumption | Particle Input |
| :--- | :--- | :--- | :--- |
| **2n / 2p** | Identical | Anti-parallel (S=0) | `0+` |
| **1n1p** | Non-identical | Parallel (S=1) or Anti-parallel (S=0) | `1+` or `0+` |

### D. Cluster Transfer Reactions
*Examples: (⁶Li, d), (⁷Li, t)*

An alpha particle (or other cluster) is transferred.

*   **Target Input**: Spin/Parity of the target nucleus.
*   **Particle Input**: Spin/Parity of the **transferred cluster**.

| Reaction | Transferred Cluster | Particle Input |
| :--- | :--- | :--- |
| (⁶Li, d) | Alpha (⁴He) | `0+` |

---

## 3. Interpreting the Output

When you run the code:
```bash
python angular_momentum_coupling.py 3/2- 1/2+
```

You receive output like:
```text
L   Wave  Parity   s     Final Jπ
0   s     -        1     1-
0   s     -        2     2-
```

*   **L (Wave)**: The orbital angular momentum of the incoming/transferred particle.
    *   $L=0$ (s-wave), $L=1$ (p-wave), etc.
*   **Parity**: The parity of the final state, determined by $\pi_f = \pi_i \pi_p (-1)^L$.
*   **s (Channel Spin)**: The intermediate coupling of Target + Particle.
    *   For a $3/2^-$ target and $1/2^+$ particle, spins can align ($3/2+1/2=2$) or anti-align ($3/2-1/2=1$).
*   **Final Jπ**: The allowed total angular momentum and parity of the final state.

### Example Analysis: ⁵⁹Cu(p, γ)⁶⁰Zn
*   **Target**: ⁵⁹Cu (3/2-)
*   **Particle**: Proton (1/2+)
*   **Result**:
    *   If capture occurs via **s-wave** (L=0):
        *   Channel spins S=1, 2.
        *   Final states Jπ = 1-, 2-.
    *   If capture occurs via **p-wave** (L=1):
        *   Parity flips (- to +).
        *   Final states include 0+, 1+, 2+, 3+.
