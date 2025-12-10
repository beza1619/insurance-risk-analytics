import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import json

def setup_plotting():
    """Setup matplotlib style"""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("Set2")
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.figsize'] = [12, 8]

def plot_loss_ratio_by_province(df, save_path):
    """Create loss ratio by province bar chart"""
    if 'province' not in df.columns or 'loss_ratio' not in df.columns:
        print("Missing required columns for province plot")
        return
    
    province_stats = df.groupby('province')['loss_ratio'].agg(['mean', 'std']).sort_values('mean')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(province_stats.index, province_stats['mean'], 
                  yerr=province_stats['std'], capsize=5, 
                  color=plt.cm.RdYlGn(np.linspace(0, 1, len(province_stats))))
    
    ax.set_title('Loss Ratio by Province', fontsize=16, fontweight='bold')
    ax.set_xlabel('Province', fontsize=12)
    ax.set_ylabel('Average Loss Ratio', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1%}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

def plot_correlation_matrix(df, save_path):
    """Create correlation matrix heatmap"""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) < 2:
        print("Not enough numerical columns for correlation matrix")
        return
    
    corr_matrix = df[numerical_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=0.5, ax=ax)
    
    ax.set_title('Correlation Matrix of Numerical Features', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

def plot_risk_heatmap(df, save_path):
    """Create province vs vehicle type risk heatmap"""
    if 'province' not in df.columns or 'vehicle_type' not in df.columns or 'loss_ratio' not in df.columns:
        print("Missing required columns for heatmap")
        return
    
    pivot = pd.pivot_table(df, values='loss_ratio', 
                          index='province', 
                          columns='vehicle_type', 
                          aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r',
                linewidths=0.5, ax=ax, cbar_kws={'label': 'Loss Ratio'})
    
    ax.set_title('Risk Heatmap: Province vs Vehicle Type', fontsize=16, fontweight='bold')
    ax.set_xlabel('Vehicle Type', fontsize=12)
    ax.set_ylabel('Province', fontsize=12)
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

def main():
    """Main visualization function"""
    setup_plotting()
    
    # Load processed data
    df = pd.read_csv('data/processed/cleaned_data.csv')
    print(f"Data loaded: {df.shape}")
    
    # Create output directory
    Path('reports/figures').mkdir(parents=True, exist_ok=True)
    Path('reports/metrics').mkdir(parents=True, exist_ok=True)
    
    # Create plots
    plot_loss_ratio_by_province(df, 'reports/figures/loss_ratio_by_province.png')
    plot_correlation_matrix(df, 'reports/figures/correlation_matrix.png')
    plot_risk_heatmap(df, 'reports/figures/risk_heatmap.png')
    
    # Create EDA metrics
    metrics = {
        'total_policies': len(df),
        'average_premium': df['premium'].mean() if 'premium' in df.columns else 0,
        'average_claims': df['total_claims'].mean() if 'total_claims' in df.columns else 0,
        'overall_loss_ratio': df['loss_ratio'].mean() if 'loss_ratio' in df.columns else 0,
        'unique_provinces': df['province'].nunique() if 'province' in df.columns else 0,
        'unique_vehicle_types': df['vehicle_type'].nunique() if 'vehicle_type' in df.columns else 0
    }
    
    # Save metrics
    with open('reports/metrics/eda_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("Visualization complete!")

if __name__ == "__main__":
    main()