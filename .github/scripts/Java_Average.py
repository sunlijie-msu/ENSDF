#!/usr/bin/env python3
"""
ENSDF Averaging Tool - Python Command Line Interface
Exact implementation matching AverageTool_22January2025.jar

This tool implements the EXACT same weighted/unweighted averaging algorithm as the Java tool.

ALGORITHM DETAILS (from V.AveLib dataPt.java / averagingMethods.java):
1. Weighted Average:
   - Variance for asymmetric uncertainties (V.AveLib dataPt.gaussVariance()):
       varianceFactor = 1 - 2/pi = 0.3633802276324186
       V = varianceFactor * (upper - lower)^2 + upper * lower
     For symmetric (upper == lower == sigma): V = sigma^2
   - Weight = 1/V
   - WeightedAveChiSq: asymmetric weights — if x > mean: w=1/lower^2; else w=1/upper^2
   - Internal uncertainty (V.AveLib averagingMethods.weightedAverage_legacy):
       lower_int = sqrt(2 / (1 + upperTot/lowerTot) / weightSum)
       upper_int = sqrt(2 / (1 + lowerTot/upperTot) / weightSum)
       Symmetric if |lower_int/upper_int - 1| < 0.01: use sqrt(1/weightSum)
   - External uncertainty = sqrt(WeightedAveChiSq / (weightSum * (n-1)))
   - Use external if its gaussVariance > internal gaussVariance

2. Unweighted Average:
   - Simple mean of values
   - Internal uncertainty = sqrt(sum(V_i))/n where V_i = gaussVariance(dxp, dxm)
   - External uncertainty = sqrt(sum((x - mean)^2) / (n * (n-1)))
   - Use larger of internal or external uncertainty
   - Unweighted chi^2/(n-1) = sum((x_i - mean_u)^2 / V_i) / (n-1)  [normalized by individual variances]

3. Decision Threshold (HARDCODED in Java AverageReport.java):
   - THRESHOLD = 3.5 (hardcoded constant, NOT from chi-squared distribution)
   - If chi^2/(n-1) <= 3.5: use WEIGHTED average (value + max(int,ext) unc)
   - If chi^2/(n-1)  > 3.5: use UNWEIGHTED average (BOTH value AND uncertainty)

4. Display Critical Value (for reference only, shown in output as [critical=X]):
   - Java: EnsdfUtil.criticalReducedChi2(N) = chi^2(N-1, 90%) / (N-1) where N = #data points
   - This is the critical REDUCED chi^2 at 90% confidence (e.g. n=2→2.706, n=3→2.303, n=4→2.084)
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

# varianceFactor = 1 - 2/pi (V.AveLib dataPt.java: private static final double varianceFactor)
# This is the asymmetric Gaussian variance factor for a split-normal distribution.
ASYM_VARIANCE_FACTOR = 1.0 - 2.0 / math.pi  # = 0.3633802276324186

# Hardcoded adoption threshold from Java AverageReport.java
# if Math.min(chi2, all_chi2) > 3.5 -> label="Unweighted-Average"
# This is NOT a chi-squared distribution critical value.
INCONSISTENCY_THRESHOLD = 3.5


def gauss_variance(lower: float, upper: float) -> float:
    """
    Variance of the asymmetric (split-normal) Gaussian.
    Matches V.AveLib dataPt.gaussVariance():
        varianceFactor = 1 - 2/pi
        V = varianceFactor * (upper - lower)^2 + upper * lower
    For symmetric (upper == lower == sigma): V = sigma^2
    """
    dxp = max(upper, 0.0)
    dxm = max(lower, 0.0)
    V = ASYM_VARIANCE_FACTOR * (dxp - dxm)**2 + dxp * dxm
    return V


def weighted_ave_chi_sq(data: List[Tuple[float, float, float]], mean: float) -> float:
    """
    Chi-square using asymmetric weights, matching V.AveLib averagingMethods.WeightedAveChiSq().
    If x_i > mean: weight = 1/lower_i^2 (left half-width faces the mean).
    If x_i <= mean: weight = 1/upper_i^2 (right half-width faces the mean).
    For symmetric inputs (lower == upper == sigma): reduces to sum((x-mean)^2/sigma^2).
    """
    result = 0.0
    for v, lower, upper in data:
        if v > mean:
            w = 1.0 / lower**2 if lower > 0 else 0.0
        else:
            w = 1.0 / upper**2 if upper > 0 else 0.0
        result += w * (v - mean)**2
    return result


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
    
    # Calculate weights using Gaussian variance (1/V_i)
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
    
    # Weighted mean
    weighted_mean = sum(nw * d[0] for nw, d in zip(norm_weights, data))
    
    # Internal uncertainty (V.AveLib averagingMethods.weightedAverage_legacy):
    #   lower_int = sqrt(2 / (1 + upperTot/lowerTot) / weightSum)
    #   upper_int = sqrt(2 / (1 + lowerTot/upperTot) / weightSum)
    #   Symmetric fallback: sqrt(1/weightSum) when |lower/upper - 1| < 0.01
    lower_tot = sum(d[1]**2 for d in data)  # sum of lower^2
    upper_tot = sum(d[2]**2 for d in data)  # sum of upper^2
    sym_int_unc = math.sqrt(1.0 / weight_sum) if weight_sum > 0 else 0.0
    if lower_tot > 0 and upper_tot > 0:
        lower_uncert = math.sqrt(2.0 / (1.0 + upper_tot / lower_tot) / weight_sum)
        upper_uncert = math.sqrt(2.0 / (1.0 + lower_tot / upper_tot) / weight_sum)
        if abs(lower_uncert / upper_uncert - 1.0) < 0.01:
            lower_uncert = upper_uncert = sym_int_unc
    else:
        lower_uncert = upper_uncert = sym_int_unc
    internal_unc = (upper_uncert + lower_uncert) / 2.0
    
    # Chi-square: asymmetric weights (V.AveLib WeightedAveChiSq)
    chi_sq = weighted_ave_chi_sq(data, weighted_mean)
    reduced_chi_sq = chi_sq / (n - 1) if n > 1 else 0.0
    
    # External uncertainty: sqrt(WeightedAveChiSq / (weightSum * (n-1)))
    external_unc = math.sqrt(chi_sq / (weight_sum * (n - 1))) if (n > 1 and weight_sum > 0) else 0.0
    
    # Use external if gaussVariance(external) > gaussVariance(internal result)
    # For symmetric result: gaussVariance = unc^2, so compare squares
    internal_variance = gauss_variance(lower_uncert, upper_uncert)
    external_variance = external_unc**2
    
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
    Calculate display-only critical REDUCED chi-squared value.
    Matches Java EnsdfUtil.criticalReducedChi2(n) called in AverageReport.java.

    Java uses: criticalReducedChi2(aboveLimitIndexesV().size())
    which takes N = number of data points ABOVE weight limit (nAboveLimit),
    and returns chi^2(N, 90%) / (N-1).

    CRITICAL: the chi^2 distribution dof = N (NOT N-1).

    Displayed as [critical=X] alongside chi^2/(n-1) for reference.
    This value is NOT used for the adoption decision.
    The decision uses the hardcoded constant INCONSISTENCY_THRESHOLD = 3.5.

    Examples:
        n=2: chi^2(2, 90%) / 1 = 4.605
        n=3: chi^2(3, 90%) / 2 = 3.0
        n=4: chi^2(4, 90%) / 3 = 2.472

    Args:
        n: number of data points (>= 2)
    Returns:
        critical reduced chi^2 at 90%, i.e., chi^2(n-1, 90%) / (n-1)
    """
    if n <= 1:
        return 0.0
    # Java: chi^2(n, 90%) / (n-1) — dof for ppf = n, NOT n-1
    return stats.chi2.ppf(0.90, n) / (n - 1)


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


