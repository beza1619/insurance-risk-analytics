import pandas as pd
import numpy as np
import json
from pathlib import Path

print("Starting data preprocessing...")

# Load data
df = pd.read_csv('data/raw/insurance_sample_data.csv')
print(f"Loaded data: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Basic cleaning
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())
        print(f"Filled missing values in {col}")

# Create loss ratio if columns exist
if 'total_claims' in df.columns and 'premium' in df.columns:
    df['loss_ratio'] = df['total_claims'] / df['premium'].replace(0, 1)
    print("Created loss_ratio column")

# Save processed data
Path('data/processed').mkdir(parents=True, exist_ok=True)
output_path = 'data/processed/cleaned_data.csv'
df.to_csv(output_path, index=False)
print(f"Saved processed data to {output_path}")

# Create metrics
Path('reports/metrics').mkdir(parents=True, exist_ok=True)
metrics = {
    'original_rows': df.shape[0],
    'original_columns': df.shape[1],
    'missing_values_total': df.isnull().sum().sum(),
    'columns_with_missing': df.isnull().any().sum()
}

if 'loss_ratio' in df.columns:
    metrics['average_loss_ratio'] = float(df['loss_ratio'].mean())
    metrics['min_loss_ratio'] = float(df['loss_ratio'].min())
    metrics['max_loss_ratio'] = float(df['loss_ratio'].max())

# Create metrics
Path('reports/metrics').mkdir(parents=True, exist_ok=True)

# Convert numpy types to Python native types for JSON serialization
metrics = {
    'original_rows': int(df.shape[0]),  # Convert to int
    'original_columns': int(df.shape[1]),  # Convert to int
    'missing_values_total': int(df.isnull().sum().sum()),  # Convert to int
    'columns_with_missing': int(df.isnull().any().sum())  # Convert to int
}

if 'LossRatio' in df.columns:
    metrics['average_loss_ratio'] = float(df['LossRatio'].mean())
    metrics['min_loss_ratio'] = float(df['LossRatio'].min())
    metrics['max_loss_ratio'] = float(df['LossRatio'].max())

with open('reports/metrics/preprocess_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("Preprocessing complete!")
print(f"Metrics saved to reports/metrics/preprocess_metrics.json")