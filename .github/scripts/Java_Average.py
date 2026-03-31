#!/usr/bin/env python3
"""
ENSDF Averaging Tool - Python Command Line Interface
Exact implementation matching AverageTool_22January2025.jar

This tool implements the EXACT same weighted/unweighted averaging algorithm as the Java tool.

ALGORITHM DETAILS (from Java source code):
1. Weighted Average:
   - Variance for asymmetric uncertainties: V = (dxp + dxm)^2/4 + 0.3633802276324186 * (dxp - dxm)^2/4
   - For symmetric uncertainties (dxp = dxm): V = sigma^2 (standard variance)
   - Weight = 1/V
   - Internal uncertainty = sqrt(1/sum(weights))
   - External uncertainty = sqrt(sum(normWeight * (x - mu)^2) / (n-1))
   - Use larger of internal or external uncertainty

2. Unweighted Average:
   - Simple mean of values
   - Internal uncertainty = sqrt(sum(sigma^2))/n
   - External uncertainty = sqrt(sum((x - mean)^2) / (n * (n-1)))
   - Use larger of internal or external uncertainty

3. Decision Threshold (HARDCODED in Java AverageReport.java):
   - THRESHOLD = 3.5 (hardcoded constant, NOT from chi-squared distribution)
   - If chi^2/(n-1) <= 3.5: use WEIGHTED average (value + max(int,ext) unc)
   - If chi^2/(n-1)  > 3.5: use UNWEIGHTED average (BOTH value AND uncertainty)

4. Display Critical Value (for reference only, shown in output as [critical=X]):
   - Java: EnsdfUtil.criticalReducedChi2(N) = chi^2(N, 90%) where N = #data points
   - This is NOT the adoption decision threshold

5. Minimum Uncertainty Rule (findSuggestedAverage):
   - Final uncertainty >= minimum input uncertainty

6. ENSDF Comment {In} Uncertainty Notation:
   - {In} means uncertainty of n in the last decimal place(s) of the preceding value.
   - Rule: unc = int(n) * 10^(-decimal_places_of_value)
   - Examples: 19.7 {I13} -> 19.7 +/- 1.3  (1 decimal -> unc = 13 * 0.1 = 1.3)
               22 {I4}    -> 22 +/- 4       (0 decimals -> unc = 4 * 1 = 4)
               1.23 {I7}  -> 1.23 +/- 0.07  (2 decimals -> unc = 7 * 0.01 = 0.07)
   - Asymmetric: {I+n-m} -> +n -m in last decimal place(s)

Usage:
    # Numeric mode (direct value/uncertainty pairs):
    python Java_Average.py VALUE1 UNC1 VALUE2 UNC2 [VALUE3 UNC3 ...]

    # ENSDF comment mode (parse {In} notation from ENSDF cL T$ comment lines):
    python Java_Average.py --comment "ENSDF comment text with {In} style uncertainties"
    # (pipe multiple continuation lines as one string, concatenated)

Examples:
    python Java_Average.py 280 50 215 70 130 60 120 65
    python Java_Average.py --comment "weighted average of 22 ps {I4} ... and 19.4 ps {I14} ..."
"""

import sys
import math
from typing import List, Tuple, Dict, Any
from scipy import stats

# Magic constant from Java code for asymmetric uncertainty handling
# This is (1 - 4/pi^2) = 1 - 4/9.8696 = 1 - 0.4053 = 0.5947... 
# Wait, let me check: 0.3633802276324186 ≈ 1/e ≈ 0.368 or related to normal distribution
# Actually this appears to be related to the variance of a split-normal distribution
ASYM_VARIANCE_FACTOR = 0.3633802276324186

# Hardcoded adoption threshold from Java AverageReport.java
# if Math.min(chi2, all_chi2) > 3.5 -> label="Unweighted-Average"
# This is NOT a chi-squared distribution critical value.
INCONSISTENCY_THRESHOLD = 3.5


def gauss_variance(lower: float, upper: float) -> float:
    """
    Calculate Gaussian variance for potentially asymmetric uncertainties.
    This matches the Java dataPt.gaussVariance() method.
    
    For symmetric uncertainties (lower == upper): V = sigma^2
    For asymmetric: V = (dxp + dxm)^2/4 + FACTOR * (dxp - dxm)^2/4
    """
    dxp = max(upper, 0.0)
    dxm = max(lower, 0.0)
    
    # From Java: V = Math.pow(dxp + dxm, 2.0D) / 4.0D + 0.3633802276324186D * Math.pow(dxp - dxm, 2.0D) / 4.0D
    V = (dxp + dxm)**2 / 4.0 + ASYM_VARIANCE_FACTOR * (dxp - dxm)**2 / 4.0
    return V


