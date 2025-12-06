# Nuclear Physics Angular Momentum Coupling Guide

This document provides the theoretical background and practical usage guide for the `angular_momentum_coupling.py` utility. This tool calculates allowed final nuclear states based on quantum mechanical selection rules.

## 1. Theoretical Basis

The code implements the **Channel Spin Coupling Scheme**, which is a standard method for determining angular momentum conservation in nuclear reactions.

### Conservation Laws
In any nuclear reaction $Target + Particle \to Final\_State$, the following quantities are conserved:

1.  **Total Angular Momentum** ($\vec{J}$):

    $$\vec{J}_{final} = \vec{J}_{target} + \vec{s}_{particle} + \vec{\ell}$$

2.  **Parity** ($\pi$):

    $$\pi_{final} = \pi_{target} \times \pi_{particle} \times (-1)^{\ell}$$

Where:
*   $\vec{J}_{target}$: Spin of the target nucleus.
*   $\vec{s}_{particle}$: Intrinsic spin of the interacting particle (projectile or transferred cluster).
*   $\vec{\ell}$: Relative orbital angular momentum between the target and the particle.

### Coupling Scheme Used in Code
The code performs the vector addition in two steps (Channel Spin representation):

1.  **Calculate Channel Spin** ($\vec{S}$): Couples the target spin and particle spin.

    $$\vec{S} = \vec{J}_{target} + \vec{s}_{particle}$$

    Possible values: $|J_{target} - s_{particle}| \le S \le J_{target} + s_{particle}$

2.  **Calculate Final Spin** ($\vec{J}_{final}$): Couples the channel spin with the orbital angular momentum.

    $$\vec{J}_{final} = \vec{S} + \vec{\ell}$$

    Possible values: $|S - \ell| \le J_{final} \le S + \ell$

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
| $^{59}\text{Cu}(p, \gamma)^{60}\text{Zn}$ | Proton | `1/2+` |
| $^{12}\text{C}(n, \gamma)^{13}\text{C}$ | Neutron | `1/2+` |
| $^{16}\text{O}(\alpha, \gamma)^{20}\text{Ne}$ | Alpha | `0+` |

### B. Single-Nucleon Transfer Reactions
*Examples:* $(d, p)$, $(p, d)$, $(^3\text{He}, d)$, $(\alpha, t)$

In these reactions, a single nucleon is transferred between the projectile and the target. You must input the properties of the **transferred nucleon**, not the beam.

*   **Target Input**: Spin/Parity of the target nucleus.
*   **Particle Input**: Spin/Parity of the **transferred nucleon** ($n$ or $p$).

| Reaction Type | Example | Transferred Object | Particle Input |
| :--- | :--- | :--- | :--- |
| Pickup | $^{13}\text{C}(p, d)^{12}\text{C}$ | Neutron | `1/2+` |
| Stripping | $^{40}\text{Ca}(^3\text{He}, d)^{41}\text{Sc}$ | Proton | `1/2+` |

> **Note on j-transfer**: In transfer physics, we often discuss the transferred total angular momentum *j* (where $\vec{j} = \vec{\ell} + \vec{s}$). The code lists results by Channel Spin *S*. The set of allowed final $J^\pi$ values is identical regardless of the coupling order.

### C. Two-Nucleon Transfer Reactions
*Examples:* $(p, t)$, $(t, p)$, $(^3\text{He}, n)$, $(\alpha, d)$

In these reactions, a pair of nucleons is transferred. The total spin of this pair depends on the coupling of the two nucleons.

#### 1. Identical Nucleon Transfer (2n or 2p)
*Reactions:* $(p, t)$, $(t, p)$ (2n transfer); $(^3\text{He}, n)$ (2p transfer)

For the transfer of two identical nucleons (2n or 2p) in the same shell model orbit, the **Pauli Exclusion Principle** dictates that their total wavefunction must be antisymmetric.
*   If they are in a relative s-state (spatially symmetric, $L=0$), their **spin wavefunction must be antisymmetric**.
*   An antisymmetric spin state for two fermions corresponds to a **Singlet State** ($S=0$).

