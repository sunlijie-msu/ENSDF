# Nuclear Physics Angular Momentum Coupling Guide

This document provides the theoretical background and practical usage guide for the `angular_momentum_coupling.py` utility. This tool calculates allowed final nuclear states based on quantum mechanical selection rules.

## 1. Theoretical Basis

The code implements the **Channel Spin Coupling Scheme**, which is a standard method for determining angular momentum conservation in nuclear reactions.

### Notation

| Symbol | Meaning |
|--------|---------|
| $J_{target}$ | Spin of target nucleus (Python target input) |
| $\pi_{target}$ | Parity of target nucleus (Python target input) |
| $s_{particle}$ | Spin of transferred particle (Python particle input) |
| $\pi_{particle}$ | Parity of transferred particle (Python particle input) |
| $T_{particle}$ | Isospin of transferred particle |
| $\ell$ | Relative orbital angular momentum between the target and the particle |
| $S$ | Channel Spin = $J_{target} + s_{particle}$ |
| $J_{final}$ | Spin of the populated final nuclear state |
| $\pi_{final}$ | Parity of the populated final nuclear state |

**Notation discipline:** Use lowercase $s_{particle}$ for the intrinsic spin of the transferred object (single nucleon, nucleon pair, or cluster). Uppercase $S$ is reserved for the channel spin formed by coupling $J_{target}$ with $s_{particle}$. Do not use $S$ to describe the transferred object itself.

### Conservation Laws

In any nuclear reaction $Target + Particle \to Final\_State$, the following quantities are conserved:

1. **Total Angular Momentum** ($\vec{J}$):

   $$\vec{J}_{final} = \vec{J}_{target} + \vec{s}_{particle} + \vec{\ell}$$

2. **Parity** ($\pi$):

   $$\pi_{final} = \pi_{target} \times \pi_{particle} \times (-1)^{\ell}$$

### Coupling Scheme Used in Code

The code performs the vector addition in two steps (Channel Spin representation):

1. **Calculate Channel Spin** ($\vec{S}$): Couples the target spin and particle spin.

   $$\vec{S} = \vec{J}_{target} + \vec{s}_{particle}$$

   Possible values: $|J_{target} - s_{particle}| \le S \le J_{target} + s_{particle}$

2. **Calculate Final Spin** ($\vec{J}_{final}$): Couples the channel spin with the orbital angular momentum.

   $$\vec{J}_{final} = \vec{\ell} + \vec{S}$$

   Possible values: $|\ell - S| \le J_{final} \le \ell + S$

**Important**: The "Particle" input to this tool represents the **intrinsic properties of the transferred particle**: spin $s_{particle}$, parity $\pi_{particle}$, and isospin $T_{particle}$.

## 2. Application to Different Reaction Types

To use the code correctly, you must identify the correct "Particle" input based on the reaction mechanism.

### A. Resonant Capture Reactions

Examples: $(p, \gamma)$, $(n, \gamma)$

In these reactions, a projectile fuses with the target to form a compound nucleus (resonance).

* **Particle Input**: `1/2+`

### B. Single-Nucleon Transfer Reactions

Examples: $(d, p)$, $(p, d)$, $(^3\text{He}, d)$, $(d, ^3\text{He})$, $(n, d)$, $(d, n)$, $(d, t)$, $(t, d)$, $(\alpha, t)$, $(t, \alpha)$, $(^3\text{He}, \alpha)$, $(\alpha, ^3\text{He})$

In these reactions, a single nucleon is transferred between the projectile and the target. You need to input the properties of the **transferred nucleon**.

* **Particle Input**: `1/2+`


### C. Two-Nucleon Transfer Reactions

In these reactions, a pair of nucleons is transferred. The total spin of this pair depends on the coupling of the two nucleons.

#### 1. Identical Nucleon Transfer (2n or 2p)

*Reactions:* $(p, t)$, $(t, p)$ (2n transfer); $(^3\text{He}, n)$ (2p transfer)

For the transfer of two identical nucleons (2n or 2p) in the same shell model orbit, the **Pauli Exclusion Principle** dictates that their total wavefunction must be antisymmetric.

* If they are in a relative s-state (spatially symmetric, $L=0$), their **spin wavefunction must be antisymmetric**.
* An antiparallel spin state for two fermions corresponds to **$s_{particle}=0$** (spin singlet for the transferred pair).
* **NDS Policy**: For $(p, t)$, $(t, p)$, and $(^3\text{He}, n)$ reactions, it is standard to assume the transferred pair is in a relative $s$ state (**$s_{particle}=0$**).
* **Particle Input**: `0+` for transferring $s_{particle}=0, T_{particle}=1$ particle pair

#### 2. Neutron-Proton Transfer (1n1p)

*Reactions:* $(\alpha, d)$, $(d, \alpha)$, $(^3\text{He}, p)$, $(p, ^3\text{He})$

For the transfer of a neutron-proton pair, the selection rules depend on the projectile/ejectile properties.