def weighted_average(data: List[Tuple[float, float, float]]) -> Dict[str, Any]:
    """
    Calculate weighted average using Java algorithm.
    
    Args:
        data: List of (value, lower_unc, upper_unc) tuples
              For symmetric uncertainties, lower_unc == upper_unc
    
    Returns dict with:
        value, internal_unc, external_unc, chi_sq, reduced_chi_sq,
        weights, norm_weights
    """
    n = len(data)
    
    # Calculate weights using Gaussian variance
    weights = []
    for v, lower, upper in data:
        V = gauss_variance(lower, upper)
        if V == 0.0:
            w = 0.0
        else:
            w = 1.0 / V
        weights.append(w)
    
    weight_sum = sum(weights)
    
    # Normalized weights
    norm_weights = [w / weight_sum for w in weights]
    
    # Weighted mean (mu_max in Java)
    weighted_mean = sum(nw * d[0] for nw, d in zip(norm_weights, data))
    
    # Internal uncertainty: sqrt(1/sum(1/sigma_lower^2)) and sqrt(1/sum(1/sigma_upper^2))
    wtp = sum(1.0 / d[2]**2 for d in data if d[2] > 0)  # upper uncertainties
    wtm = sum(1.0 / d[1]**2 for d in data if d[1] > 0)  # lower uncertainties
    
    upper_uncert = math.sqrt(1.0 / wtp) if wtp > 0 else 0.0
    lower_uncert = math.sqrt(1.0 / wtm) if wtm > 0 else 0.0
    
    # For symmetric case, both should be equal
    internal_unc = (upper_uncert + lower_uncert) / 2.0
    
    # Chi-squared calculation (matching Java WeightedAveChiSq)
    chi_sq = sum(w * (d[0] - weighted_mean)**2 for w, d in zip(weights, data))
    reduced_chi_sq = chi_sq / (n - 1) if n > 1 else 0.0
    
    # External uncertainty: sqrt(sum(normWeight * (x - mu)^2) / (n-1))
    ext_unc_sq = sum(nw * (d[0] - weighted_mean)**2 for nw, d in zip(norm_weights, data))
    external_unc = math.sqrt(ext_unc_sq / (n - 1)) if n > 1 else 0.0
    
    # Gaussian variance comparison to decide which uncertainty to use
    internal_variance = gauss_variance(lower_uncert, upper_uncert)
    external_variance = external_unc**2
    
    # Use external if external_variance > internal_variance
    if internal_variance < external_variance:
        final_unc = external_unc
        unc_type = "external"
    else:
        final_unc = internal_unc
        unc_type = "internal"
    
    return {
        'value': weighted_mean,
        'internal_unc': internal_unc,
        'internal_lower': lower_uncert,
        'internal_upper': upper_uncert,
        'external_unc': external_unc,
        'final_unc': final_unc,
        'unc_type': unc_type,
        'chi_sq': chi_sq,
        'reduced_chi_sq': reduced_chi_sq,
        'weights': weights,
        'norm_weights': norm_weights
    }


def unweighted_average(data: List[Tuple[float, float, float]]) -> Dict[str, Any]:
    """
    Calculate unweighted (simple) average using Java algorithm.
    
    Returns dict with value and uncertainties.
    """
    values = [d[0] for d in data]
    n = len(data)
    
    # Simple mean
    mean = sum(values) / n
    
    # Deviation array: (mean - x)^2
    deviations = [(mean - v)**2 for v in values]
    
    # External uncertainty: sqrt(sum((mean - x)^2) / (n * (n-1)))
    # From Java: externaluncert = Math.sqrt(externaluncert / n * (n - 1))
    # which is sqrt(sum_deviations / n / (n-1)) = sqrt(sum / (n*(n-1)))
    external_unc = math.sqrt(sum(deviations) / (n * (n - 1))) if n > 1 else 0.0
    
    # Internal uncertainty: sqrt(sum(sigma^2)) / n
    # From Java: internaluncert = Math.sqrt(internaluncert) / n
    # where internaluncert += dataset[i].gaussVariance()
    internal_unc = math.sqrt(sum(gauss_variance(d[1], d[2]) for d in data)) / n
    
    # Use max of internal and external
    final_unc = max(internal_unc, external_unc)
    unc_type = "external" if external_unc > internal_unc else "internal"
    
    return {
        'value': mean,
        'internal_unc': internal_unc,
        'external_unc': external_unc,
        'final_unc': final_unc,
        'unc_type': unc_type,
        'deviations': deviations
    }


