import pandas as pd
import json
from pathlib import Path
import sys

def main():
    print("🚀 Starting data preprocessing...")
    
    try:
        # Load data
        df = pd.read_csv('data/raw/insurance_sample_data.csv')
        print(f"✅ Data loaded: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Basic preprocessing
        if 'TotalClaims' in df.columns and 'TotalPremium' in df.columns:
            df['LossRatio'] = df['TotalClaims'] / df['TotalPremium'].replace(0, 1)
            print(f"📊 LossRatio calculated - Mean: {df['LossRatio'].mean():.3f}")
        
        # Save processed data
        Path('data/processed').mkdir(parents=True, exist_ok=True)
        output_path = 'data/processed/cleaned_data.csv'
        df.to_csv(output_path, index=False)
        print(f"💾 Saved processed data to: {output_path}")
        
        # Save metrics
        Path('reports/metrics').mkdir(parents=True, exist_ok=True)
        metrics = {
            'rows': int(len(df)),
            'cols': int(len(df.columns)),
            'avg_loss_ratio': float(df['LossRatio'].mean()) if 'LossRatio' in df.columns else 0,
            'data_file': 'data/raw/insurance_sample_data.csv'
        }
        
        metrics_path = 'reports/metrics/preprocess.json'
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"📈 Metrics saved to: {metrics_path}")
        print("🎉 Preprocessing completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())