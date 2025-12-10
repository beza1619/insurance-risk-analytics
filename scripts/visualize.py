import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

print("🎨 Creating visualizations...")

try:
    # Load processed data
    df = pd.read_csv('data/processed/cleaned_data.csv')
    print(f"✅ Data loaded: {df.shape}")
    
    # Create output directories
    Path('reports/figures').mkdir(parents=True, exist_ok=True)
    Path('reports/metrics').mkdir(parents=True, exist_ok=True)
    
    # 1. Loss Ratio by Province (if columns exist)
    if 'Province' in df.columns and 'LossRatio' in df.columns:
        plt.figure(figsize=(12, 6))
        province_stats = df.groupby('Province')['LossRatio'].mean().sort_values()
        colors = plt.cm.RdYlGn(range(len(province_stats)))
        plt.bar(province_stats.index, province_stats.values, color=colors)
        plt.title('Loss Ratio by Province')
        plt.xlabel('Province')
        plt.ylabel('Average Loss Ratio')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/figures/loss_ratio_by_province.png', dpi=100)
        plt.close()
        print("✅ Created: loss_ratio_by_province.png")
    
    # 2. Simple correlation matrix
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 1:
        plt.figure(figsize=(10, 8))
        corr_matrix = df[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.savefig('reports/figures/correlation_matrix.png', dpi=100)
        plt.close()
        print("✅ Created: correlation_matrix.png")
    
    # Save visualization metrics
    metrics = {
        'figures_created': 2,
        'data_shape': df.shape,
        'numeric_columns': len(numeric_cols)
    }
    
    with open('reports/metrics/visualization.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("🎉 Visualization completed successfully!")
    
except Exception as e:
    print(f"❌ Error during visualization: {e}")