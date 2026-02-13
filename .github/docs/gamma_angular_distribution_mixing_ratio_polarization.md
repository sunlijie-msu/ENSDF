# Gamma Spectroscopy: Angular Distribution, Mixing Ratios, and Polarization

## 1. Gamma-Ray Angular Distribution

Angular distribution measurements exploit spatial anisotropy of gamma radiation emitted from oriented nuclear states to determine nuclear spins ($J$) and mixing ratios ($\delta$) by comparing measured radiation patterns with theoretical models.

### General Formalism

Nuclear states produced in reactions (e.g., fusion-evaporation) are typically aligned with spin vectors perpendicular to the beam axis. Gamma-ray intensity $W(\theta)$ is measured at specific angles. Data are fitted to a Legendre polynomial expansion to extract experimental coefficients:

$$W(\theta)_{exp} = A_0 [1 + a_2^{exp} P_2(\cos \theta) + a_4^{exp} P_4(\cos \theta)]$$

**Notation:**
- **$A_0$:** Isotropic normalization constant
- **$P_k(\cos \theta)$:** Legendre polynomials of order $k$
- **$a_k^{exp}$:** Measured angular distribution coefficients (e.g., $a_2^{exp}$, $a_4^{exp}$)

### Theoretical Framework

**Calculation of Theoretical Coefficients**

Theoretical angular distribution coefficients account for nuclear orientation and transition properties:

$$a_k^{theo}(\delta) = Q_k(\sigma) \cdot B_k(J_i, J_f, L, L', \delta)$$

**Physical Components:**
- **$Q_k(\sigma)$:** Orientation parameters (quantify nuclear alignment quality)
  - Range: $0 \le Q_k \le 1$ (unity for perfect alignment)
  - Depend on substate population distribution width $\sigma$
  - Account for deorientation effects from nuclear recoil, precession, or finite detection solid angle
- **$B_k(J_i, J_f, L, L', \delta)$:** Radiation distribution coefficients
  - Tabulated geometrical factors from angular momentum coupling
  - Depend on initial spin $J_i$, final spin $J_f$, multipolarities $L$, $L'$, and mixing ratio $\delta$

**Input Parameters:**
- **Known/constrained:** $J_i$, $J_f$, $L$, $L'$, $Q_k$ (from calibration or model)
- **Extracted parameter:** Mixing ratio $\delta$ (scanned from $-\infty$ to $+\infty$)

### Experimental Interpretation

- **Dipole transitions ($\Delta J = 1$):** Negative $a_2^{exp}$ values (e.g., $\approx -0.7$ for pure stretched dipole with full alignment)
- **Quadrupole transitions ($\Delta J = 2$):** Positive $a_2^{exp}$ values (e.g., $\approx +0.3$ for pure stretched quadrupole with full alignment)
- **Isotropic emission ($J=0$ or unaligned):** $a_2^{exp} \approx a_4^{exp} \approx 0$

---

## 2. Multipole Mixing Ratio ($\delta$)

Transitions between nuclear states often proceed via a mixture of two multipolarities: $L$ (lower order) and $L' = L+1$ (higher order), such as mixed M1+E2 transitions.

### Definition

The mixing ratio $\delta$ is defined as the ratio of reduced matrix elements of competing multipoles:

$$\delta = \frac{\langle J_f || L' || J_i \rangle}{\langle J_f || L || J_i \rangle}$$

**Properties:**
- **Magnitude:** Related to intensity ratio via $I(L')/I(L) = \delta^2$
- **Sign convention:** Critical for comparison; two major conventions exist:
  - **Rose-Brink:** Common in older literature
  - **Krane-Steffen:** Standard in modern evaluations
  - Signs are typically opposite depending on matrix element phase definitions

### Chi-Squared ($\chi^2$) Metric

$\chi^2$ quantifies the goodness of fit between experimental measurements and theoretical calculations.

**Formula:**

$$\chi^2(\delta) = \sum_{k=2,4} \left( \frac{a_k^{exp} - a_k^{theo}(\delta)}{\Delta a_k^{exp}} \right)^2$$

**Interpretation:**
- **Low $\chi^2$:** Good agreement (theory matches experiment)
- **High $\chi^2$:** Poor agreement (theory contradicts experiment)

### Analysis Workflow

1. **Select spin hypothesis:** Assume specific $J_i \to J_f$ transition
2. **Scan $\delta$:** Vary $\delta$ continuously (often plotted as $x = \arctan\delta$ from -90° to +90°)
3. **Calculate $\chi^2$:** For each $\delta$ step, calculate $a_k^{theo}$ and resulting $\chi^2$
4. **Find minimum:** The $\delta$ value at $\chi^2_{min}$ is the measured mixing ratio
5. **Determine uncertainty:** Range where $\chi^2 \le \chi^2_{min} + 1$ defines $1\sigma$ uncertainty

### $\arctan(\delta)$ Analysis

**Purpose of Transformation**

The mixing ratio $\delta$ ranges from $-\infty$ to $+\infty$. The $\arctan(\delta)$ transformation compresses this infinite range into a finite interval:
- **$\delta$ range:** $(-\infty, +\infty)$
- **$\arctan(\delta)$ range:** (-90°, +90°) or $(-\pi/2, +\pi/2)$

**Axis Interpretation**

The plot sweeps through all possible mixing ratios, from pure lower multipole ($L$) to pure higher multipole ($L+1$).

| $\arctan(\delta)$ | $\delta$ Value | Physical Meaning |
| :--- | :--- | :--- |
| 0° | 0 | Pure lower multipole ($L$), e.g., pure M1 |
| ±45° | ±1 | Equal mixing ($L$ intensity = $L+1$ intensity) |
| ±90° | ±∞ | Pure higher multipole ($L+1$), e.g., pure E2 |

**Data Interpretation**

- **$\chi^2$ plots:** Minimum (lowest $\chi^2$) indicates most likely $\arctan(\delta)$ value. Values below confidence limit (e.g., $\chi^2_{min} + 1$) define uncertainty range. Assumed spin sequences whose minimum $\chi^2$ curve lie above this threshold are statistically rejected as incompatible with the experimental data.
- **Coefficient plots:** Experimental values ($a_k^{exp} \pm \Delta a_k^{exp}$) appear as horizontal bands; theoretical curves ($a_k^{theo}$ vs. $\arctan(\delta)$) are calculated functions. Intersection indicates solution.
The dashed line typically represents the **99.9% (or 0.1%) confidence limit** for rejecting incorrect spin hypotheses.

---

## 3. Linear Polarization ($P$)

Angular distributions determine multipolarities ($L$) but are often insensitive to parity change ($\pi$) of transitions (e.g., distinguishing M1 from E1 or E2 from M2). Linear polarization measurements resolve this ambiguity.

### Physical Principle

Gamma rays from aligned nuclei are linearly polarized. The electric field vector direction depends on electromagnetic character (electric vs. magnetic) of the radiation.

### Measurement Technique

Polarization is measured using Compton polarimeters (often segmented germanium detectors or clover detectors), which exploit Compton scattering probability dependence on incident photon polarization vector.

### Asymmetry ($A$)

Experimental asymmetry is defined as:

$$A = \frac{N_\perp - N_\parallel}{N_\perp + N_\parallel} = Q \cdot P(\theta)$$

**Notation:**
- **$N_\perp$, $N_\parallel$:** Coincidence counts where scattering plane is perpendicular or parallel to reaction plane
- **$Q$:** Polarization sensitivity of detector
- **$P(\theta)$:** Degree of polarization at angle $\theta$ (typically measured at 90°)

### Parity Determination

For measurements at $\theta = 90°$:
- **Electric transitions (E1, E2):** Polarization vector perpendicular to beam-detector plane ($P > 0$)
- **Magnetic transitions (M1, M2):** Polarization vector parallel to beam-detector plane ($P < 0$)

**Conclusion:** Combining $a_2^{exp}$, $a_4^{exp}$ (spin/multipolarity) with $P$ (parity) enables unique $J^\pi$ assignments.

---