def critical_chi_sq_display(n: int) -> float:
    """
    Calculate display-only critical chi-squared value.
    Matches Java EnsdfUtil.criticalReducedChi2(n) called in AverageReport.java.

    Java uses: criticalReducedChi2(aboveLimitIndexesV().size())
    which returns chi^2(N, 90%) where N = number of data points above 2% weight.
    For display as [critical=X] alongside chi^2/(n-1).

    This value is NOT used for the adoption decision.
    The decision uses the hardcoded constant INCONSISTENCY_THRESHOLD = 3.5.

    Args:
        n: number of data points
    Returns:
        chi^2(n, 90%) — e.g. for n=2: chi^2(2, 90%) = 4.605
    """
    return stats.chi2.ppf(0.90, n)


def find_suggested_average(result_unc: float, data: List[Tuple[float, float, float]]) -> float:
    """
    Apply the minimum uncertainty rule from Java findSuggestedAverage.
    
    The result uncertainty must be >= minimum input uncertainty.
    """
    # Find minimum input uncertainty (considering both lower and upper)
    min_unc = float('inf')
    for v, lower, upper in data:
        if lower > 0 and lower < min_unc:
            min_unc = lower
        if upper > 0 and upper < min_unc:
            min_unc = upper
    
    # Apply the rule
    if result_unc < min_unc:
        return min_unc
    return result_unc


def fmt_val_unc(val: float, unc: float, max_decimals: int) -> str:
    """Format value(uncertainty) in ENSDF notation matching Java XDX2SDS."""
    if max_decimals == 0:
        val_str = f"{val:.0f}"
        unc_int = int(round(unc))
    elif max_decimals == 1:
        val_str = f"{val:.1f}"
        unc_int = int(round(unc * 10))
    else:
        val_str = f"{val:.{max_decimals}f}"
        unc_int = int(round(unc * 10**max_decimals))
    return f"{val_str}({unc_int})"


def count_max_decimals(data: List[Tuple[float, float, float]]) -> int:
    """Count maximum decimal places across all input values and uncertainties."""
    max_dec = 0
    for v, lower, upper in data:
        for x in (v, lower, upper):
            s = str(x)
            if '.' in s:
                stripped = s.rstrip('0')
                if '.' in stripped:
                    dec = len(stripped.split('.')[-1])
                else:
                    dec = 0
                max_dec = max(max_dec, dec)
    return max_dec


def decimal_places(s: str) -> int:
    """Return the number of decimal places in a numeric string like '19.7' or '22'."""
    s = s.strip()
    if '.' in s:
        stripped = s.rstrip('0')
        if '.' in stripped:
            return len(stripped.split('.')[-1])
        return 0
    return 0


def parse_ensdf_unc(value_str: str, unc_str: str) -> float:
    """
    Convert ENSDF {In} or {I+n-m} uncertainty to absolute float.

    Rule: the integer n (or m) represents n units in the last decimal place of value_str.
    - {I13} with value '19.7' (1 decimal) -> 13 * 10^-1 = 1.3
    - {I4}  with value '22'   (0 decimals) -> 4  * 10^0  = 4.0
    - {I14} with value '19.4' (1 decimal)  -> 14 * 10^-1 = 1.4
    - {I7}  with value '1.23' (2 decimals) -> 7  * 10^-2 = 0.07

    For asymmetric {I+n-m}: average of upper and lower (symmetric treatment for averaging).
    Returns the uncertainty as a float.
    """
    ndp = decimal_places(value_str)
    scale = 10.0 ** (-ndp)

    unc_str = unc_str.strip()
    if '+' in unc_str and '-' in unc_str:
        # Asymmetric: {I+n-m} — extract both parts
        # Format examples: '+10-11', '+7-9'
        unc_str_clean = unc_str.replace('+', ' +').replace('-', ' -').strip()
        parts = unc_str_clean.split()
        pos_val = abs(float(parts[0]))
        neg_val = abs(float(parts[1]))
        return ((pos_val + neg_val) / 2.0) * scale
    else:
        return float(unc_str) * scale


