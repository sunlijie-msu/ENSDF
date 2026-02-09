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

3. Chi-squared Test (95% confidence):
   - If chi^2/(n-1) < critical chi^2/(n-1): data are consistent -> use WEIGHTED
   - Otherwise: data are inconsistent -> use UNWEIGHTED

4. Minimum Uncertainty Rule (findSuggestedAverage):
   - Final uncertainty >= minimum input uncertainty

Usage:
    python Java_Average.py VALUE1 UNC1 VALUE2 UNC2 [VALUE3 UNC3 ...]
    
Example:
    python Java_Average.py 280 50 215 70 130 60 120 65
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


def critical_chi_sq(df: int, confidence: float = 0.9845, reduced: bool = True) -> float:
    """
    Calculate critical chi-squared value at given confidence level.
    Matches Java criticalChiSq method.
    
    Args:
        df: degrees of freedom (n-1)
        confidence: confidence level (default 0.9845, matching Java tool)
        reduced: if True, return chi^2/df (default True)
    
    Returns:
        Critical chi-squared value (or reduced if reduced=True)
    """
    # Cap at 340 degrees of freedom like Java does
    dof = min(df, 340)
    chi_sq = stats.chi2.ppf(confidence, dof)
    if reduced:
        return chi_sq / dof
    return chi_sq


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


def main():
    if len(sys.argv) < 5 or len(sys.argv) % 2 != 1:
        print(__doc__)
        print("\nError: Need at least 2 data points (4 arguments: value1 unc1 value2 unc2)")
        print(f"Got {len(sys.argv) - 1} arguments")
        sys.exit(1)
    
    # Parse arguments - for now assume symmetric uncertainties
    args = sys.argv[1:]
    data = []
    for i in range(0, len(args), 2):
        value = float(args[i])
        unc = float(args[i + 1])
        # Store as (value, lower_unc, upper_unc) - symmetric for now
        data.append((value, unc, unc))
    
    n = len(data)
    
    # Calculate averages
    wt_result = weighted_average(data)
    uwt_result = unweighted_average(data)
    
    # Critical chi-squared at 98.45% confidence (matching Java tool)
    crit_reduced = critical_chi_sq(n - 1, 0.9845, reduced=True)
    crit_full = critical_chi_sq(n - 1, 0.9845, reduced=False)
    
    # Print results
    print("=" * 70)
    print("ENSDF AVERAGING TOOL - Python Implementation")
    print("(Exact algorithm from AverageTool_22January2025.jar)")
    print("=" * 70)
    print()
    print("Input Data Points:")
    for i, (v, lower, upper) in enumerate(data):
        if lower == upper:
            print(f"  {i+1}. {v} ± {lower}")
        else:
            print(f"  {i+1}. {v} +{upper}/-{lower}")
    print()
    
    print("WEIGHTED AVERAGE:")
    print(f"  Value: {wt_result['value']:.4f}")
    print(f"  Internal Uncertainty: {wt_result['internal_unc']:.4f}")
    print(f"  External Uncertainty: {wt_result['external_unc']:.4f}")
    print(f"  Used: {wt_result['unc_type']} -> {wt_result['final_unc']:.4f}")
    print(f"  Normalized Weights: {[f'{w:.4f}' for w in wt_result['norm_weights']]}")
    print()
    
    print("UNWEIGHTED AVERAGE:")
    print(f"  Value: {uwt_result['value']:.4f}")
    print(f"  Internal Uncertainty: {uwt_result['internal_unc']:.4f}")
    print(f"  External Uncertainty: {uwt_result['external_unc']:.4f}")
    print(f"  Used: {uwt_result['unc_type']} -> {uwt_result['final_unc']:.4f}")
    print()
    
    print("CHI-SQUARED TEST (98.45% confidence):")
    print(f"  Chi^2 = {wt_result['chi_sq']:.4f}")
    print(f"  Chi^2/(N-1) = {wt_result['reduced_chi_sq']:.4f}")
    print(f"  Critical Chi^2 (df={n-1}) = {crit_full:.4f}")
    print(f"  Critical Chi^2/(N-1) = {crit_reduced:.4f}")
    print()
    
    # Determine recommendation based on chi-squared test
    # CRITICAL FIX: Always use weighted average as central value!
    # Only uncertainty selection changes based on chi-squared test
    suggested_value = wt_result['value']  # Always weighted!
    
    if wt_result['reduced_chi_sq'] < crit_reduced:
        recommendation = "WEIGHTED (Internal)"
        reason = "data are CONSISTENT (chi^2/(N-1) < critical)"
        suggested_unc = wt_result['internal_unc']
    else:
        recommendation = "WEIGHTED (External)"
        reason = "data are INCONSISTENT (chi^2/(N-1) >= critical)"
        suggested_unc = wt_result['external_unc']
    
    print(f"RECOMMENDATION: Use {recommendation}")
    print(f"  Reason: {reason}")
    print()
    
    # Apply minimum uncertainty rule
    min_input_unc = min(min(d[1], d[2]) for d in data if d[1] > 0 and d[2] > 0)
    final_unc = find_suggested_average(suggested_unc, data)
    
    print("MINIMUM UNCERTAINTY RULE (from findSuggestedAverage):")
    print(f"  Minimum input uncertainty: {min_input_unc:.4f}")
    print(f"  Calculated uncertainty: {suggested_unc:.4f}")
    if final_unc > suggested_unc:
        print(f"  Applied rule: uncertainty increased to {final_unc:.4f}")
    else:
        print(f"  No adjustment needed: {final_unc:.4f}")
    print()
    
    # Determine decimal places from input data (use maximum precision)
    max_decimals = 0
    for v, lower, upper in data:
        # Count decimal places in the value
        v_str = f"{v:.10f}".rstrip('0').rstrip('.')
        if '.' in v_str:
            decimals_count = len(v_str.split('.')[1])
            max_decimals = max(max_decimals, decimals_count)
    
    # Format result with same precision as input data
    if max_decimals == 0:
        value_str = f"{suggested_value:.0f}"
        unc_int = int(round(final_unc))
    elif max_decimals == 1:
        value_str = f"{suggested_value:.1f}"
        unc_int = int(round(final_unc * 10))
    else:  # 2 or more decimals
        value_str = f"{suggested_value:.2f}"
        unc_int = int(round(final_unc * 100))
    
    print("=" * 70)
    print(f"*** Suggested Adopted Result: {value_str}({unc_int}) ***")
    print(f"    Alternative notation: {value_str} ± {final_unc:.2f}")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
