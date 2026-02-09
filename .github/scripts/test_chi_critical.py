#!/usr/bin/env python3
"""Test critical chi-squared values to match Java tool"""
from scipy import stats

df = 5  # degrees of freedom (n-1 for 6 data points)

print("Testing different confidence levels for df=5:")
print("=" * 60)
for conf in [0.90, 0.95, 0.975, 0.98, 0.985, 0.99, 0.995]:
    chi_full = stats.chi2.ppf(conf, df)
    chi_red = chi_full / df
    print(f"Confidence {conf:.3f}: chi^2={chi_full:.4f}, reduced={chi_red:.4f}")

print("\n" + "=" * 60)
crit_target = 2.802
chi_full_target = crit_target * df
conf_result = stats.chi2.cdf(chi_full_target, df)
print(f"For reduced critical = {crit_target}:")
print(f"  Full chi^2 = {chi_full_target:.4f}")
print(f"  Confidence level = {conf_result:.4f} ({conf_result*100:.2f}%)")