def parse_comment_data(comment_text: str) -> List[Tuple[float, float, float]]:
    """
    Parse ENSDF cL T$ comment text and extract (value, lower_unc, upper_unc) data points.

    Handles:
    - Half-life units: ps, fs, ns, us, ms, s, m, h, d, y, eV, keV, MeV (case-insensitive)
    - {In} symmetric uncertainty: e.g., '19.7 ps {I13}'  -> 19.7 +/- 1.3
    - {I+n-m} asymmetric uncertainty: e.g., '100 fs {I+18-11}' -> averaged
    - Parenthetical notation: e.g., '22(4)' -> 22 +/- 4  (same {In} rule applies)
    - Converts all values to a common unit (the unit of the FIRST extracted data point).
    - Skips any value that appears BEFORE the phrase "average of" (that value is the result,
      not an input).
    - Stops at "Other:" (those values are not part of the weighted set).

    Returns (data, base_unit, src_max_dec) where:
        data         = list of (value, lower_unc, upper_unc) tuples (symmetric: lower==upper)
        base_unit    = string of unit (e.g. 'ps'), or None
        src_max_dec  = max decimal places from the original string representations
                       (used for output formatting, avoids floating point noise)
    """
    import re

    # Unit conversion table to picoseconds (ps)
    TO_PS = {
        'fs': 1e-3, 'ps': 1.0, 'ns': 1e3, 'us': 1e6, 'ms': 1e9,
        's': 1e12, 'm': 6e13, 'h': 3.6e15, 'd': 8.64e16, 'y': 3.156e19,
        'ev': None, 'kev': None, 'mev': None,
    }
    UNIT_ALIASES = {'μs': 'us', 'µs': 'us'}

    # Strip ENSDF record prefixes: " 34CL cL T$", " 34CL2cL", " 34CL3cL", etc.
    lines = comment_text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = re.sub(
            r'^\s*[0-9]{0,3}[A-Za-z]{1,2}\s*\d?c[Ll]\s*(?:T\$)?\s*',
            '', line, flags=re.IGNORECASE
        )
        stripped = re.sub(
            r'^\s*\d{1,3}\s*[A-Za-z]{1,2}\s+\d?c[Ll]\s*(?:T\$)?\s*',
            '', stripped, flags=re.IGNORECASE
        )
        cleaned_lines.append(stripped)
    text = ' '.join(cleaned_lines)
    text = re.sub(r'\s+', ' ', text).strip()

    # Truncate at "Other:" — values after this are NOT part of the averaging set
    other_match = re.search(r'\bOther\b', text, re.IGNORECASE)
    if other_match:
        text = text[:other_match.start()]

    # Skip the summary value: if "average of" appears, start parsing AFTER it.
    # The summary value is typically written as "result: average of v1 and v2 ..."
    avg_of_match = re.search(r'\baverage\s+of\b', text, re.IGNORECASE)
    if avg_of_match:
        text = text[avg_of_match.end():]

    # Regex components
    NUMBER_RE = r'(?:\d+\.?\d*|\.\d+)'         # non-negative decimals and integers
    UNIT_RE   = r'(?:fs|ps|ns|us|ms|eV|keV|MeV|s|m|h|d|y)\b'
    INC_RE    = r'\{I([^}]+)\}'
    PAREN_RE  = r'\(([^)]+)\)'

    PATTERN = re.compile(
        r'(' + NUMBER_RE + r')'
        r'\s*'
        r'(' + UNIT_RE + r')?'
        r'\s*'
        r'(?:' + INC_RE + r'|' + PAREN_RE + r')',
        re.IGNORECASE
    )

    data = []
    base_unit = None
    src_max_dec = 0

    for m in PATTERN.finditer(text):
        val_str   = m.group(1)
        unit_str  = m.group(2)
        i_unc_str = m.group(3)
        p_unc_str = m.group(4)

        val = float(val_str)

        if i_unc_str is not None:
            unc = parse_ensdf_unc(val_str, i_unc_str)
        elif p_unc_str is not None:
            unc = parse_ensdf_unc(val_str, p_unc_str)
        else:
            continue

        if unc <= 0:
            continue

        # Track max decimal places from original strings (avoid float noise in formatting)
        ndp_val = decimal_places(val_str)
        src_max_dec = max(src_max_dec, ndp_val)

        # Unit handling
        if unit_str is not None:
            u = UNIT_ALIASES.get(unit_str.lower(), unit_str.lower())
        else:
            u = None

        if base_unit is None and u is not None:
            base_unit = u

        # Convert to base_unit if needed
        if base_unit is not None and u is not None and u != base_unit:
            factor_u    = TO_PS.get(u, 1.0)
            factor_base = TO_PS.get(base_unit, 1.0)
            if factor_u is not None and factor_base is not None:
                val = val * factor_u / factor_base
                unc = unc * factor_u / factor_base

        data.append((val, unc, unc))

    return data, base_unit, src_max_dec