def _decimal_places_from_value(value: float) -> int:
    """Return decimal places visible in Decimal(str(value))."""
    from decimal import Decimal

    exponent = Decimal(str(value)).as_tuple().exponent
    return max(0, -exponent)


def _successive_round(value: float, tgt_decimals: int, threshold: int, min_src_decimals: int = 0) -> float:
    """
    Apply ENSDF successive rounding digit-by-digit from right to left.

    Args:
        value: numeric value to round
        tgt_decimals: target number of decimal places
        threshold: rounding threshold for the discarded digit
            5 => standard round-half-up for general values
            4 => conservative uncertainty rounding
        min_src_decimals: minimum source precision to honor when the original
            input carried trailing zeros not preserved by float conversion
    """
    from decimal import Decimal, ROUND_DOWN

    sign = -1 if value < 0 else 1
    d = Decimal(str(abs(value)))
    src_decimals = max(_decimal_places_from_value(value), min_src_decimals)

    for nd in range(src_decimals, tgt_decimals, -1):
        shift = Decimal(10) ** (nd - 1)
        scaled = d * shift
        floor_val = int(scaled.to_integral_value(rounding=ROUND_DOWN))
        remainder_digit = int((scaled - floor_val) * 10)
        if remainder_digit >= threshold:
            floor_val += 1
        d = Decimal(floor_val) / shift

    return float(d) * sign


