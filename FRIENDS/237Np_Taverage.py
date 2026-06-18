import re
import math
from decimal import Decimal

def calculate_and_format_ensdf(data_text, is_lifetime=True):
    """
    Parses ENSDF '{In}' formatted notation, calculates the weighted mean 
    and uncertainties (internal/external), and strictly applies ENSDF 
    Successive Rounding rules (4-up for uncertainty, 5-up for values).
    """
    
    # ---------------------------------------------------------
    # 1. Parse Raw Data and Scale Uncertainties
    # ---------------------------------------------------------
    measurements = []
    for line in data_text.strip().split('\n'):
        if not line.strip():
            continue
            
        # Match pattern: value ns {I<unc>} (ref)
        match = re.search(r"([\d\.]+)\s*ns\s*\{.*?(\d+)\}\s*\((.*?)\)", line)
        if match:
            val_str = match.group(1)
            unc_int = float(match.group(2))
            ref = match.group(3)
            
            # Determine decimal places to properly scale the '{I...}' integer
            dec_places = len(val_str.split('.')[1]) if '.' in val_str else 0
            
            val = float(val_str)
            unc = unc_int * (10 ** -dec_places)
            weight = 1.0 / (unc ** 2)
            
            measurements.append({'ref': ref, 'val': val, 'unc': unc, 'weight': weight})

    # ---------------------------------------------------------
    # 2. Compute Weighted Statistics
    # ---------------------------------------------------------
    sum_w = sum(m['weight'] for m in measurements)
    sum_wx = sum(m['weight'] * m['val'] for m in measurements)
    
    w_mean = sum_wx / sum_w
    int_unc = 1.0 / math.sqrt(sum_w)
    
    # Calculate Reduced Chi-Square and External Uncertainty
    dof = len(measurements) - 1
    chi2 = sum(m['weight'] * (m['val'] - w_mean)**2 for m in measurements)
    reduced_chi2 = chi2 / dof
    
    # Standard physics practice: if chi2/nu > 1, adopt external uncertainty
    ext_unc = int_unc * math.sqrt(reduced_chi2)
    final_unc = ext_unc if reduced_chi2 > 1.0 else int_unc

    # ---------------------------------------------------------
    # 3. Apply ENSDF Successive Rounding Rules
    # ---------------------------------------------------------
    # Convert to 15-decimal strings to avoid floating-point representation artifacts
    val_dec = Decimal(f"{w_mean:.15f}")
    unc_dec = Decimal(f"{final_unc:.15f}")

    # Determine Significant Figures
    unc_sci = f"{unc_dec:e}"
    coeff = unc_sci.split('e')[0].replace('.', '').replace('-', '')
    leading_two = int(coeff[0]) * 10 + (int(coeff[1]) if len(coeff) > 1 else 0)
    exponent = int(unc_sci.split('e')[1])
    
    # Rule: 2 sig figs if 10-34, or if it is a lifetime. Otherwise 1.
    sig_figs = 2 if (10 <= leading_two <= 34 or is_lifetime) else 1
    target_exp = exponent - sig_figs + 1

    def round_successively(num_dec, target, threshold):
        """Recursively rounds digit-by-digit from right to left."""
        curr_exp = num_dec.as_tuple().exponent
        res = num_dec
        
        # If the number lacks precision to reach the target, return as-is
        if curr_exp >= target:
            return res
            
        for e in range(curr_exp, target):
            shift = Decimal('10') ** -(e + 1)
            shifted = res * shift
            discarded = int(abs(shifted - int(shifted)) * 10)
            
            int_part = int(shifted)
            if discarded >= threshold:
                int_part += (1 if num_dec > 0 else -1)
                
            res = Decimal(int_part) / shift
            
        return res

    # ENSDF Rules: Uncertainty rounds 4-up, Value rounds 5-up
    rounded_unc = round_successively(unc_dec, target_exp, threshold=4)
    rounded_val = round_successively(val_dec, target_exp, threshold=5)

    # Format the final extracted fields
    decimals_to_show = -target_exp if target_exp < 0 else 0
    
    val_out = f"{rounded_val:.{decimals_to_show}f}" if decimals_to_show else str(int(rounded_val))
    unc_out = str(int(rounded_unc * (Decimal('10') ** decimals_to_show)))

    # ---------------------------------------------------------
    # 4. Print Summary
    # ---------------------------------------------------------
    print("--- PARSED DATA ---")
    for m in measurements:
        print(f"Ref: {m['ref']:<25} | Val: {m['val']:<8.2f} | Unc: {m['unc']:<6.2f} | W: {m['weight']:.2f}")

    print("\n--- STATISTICAL RESULTS ---")
    print(f"Weighted Mean        : {w_mean:.5f} ns")
    print(f"Internal Uncertainty : {int_unc:.5f} ns")
    print(f"External Uncertainty : {ext_unc:.5f} ns")
    print(f"Reduced Chi-Square   : {reduced_chi2:.4f}")
    
    print("\n--- ENSDF FORMATTED OUTPUT (Lifetime Rule: 2 Sig-Figs) ---")
    print(f"Format for Comment Line : {val_out} ns {{I{unc_out}}}")
    print(f"Format for ENSDF Record : {val_out} PS    {unc_out}")

# =========================================================
# Execution Block
# =========================================================
if __name__ == "__main__":
    raw_data = """
    62 ns {I3} (Vartapetian_AP1958),
    63 ns {I5} (Beling_PR1952),
    63 ns {I5} (Unik_Thesis1960),
    64.2 ns {I20} (Oberhofer_Thesis1968),
    66.7 ns {I7} (Garg_ZP1971),
    66.9 ns {I10} (McBeth_NIM1972),
    67.8 ns {I10} (McBeth_NIM1972),
    68.3 ns {I2} (Miller_NIM1972),
    68.5 ns {I4} (Bishop_NIM1974),
    70 ns {I4} (Finck_NIMA1985),
    67.7 ns {I1} (Vretenar_AJP2019),
    67.60 ns {I25} (Dutsov_ARI2021),
    67.86 ns {I9} (Takacs_ARI2021),
    67.60 ns {I20} (Santos_NPA2023),
    68.03 ns {I7} (Present_work)
    """
    
    calculate_and_format_ensdf(raw_data, is_lifetime=True)