def main():
    args = sys.argv[1:]

    # --- ENSDF comment mode ---
    if len(args) >= 2 and args[0] == '--comment':
        comment_text = ' '.join(args[1:])
        data, base_unit, src_max_dec = parse_comment_data(comment_text)
        if len(data) < 2:
            print("Error: --comment mode found fewer than 2 data points in the comment text.")
            print("Parsed data points:")
            for item in data:
                print(f"  {item}")
            sys.exit(1)
        print(f"\nParsed {len(data)} data point(s) from comment"
              + (f" [unit: {base_unit}]" if base_unit else "") + ":")
        for v, lo, hi in data:
            print(f"  value={v:.{src_max_dec}f}, unc={lo:.{src_max_dec}f}"
                  + (f" {base_unit}" if base_unit else ""))
        # Use src_max_dec (from original string representations) for output formatting
        max_dec = src_max_dec

    # --- Numeric mode ---
    elif len(args) >= 4 and len(args) % 2 == 0:
        data = []
        for i in range(0, len(args), 2):
            value = float(args[i])
            unc = float(args[i + 1])
            data.append((value, unc, unc))
        base_unit = None
        max_dec = count_max_decimals(data)

    else:
        print(__doc__)
        print("\nError: provide either:")
        print("  Numeric mode : VALUE1 UNC1 VALUE2 UNC2 ...")
        print("  Comment mode : --comment \"ENSDF comment text\"")
        sys.exit(1)

    n = len(data)

    # Calculate weighted and unweighted averages
    wt_result = weighted_average(data)
    uwt_result = unweighted_average(data)

    # Display critical chi^2: chi^2(N, 90%) — Java EnsdfUtil.criticalReducedChi2(N)
    # DISPLAY ONLY — the adoption DECISION uses hardcoded threshold INCONSISTENCY_THRESHOLD = 3.5
    crit_display = critical_chi_sq_display(n)

    # Unweighted chi^2 for display: sum((x - mean)^2) / (n-1)  [sample variance S^2]
    mean_uwt = uwt_result['value']
    uwt_chi2_display = sum((v - mean_uwt)**2 for v, _, _ in data) / (n - 1) if n > 1 else 0.0

    # Apply minimum-uncertainty rule to weighted internal and external for display
    wt_int_disp = find_suggested_average(wt_result['internal_unc'], data)
    wt_ext_disp = find_suggested_average(wt_result['external_unc'], data)

    # Apply minimum-uncertainty rule to unweighted final uncertainty for display
    uwt_disp = find_suggested_average(uwt_result['final_unc'], data)

    unit_label = f" {base_unit}" if base_unit else ""

    # --- Print output matching Java AverageTool format ---
    print()
    print("------ average T------")
    print("Data points of T record")
    for i, (v, lower, upper) in enumerate(data):
        unc_str = fmt_val_unc(v, lower, max_dec) + unit_label
        nw = wt_result['norm_weights'][i]
        print(f"*   {unc_str:<25} weight={nw * 100:.2f}%")

    print("Averaging results:")

    wt_val_int = fmt_val_unc(wt_result['value'], wt_int_disp, max_dec) + unit_label
    wt_val_ext = fmt_val_unc(wt_result['value'], wt_ext_disp, max_dec) + unit_label
    print(f"           weighted average:      {wt_val_int:<25} (internal)")
    print(f"                                  {wt_val_ext:<25} (external)")
    print(f"                                  chi**2/(n-1)={wt_result['reduced_chi_sq']:.3f}     [critical={crit_display:.3f}]")

    uwt_disp_str = fmt_val_unc(uwt_result['value'], uwt_disp, max_dec) + unit_label
    print(f"         unweighted average:      {uwt_disp_str}")
    print(f"           (of all values)        chi**2/(n-1)={uwt_chi2_display:.3f}     [critical={crit_display:.3f}]")
    print()

    # --- ADOPTION DECISION: hardcoded threshold 3.5 (Java AverageReport.java) ---
    # Java: if Math.min(chi2, all_chi2) > 3.5 -> Unweighted-Average
    chi2_val = wt_result['reduced_chi_sq']

    if chi2_val <= INCONSISTENCY_THRESHOLD:
        label = "Weighted-Average"
        suggested_value = wt_result['value']
        # Java uses max(internal, external) for the weighted adopted uncertainty
        wt_unc_raw = max(wt_result['internal_unc'], wt_result['external_unc'])
        final_unc = find_suggested_average(wt_unc_raw, data)
    else:
        label = "Unweighted-Average"
        suggested_value = uwt_result['value']
        final_unc = find_suggested_average(uwt_result['final_unc'], data)

    adopted_str = fmt_val_unc(suggested_value, final_unc, max_dec) + unit_label
    print(f"   suggested adopted result:      {adopted_str}")
    print(f"    ({label})")
    print()


if __name__ == "__main__":
    main()

