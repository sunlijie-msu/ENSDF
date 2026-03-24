### **Normalization Multipliers Table**

| Multiplier | Full Name | Application | Local Normalization (To Branch Level) | Global Normalization (To Parent Level) | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NR** | Photon Multiplier | Relative Photons (**RI**) | Photons per 100 branch decays | $RI \times (NR \times BR)$ |, |
| **NT** | Transition Multiplier | Relative Transitions (**TI**) | Transitions per 100 branch decays | $TI \times (NT \times BR)$ |, |
| **NB** | Beta/EC Multiplier | Rel. Beta/EC (**IB/IE**) | Intensity per 100 branch decays | $IB \times (NB \times BR)$ |, |
| **BR** | Branching Ratio | **N/A** (Bridge) | Bridge from Branch $\rightarrow$ Parent | Multiplies NR, NT, and NB | |
| **NP** | Delayed Particle Multiplier | Delayed Transitions | **N/A** (Direct Step) | Intensity per 100 decays of precursor |, |

---

### **Absolute Intensity Formulas**

The following formulas calculate the **absolute intensity** (per 100 decays of the parent/precursor nuclide):

1.  **Absolute Photon Intensity ($I_\gamma$):**
    $$I_\gamma (\text{abs}) = RI \times (NR \times BR)$$
    *(Note: $NR \times BR$ is the combined multiplier found in the P-record.)*

2.  **Absolute Total Transition Intensity ($I_{tot}$):**
    $$I_{tot} (\text{abs}) = TI \times (NT \times BR)$$
    *(Note: This includes conversion electrons; $TI \times NT \times BR$ is Option 3 in the NDS drawing logic.)*

3.  **Absolute Beta/EC Intensity ($I_\beta$ or $I_\epsilon$):**
    $$I_\beta (\text{abs}) = I_\beta (\text{rel}) \times (NB \times BR)$$
    *(Technicality: Since $\beta$ intensities are normally reported as absolute, the convention is $NB = 1/BR$ to ensure the product is 1.)*

4.  **Absolute Delayed Transition Intensity ($I_{delayed}$):**
    $$I_{delayed} (\text{abs}) = I_{delayed} (\text{rel}) \times NP$$
    *(Distinct from others: NP converts directly to per 100 decays of the precursor.)*

---
