---
name: ensdf-delayed-particle-record-format
description: "Defines ENSDF delayed-particle (DP-record) 80-column fields and shared DN, DA, DD, and DT formatting. Use when checking or formatting delayed proton or related delayed-particle records."
---

# Delayed Proton Emission Record (DP-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  DP EP       DE IP     DI EI                                              
 35CL  DP 501      10 3.5    12 9022                                            
```

| Field | Columns | Description                                                       |
| :---- | :------ | :---------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`) |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`  |
| SPACE | 7       | Must be blank                                                     |
| RTYPE | 8       | Record type `D` for delayed particle                              |
| PSYM  | 9       | Particle symbol `P` for proton                                    |
| SPACE | 10      | Readability space                                                 |
| EP    | 11–19   | Proton energy in keV                                              |
| DE    | 20–21   | Energy uncertainty                                                |
| SPACE | 22      | Readability space                                                 |
| IP    | 23–29   | Proton intensity in percent                                       |
| DIP   | 30–31   | Uncertainty in IP                                                 |
| SPACE | 32      | Readability space                                                 |
| EI    | 33–39   | Energy of proton-emitting level in keV                            |

## Related Delayed-Particle Records
- Delayed-neutron (DN), delayed-alpha (DA), delayed-deuteron (DD), and delayed-triton (DT) records use the same field layout. Column 8 contains `D`; column 9 contains `N`, `A`, `D`, or `T`, respectively.