* **$(\alpha, d)$ and $(d, \alpha)$**:
  * Both $d$ and $\alpha$ have $T=0$. Thus, only **$T=0$** transfer is allowed.
  * Antisymmetry requires $s_{particle}+T$ to be odd (for $L=0$). Since $T=0$, the transferred pair must be spin triplet, i.e., **$s_{particle}=1$**.
  * **Particle Input**: `1+` for transferring $s_{particle}=1, T_{particle}=0$ particle pair

* **$(^3\text{He}, p)$ and $(p, ^3\text{He})$**:
  * Both particles have $s_{particle}=1/2, T_{particle}=1/2$.
  * Allowed transferred-pair components: **$(s_{particle}=0, T_{particle}=1)$** and **$(s_{particle}=1, T_{particle}=0)$**.
  * **Particle Input**:
    * `0+` for transferring $s_{particle}=0, T_{particle}=1$ particle pair
    * `1+` for transferring $s_{particle}=1, T_{particle}=0$ particle pair
  * *Note: Both components can contribute.*

### D. Cluster Transfer Reactions

*Examples:* $(^6\text{Li}, d)$, $(^7\text{Li}, t)$

An alpha particle is transferred.

* **Particle Input**: `0+`

### E. Inelastic Scattering

*Examples:* $(\alpha, \alpha')$, $(p, p')$