def _successive_round_4up(value: float, tgt_decimals: int, min_src_decimals: int = 0) -> float:
    """Apply ENSDF successive 4-up uncertainty rounding."""
    return _successive_round(value, tgt_decimals, threshold=4, min_src_decimals=min_src_decimals)


def _successive_round_5up(value: float, tgt_decimals: int, min_src_decimals: int = 0) -> float:
    """Apply ENSDF successive 5-up general-value rounding."""
    return _successive_round(value, tgt_decimals, threshold=5, min_src_decimals=min_src_decimals)


def _ensdf_unc_target_decimals(unc: float) -> int:
    """
    Determine target decimal places for ENSDF uncertainty display.
    Rule: express uncertainty to 1 sig fig if leading-2-digits >= 35;
          express to 2 sig figs if leading-2-digits in [10, 34].
    Uses 4-up successive rounding to determine the rounded leading-2-digit value.
    """
    if unc <= 0:
        return 0
    import math
    # Order of magnitude: floor(log10(unc))
    log10 = math.floor(math.log10(unc))
    # Scale to 2-digit integer representation (10.x to 99.x)
    leading_raw = unc / (10.0 ** (log10 - 1))  # 10.0 to 99.9...
    # Apply successive 4-up rounding from raw precision to 2 decimal places of leading_raw
    # (i.e., from ~4 sig digits to 2 sig digits of the leading scaled value)
    raw_dec = max(0, 4)  # work with 4 extra digits of leading_raw
    rounded_leading = _successive_round_4up(leading_raw, 0, min_src_decimals=raw_dec)
    leading_2 = int(rounded_leading)
    if leading_2 >= 35:  # or single digit after rounding up to 100+
        n_sig = 1
    else:
        n_sig = 2
    # Decimal places = n_sig - (log10 + 1)
    target_dec = n_sig - log10 - 1
    return target_dec


