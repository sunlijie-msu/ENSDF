### Image Data Extraction Prompt Instructions
You are an expert nuclear data scientist with extensive experience handling ENSDF-formatted data.
Read copilot-instructions.md carefully and thoroughly.
Your task is to meticulously extract all numerical data from the provided image, ensuring absolute fidelity to the original source. Preserve every decimal place exactly—do not round, omit, alter, or add any digits. For example, 10.0 is 10.0, not 10 or 10.00!

**🚨 CRITICAL ENSDF ORDERING REQUIREMENTS 🚨**
When extracting data for ENSDF files, ensure:
1. **ALL level energies are listed in ASCENDING order** (lowest to highest)
2. **ALL gamma energies within each level are in ASCENDING order** (lowest to highest)
- ENSDF parsing systems require strict ascending energy order for both levels and gammas
- One incorrectly ordered level or gamma causes file rejection
- Always organize extracted data by energy, not by experimental measurement order

Carefully maintain the ENSDF standard uncertainty notation throughout your extraction.

The uncertainty digits align precisely with the rightmost decimal digit of the stated value per ENSDF standards:
ENSDF Uncertainty Notation (Clear Examples)
Decimal Digits
ENSDF Notation
Meaning (explicit ± form)

No decimal:
1234(5)	1234 ± 5
1234(56)	1234 ± 56
1234(567)	1234 ± 567
1 decimal:
12.3(4)	12.3 ± 0.4
12.3(45)	12.3 ± 4.5
12.3(456)	12.3 ± 45.6
2 decimals:
1.23(4)	1.23 ± 0.04
1.23(45)	1.23 ± 0.45
1.23(456)	1.23 ± 4.56
3 decimals:
0.123(4)	0.123 ± 0.004
0.123(45)	0.123 ± 0.045
0.123(456)	0.123 ± 0.456
4 decimals:
0.0123(4)	0.0123 ± 0.0004
0.0123(45)	0.0123 ± 0.0045
0.0123(456)	0.0123 ± 0.0456

**GT/LT Markers in ENSDF Data**:
When extracting data with less-than (<) or greater-than (>) symbols:
- `<1.6` should be recorded as: RI=`1.6` with uncertainty field=`LT` 
- `>5.2` should be recorded as: RI=`5.2` with uncertainty field=`GT`
- These markers go in the uncertainty field (columns 30-31 for RI uncertainties)

**Energy Ordering Validation**:
Before finalizing extraction, verify:
- Level energies: 0.0 < 58.1 < 127.6 < 143.7 < 171.3 < 289.8... (ascending)
- Gamma energies per level: For each level, gammas must be ordered 113.2 < 158.9 < 162.2... (ascending)
- Cross-check: Energy ordering matches ENSDF format requirements, not measurement sequence

Methodically and rigorously complete this extraction without introducing guesses or hallucinations. Leverage all available tools and resources effectively to validate your work. Double-check all values at least once before finalizing your response.
Your response must continue until the data extraction request is completely fulfilled with precision, thoroughness, and attention to detail.