* **$(\alpha, \alpha')$**: The alpha particle has spin 0. Since the projectile spin cannot flip, the angular momentum transfer is purely orbital ($\vec{\ell}$). This selectively excites **Natural Parity** resonances ($\pi = (-1)^\ell$) in the compound nucleus.
* **Particle Input**: `0+`

* **$(p, p')$**: The proton ($s=1/2$) can undergo spin-flip. It allows both Isoscalar ($T=0$) and Isovector ($T=1$) transitions.
  * **Particle Input**: `0+` for non spin-flip
  * **Particle Input**: `1+` for spin-flip

### F. Charge Exchange Reactions

*Examples:* $(p, n)$, $(^3\text{He}, t)$, $(^6\text{Li}, ^6\text{He})$

These reactions exchange nucleon type (n ↔ p), governed by the transferred angular momentum ($\Delta L$), spin ($\Delta S$), and total angular momentum ($\Delta J = \Delta L + \Delta S$). Parity change follows $\pi_f = \pi_i (-1)^{\Delta L}$.

#### Transition Types

* **Fermi** ($\Delta L = 0, \Delta S = 0, \Delta J = 0, \Delta T = 0$): The emitted electron and antineutrino (or positron and neutrino) have antiparallel spins, and hence, no spin-flip, no parity change. Excites the Isobaric Analog State with $J_f = J_i$ and $\pi_f = \pi_i$.

* **Gamow-Teller** ($\Delta L = 0, \Delta S = 1, \Delta J = 1, \Delta T = 0, \pm1$): The emitted leptons have parallel spins, and hence, spin-flip. Selection rule: $J_f = J_i, J_i \pm 1$ but except $J_i = 0 \to J_f = 0$. Therefore, from $0^+$ targets, GT transitions selectively populate $1^+$ states. Except $T_i = 0 \to T_f = 0$.

* **Spin-Dipole** ($\Delta L = 1, \Delta S = 1$): Parity change ($\pi_f = -\pi_i$), with $\Delta J = 0, 1, 2$.

#### Particle Input

* **$(^6\text{Li}, ^6\text{He})$**: Pure Gamow-Teller ($1^+$ $^6\text{Li}$ to $0^+$ $^6\text{He}$ projectile).
  * **Particle Input**: `1+`

* **$(p, n)$ and $(^3\text{He}, t)$**: Mixed (Fermi + Gamow-Teller).
  * **Particle Input**: `0+` (Fermi)
  * **Particle Input**: `1+` (Gamow-Teller)


## 3. Interpreting the Output

When you run the code:

```bash
python .github/scripts/angular_momentum_coupling.py
```

then enter prompted values, for example:

```text
Target J^π [3/2-]: 3/2-
Particle s^π [1/2+]: 1/2+
```

You receive output like:

```text
Target: J=3/2 π=- | Particle: s=1/2 π=+
Channel Spins S: 1, 2: from |3/2 - 1/2| to 3/2 + 1/2
----------------------------------------------------------------------
Wave   L    S      Final Jπ
----------------------------------------------------------------------
s      0    1      1-
s      0    2      2-
----------------------------------------------------------------------
p      1    1      0+, 1+, 2+
p      1    2      1+, 2+, 3+
----------------------------------------------------------------------
d      2    1      1-, 2-, 3-
d      2    2      0-, 1-, 2-, 3-, 4-
----------------------------------------------------------------------
```

* **Wave**: The orbital angular momentum ($\ell$) between target and particle, expressed as spectroscopic notation (s, p, d, f, g, h, i for $\ell = 0, 1, 2, 3, 4, 5, 6$).
* **L**: Numeric value of orbital angular momentum ($\ell$).
* **S**: Channel Spin value ($S = \vec{J}_{target} + \vec{s}_{particle}$). For $3/2^-$ target and $1/2^+$ particle: $S$ ranges from $|3/2 - 1/2| = 1$ to $3/2 + 1/2 = 2$.
* **Final Jπ**: All allowed final spin-parity combinations for each $(L, S)$ pair. Values are calculated from $|\ell - S| \le J_{final} \le \ell + S$. Parity is determined by $\pi_{final} = \pi_{target} \times \pi_{particle} \times (-1)^{\ell}$.

### Example Analysis: $^{59}\text{Cu}(p, \gamma)^{60}\text{Zn}$

* **Target**: $^{59}\text{Cu}$ ($3/2^-$)
* **Particle**: Proton ($1/2^+$)
* **Channel Spins**: $S = 1, 2$ (from $|3/2 - 1/2|$ to $3/2 + 1/2$)
* **Results**:
  * **s-wave capture** ($L=0$): Parity = $(-) \times (+) \times (-1)^0 = -$
    * $S=1$: $J^\pi = 1^-$
    * $S=2$: $J^\pi = 2^-$
  * **p-wave capture** ($L=1$): Parity = $(-) \times (+) \times (-1)^1 = +$
    * $S=1$: $J^\pi = 0^+, 1^+, 2^+$ (from $|1-1|$ to $1+1$)
    * $S=2$: $J^\pi = 1^+, 2^+, 3^+$ (from $|2-1|$ to $2+1$)
  * **d-wave capture** ($L=2$): Parity = $-$
    * $S=1$: $J^\pi = 1^-, 2^-, 3^-$
    * $S=2$: $J^\pi = 0^-, 1^-, 2^-, 3^-, 4^-$

## 4. Isospin Coupling

For transfer reactions, isospin ($T$) provides additional selection rules.

* **Single Nucleon Transfer**: Transferring one nucleon ($n$ or $p$) has $T_{particle} = 1/2$.
* **Identical Nucleon Pair (2n/2p)**: In a relative $L=0$ state, the Pauli Principle requires $s_{particle}=0$ (spin singlet for the transferred pair) and $T_{particle}=1$ (isospin triplet).
* **Neutron-Proton Pair (np)**:
  * Deuteron-like ($s_{particle}=1, T_{particle}=0$)
  * Singlet ($s_{particle}=0, T_{particle}=1$)

**Selection Rule**: The final isospin is determined by vector addition:

$$\vec{T}_{final} = \vec{T}_{target} + \vec{T}_{particle}$$

*Note: This tool calculates angular momentum ($J^\pi$) only. Isospin selection rules must be applied separately.*

## 5. Summary of Transferred Particle Properties

| Reaction Mechanism | Common Examples | Physical Process | $s_{particle}$ | $T_{particle}$ |
| :--- | :--- | :--- | :--- | :--- |
| **Radiative Capture** | $(p,\gamma), (n,\gamma)$ | Projectile capture | $1/2$ | $1/2$ |
| | $(\alpha,\gamma)$ | Projectile capture | $0$ | $0$ |
| **Inelastic Scattering** | $(\alpha,\alpha')$ | Excitation (Natural Parity) | $0$ | $0$ |
| | $(p,p')$ | Excitation (non-flip / spin-flip) | $0$ and $1$ | $0$ and $1$ |
| **One Neutron Transfer** | $(d,p), (p,d), (t,d), (d,t), (\alpha,^3\text{He}), (^3\text{He},\alpha)$ | Transfer of $n$ | $1/2$ | $1/2$ |
| **One Proton Transfer** | $(d,n), (n,d), (^3\text{He},d), (d,^3\text{He}), (\alpha,t), (t,\alpha)$ | Transfer of $p$ | $1/2$ | $1/2$ |
| **Two-Nucleon Transfer** | $(p,t), (t,p), (^3\text{He},n)$ | Transfer of $2n$ or $2p$ ($L_{rel}=0$) | $0$ | $1$ |
| | $(\alpha,d), (d,\alpha)$ | Transfer of $np$ (Deuteron-like) | $1$ | $0$ |
| | $(^3\text{He},p), (p,^3\text{He})$ | Transfer of np (Mixed) | $0$ and $1$ | $1$ ($s_{particle}=0$) / $0$ ($s_{particle}=1$) |
| **Cluster Transfer** | $(^6\text{Li},d)$ | Transfer of $\alpha$-cluster | $0$ | $0$ |
| **Charge Exchange** | $(p,n), (n,p)$ | Fermi / GT | $0$ / $1$ | $0$ / $0,1$ |
| | $(^3\text{He},t), (t,^3\text{He})$ | Fermi / GT | $0$ / $1$ | $0$ / $0,1$ |
| | $(^6\text{Li},^6\text{He})$ | Pure GT ($1^+ \to 0^+$) | $1$ | $0,1$ |
