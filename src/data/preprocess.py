import pandas as pd
import numpy as np
import yaml
from pathlib import Path

def load_config():
    """Load configuration from params.yaml"""
    with open('params.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_data(filepath):
    """Load insurance data"""
    return pd.read_csv(filepath)

def clean_data(df):
    """Clean the insurance data"""
    # Handle missing values
    df = df.fillna({
        'vehicle_age': df['vehicle_age'].median(),
        'cubic_capacity': df['cubic_capacity'].median(),
        'premium': df['premium'].median(),
        'total_claims': 0
    })
    
    # Create new features
    df['loss_ratio'] = df['total_claims'] / df['premium'].replace(0, 1)
    df['has_previous_claims'] = (df.get('previous_claims', 0) > 0).astype(int)
    
    # Encode categorical variables
    if 'province' in df.columns:
        df['province_code'] = pd.Categorical(df['province']).codes
    
    if 'vehicle_type' in df.columns:
        df['vehicle_type_code'] = pd.Categorical(df['vehicle_type']).codes
    
    return df

def save_data(df, filepath):
    """Save processed data"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

def main():
    """Main preprocessing function"""
    config = load_config()
    
    # Load raw data
    raw_path = config['data']['raw_path']
    print(f"Loading data from {raw_path}")
    df = load_data(raw_path)
    print(f"Original shape: {df.shape}")
    
    # Clean data
    df = clean_data(df)
    print(f"Cleaned shape: {df.shape}")
    
    # Save processed data
    processed_path = config['data']['processed_path']
    save_data(df, processed_path)
    
    # Create metrics
    metrics = {
        'original_rows': df.shape[0],
        'original_columns': df.shape[1],
        'missing_values': df.isnull().sum().sum(),
        'average_loss_ratio': df['loss_ratio'].mean() if 'loss_ratio' in df.columns else 0
    }
    
    # Save metrics
    import json
    with open('reports/metrics/preprocess_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("Preprocessing complete!")

if __name__ == "__main__":
    main()