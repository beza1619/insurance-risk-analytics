import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import json

print("Creating visualizations...")

# Load processed data
df = pd.read_csv('data/processed/cleaned_data.csv')
print(f"Loaded data: {df.shape}")

# Create output directory
Path('reports/figures').mkdir(parents=True, exist_ok=True)

# 1. Loss Ratio by Province (if province column exists)
if 'province' in df.columns and 'loss_ratio' in df.columns:
    plt.figure(figsize=(12, 6))
    province_stats = df.groupby('province')['loss_ratio'].mean().sort_values()
    
    colors = plt.cm.RdYlGn(np.linspace(0, 1, len(province_stats)))
    bars = plt.bar(province_stats.index, province_stats.values, color=colors)
    
    plt.title('Loss Ratio by Province', fontsize=16, fontweight='bold')
    plt.xlabel('Province')
    plt.ylabel('Average Loss Ratio')
    plt.xticks(rotation=45)
    
    # Add values on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1%}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('reports/figures/loss_ratio_by_province.png', dpi=300)
    plt.close()
    print("✅ Created loss_ratio_by_province.png")

# 2. Correlation Matrix
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 8))
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('reports/figures/correlation_matrix.png', dpi=300)
    plt.close()
    print("✅ Created correlation_matrix.png")

# 3. Risk Heatmap (if both province and vehicle_type exist)
if 'province' in df.columns and 'vehicle_type' in df.columns and 'loss_ratio' in df.columns:
    try:
        pivot = pd.pivot_table(df, values='loss_ratio', 
                              index='province', 
                              columns='vehicle_type', 
                              aggfunc='mean')
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r')
        plt.title('Risk Heatmap: Province vs Vehicle Type', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('reports/figures/risk_heatmap.png', dpi=300)
        plt.close()
        print("✅ Created risk_heatmap.png")
    except:
        print("⚠ Could not create risk heatmap")

# Save EDA metrics
metrics = {
    'total_policies': len(df),
    'total_columns': len(df.columns),
    'numeric_columns': len(numeric_cols),
    'categorical_columns': len(df.select_dtypes(include=['object']).columns)
}

if 'premium' in df.columns:
    metrics['average_premium'] = float(df['premium'].mean())

if 'total_claims' in df.columns:
    metrics['average_claims'] = float(df['total_claims'].mean())

if 'loss_ratio' in df.columns:
    metrics['overall_loss_ratio'] = float(df['loss_ratio'].mean())

Path('reports/metrics').mkdir(parents=True, exist_ok=True)
with open('reports/metrics/eda_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("✅ Visualizations complete!")
print("📊 Metrics saved to reports/metrics/eda_metrics.json")