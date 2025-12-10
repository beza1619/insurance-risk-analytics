# test_hypothesis.py
"""
Test the hypothesis testing module.
"""

import pandas as pd
import numpy as np

# Create test data
print("Creating test data for hypothesis testing...")

np.random.seed(42)
n_samples = 100

# Create provinces with different risk levels
data = {
    'Province': np.random.choice(['Gauteng', 'Western Cape', 'Free State'], n_samples),
    'TotalPremium': np.random.randint(5000, 20000, n_samples),
}

# Make Gauteng high risk, Free State low risk
claims = []
for i in range(n_samples):
    base = np.random.randint(0, 5000)
    if data['Province'][i] == 'Gauteng':
        base *= 2.0  # High risk
    elif data['Province'][i] == 'Free State':
        base *= 0.6  # Low risk
    else:
        base *= 1.0  # Medium risk
    claims.append(base)

data['TotalClaims'] = claims
df = pd.DataFrame(data)
df['LossRatio'] = df['TotalClaims'] / df['TotalPremium']

# Save test data
df.to_csv('data/processed/test_hypothesis_data.csv', index=False)
print(f"Saved test data: {len(df)} rows")

# Show province statistics
print("\nProvince statistics:")
for province in df['Province'].unique():
    subset = df[df['Province'] == province]
    avg_lr = subset['LossRatio'].mean()
    print(f"{province:15} Avg Loss Ratio: {avg_lr:.3f} ({len(subset)} policies)")