*   **ENSDF Policy**: For $(p, t)$, $(t, p)$, and $(^3\text{He}, n)$ reactions, it is standard to assume the transferred pair is in an **anti-parallel spin state** ($S=0$).
*   **Particle Input**: `0+`

#### 2. Neutron-Proton Transfer (1n1p)
*Reactions:* $(\alpha, d)$, $(d, \alpha)$, $(^3\text{He}, p)$, $(p, ^3\text{He})$

For the transfer of a neutron-proton pair (a deuteron), the Pauli principle does not restrict the spin to $S=0$. The deuteron itself has spin $S=1$.

*   **Spin Configurations**: Both singlet ($S=0$) and triplet ($S=1$) transfers are possible.
*   **Particle Input**:
    *   If assuming singlet transfer: `0+`
    *   If assuming triplet transfer (e.g., deuteron-like): `1+`
    *   *Note: Selection rules often require analyzing both possibilities.*

| Transfer Type | Transferred Pair | Spin Assumption | Particle Input |
| :--- | :--- | :--- | :--- |
| **2n / 2p** | Identical | Anti-parallel ($S=0$) | `0+` |
| **1n1p** | Non-identical | Parallel ($S=1$) or Anti-parallel ($S=0$) | `1+` or `0+` |

### D. Cluster Transfer Reactions
*Examples:* $(^6\text{Li}, d)$, $(^7\text{Li}, t)$

An alpha particle (or other cluster) is transferred.

*   **Target Input**: Spin/Parity of the target nucleus.
*   **Particle Input**: Spin/Parity of the **transferred cluster**.

| Reaction | Transferred Cluster | Particle Input |
| :--- | :--- | :--- |
| $(^6\text{Li}, d)$ | Alpha ($^4\text{He}$) | `0+` |

### E. Alpha Inelastic Scattering
*Examples:* $(\alpha, \alpha')$

In inelastic scattering, the target nucleus is excited to a higher energy state.

*   **$(\alpha, \alpha')$**: The alpha particle has spin 0. Since the projectile spin cannot flip, the angular momentum transfer is purely orbital ($\vec{\ell}$). This selectively excites **Natural Parity** states ($\pi = (-1)^\ell$).

*   **Particle Input**: `0+`
    *   *Note: This treats the angular momentum transfer as a spin-0 boson transfer.*

---

## 3. Interpreting the Output

When you run the code:
```bash
python .github/scripts/angular_momentum_coupling.py 3/2- 1/2+
```

You receive output like:
```text
L   Wave  Parity   s     Final Jπ
0   s     -        1     1-
0   s     -        2     2-
```

*   **L (Wave)**: The orbital angular momentum of the incoming/transferred particle.
    *   $L=0$ (s-wave), $L=1$ (p-wave), etc.
*   **Parity**: The parity of the final state, determined by $\pi_{final} = \pi_{target} \times \pi_{particle} \times (-1)^\ell$.
*   **s (Channel Spin)**: The intermediate coupling of Target + Particle.
    *   For a $3/2^-$ target and $1/2^+$ particle, spins can align ($3/2+1/2=2$) or anti-align ($3/2-1/2=1$).
*   **Final Jπ**: The allowed total angular momentum and parity of the final state.

### Example Analysis: $^{59}\text{Cu}(p, \gamma)^{60}\text{Zn}$
*   **Target**: $^{59}\text{Cu}$ ($3/2^-$)
*   **Particle**: Proton ($1/2^+$)
*   **Result**:
    *   If capture occurs via **s-wave** ($L=0$):
        *   Channel spins $S=1, 2$.
        *   Final states $J^\pi = 1^-, 2^-$.
    *   If capture occurs via **p-wave** ($L=1$):
        *   Parity flips ($-$ to $+$).
        *   Final states include $0^+, 1^+, 2^+, 3^+$.
