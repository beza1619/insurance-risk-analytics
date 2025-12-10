import pandas as pd
import numpy as np
import json
from pathlib import Path

# Simple config since yaml might not be installed
CONFIG = {
    'data': {
        'raw_path': 'data/raw/insurance_sample_data.csv',
        'processed_path': 'data/processed/cleaned_data.csv'
    },
    'preprocessing': {
        'missing_threshold': 0.3
    }
}

def load_data(filepath):
    """Load insurance data"""
    return pd.read_csv(filepath)

def clean_data(df):
    """Clean the insurance data"""
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    
    # Create new features
    if 'premium' in df.columns and 'total_claims' in df.columns:
        df['loss_ratio'] = df['total_claims'] / df['premium'].replace(0, 1)
    
    if 'previous_claims' in df.columns:
        df['has_previous_claims'] = (df['previous_claims'] > 0).astype(int)
    
    # Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col in df.columns:
            df[f'{col}_code'] = pd.Categorical(df[col]).codes
    
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