def fmt_val_unc(val: float, unc: float, src_max_decimals: int) -> str:
    """
    Format value(uncertainty) in ENSDF notation matching Java XDX2SDS.
    Uses ENSDF successive 4-up rounding: each digit removed right-to-left;
    digit 0-3 rounds down, digit 4-9 rounds up.
    Decimal places are determined by the uncertainty sig-fig rule, not src_max_decimals.
    src_max_decimals is the raw precision of the inputs (used as starting point).
    """
    if unc <= 0:
        return f"{val}(0)"
    # Step 1: determine target decimal places from uncertainty
    tgt_dec = _ensdf_unc_target_decimals(unc)
    tgt_dec = max(0, tgt_dec)
    # Step 2: apply successive 4-up rounding to uncertainty
    rounded_unc = _successive_round_4up(unc, tgt_dec, min_src_decimals=src_max_decimals + 2)
    unc_int = int(round(rounded_unc * 10**tgt_dec))
    if unc_int == 0:
        unc_int = 1  # floor at 1
    # Step 3: round value to tgt_dec decimal places using successive 5-up.
    val_rounded = _successive_round_5up(val, tgt_dec, min_src_decimals=src_max_decimals)
    val_str = f"{val_rounded:.{tgt_dec}f}"
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

    # Truncate at "Other:" / "Others:" — values after this are NOT part of the averaging set
    other_match = re.search(r'\bOthers?\b', text, re.IGNORECASE)
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
        # Extract record name from comment header: T$, E$, RI$, etc.
        import re as _re
        m = _re.search(r'\b([A-Za-z]{1,2})\$', comment_text)
        record_name = m.group(1).upper() if m else 'T'

    # --- Numeric mode ---
    # Strip commas used as pair separators: "19.7 1.3, 22 4, 21.5 1.5"
    else:
        flat = [a.rstrip(',') for a in args if a != ',']
        if len(flat) >= 4 and len(flat) % 2 == 0 and all(a.replace('.','').replace('-','').replace('+','').isdigit() for a in flat):
            data = []
            for i in range(0, len(flat), 2):
                value = float(flat[i])
                unc = float(flat[i + 1])
                data.append((value, unc, unc))
            base_unit = None
            max_dec = count_max_decimals(data)
            record_name = 'E'  # numeric mode default
        else:
            print(__doc__)
            print("\nError: provide either:")
            print("  Numeric mode : VALUE1 UNC1[,] VALUE2 UNC2[,] ...")
            print("  Comment mode : --comment \"ENSDF comment text\"")
            sys.exit(1)

    n = len(data)

    # Calculate weighted and unweighted averages
    wt_result = weighted_average(data)
    uwt_result = unweighted_average(data)

    # Display critical chi^2: chi^2(N, 90%) — Java EnsdfUtil.criticalReducedChi2(N)
    # DISPLAY ONLY — the adoption DECISION uses hardcoded threshold INCONSISTENCY_THRESHOLD = 3.5
    crit_display = critical_chi_sq_display(n)

    # Unweighted chi^2/(n-1): Java avg.unweightedChi2() = sum((x_i - mean_u)^2) / (n-1)
    # Note: Java does NOT normalize by individual variances here.
    mean_uwt = uwt_result['value']
    uwt_chi2_display = sum(
        (v - mean_uwt)**2
        for v, lo, hi in data
    ) / (n - 1) if n > 1 else 0.0

    # Internal/external shown raw — min-unc rule applied only to the final suggested result
    wt_int_disp = wt_result['internal_unc']
    wt_ext_disp = wt_result['external_unc']
    uwt_disp = uwt_result['final_unc']

    unit_label = f" {base_unit}" if base_unit else ""

    # --- Print output matching Java AverageTool format ---
    print()
    print(f"------ average {record_name}------")
    print(f"Data points of {record_name} record")
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
    # Java: if avg.isEqualWeighted(avg_all) -> "Weighted-Of-All" (all points used)
    # Java: else -> "Weighted-Of-All" with avg_all, or default weighted
    # For the Python (no weight-threshold exclusion): all points are always used,
    # so avg == avg_all -> label is always "Weighted-Of-All" when chi2 <= 3.5.
    chi2_val = wt_result['reduced_chi_sq']

    if chi2_val <= INCONSISTENCY_THRESHOLD:
        label = "Weighted-Of-All"  # all points used (no weight exclusion in this implementation)
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

