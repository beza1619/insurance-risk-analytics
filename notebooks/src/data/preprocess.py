
# src/data/preprocess.py
"""
Data preprocessing pipeline for ACIS insurance analytics.
Version: 1.0
"""
import pandas as pd
import numpy as np
import yaml
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path="config/params.yaml"):
    """Load configuration parameters"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def calculate_business_metrics(df):
    """Calculate key business metrics"""
    logger.info("Calculating business metrics...")
    
    # Calculate Loss Ratio
    if 'TotalClaims' in df.columns and 'TotalPremium' in df.columns:
        df['LossRatio'] = df['TotalClaims'] / df['TotalPremium']
        df['HasClaim'] = (df['TotalClaims'] > 0).astype(int)
        logger.info(f"Loss Ratio calculated. Range: {df['LossRatio'].min():.3f} to {df['LossRatio'].max():.3f}")
    
    # Calculate Vehicle Age if not present
    if 'VehicleAge' not in df.columns and 'Year' in df.columns:
        current_year = pd.Timestamp.now().year
        df['VehicleAge'] = current_year - df['Year']
        logger.info(f"VehicleAge calculated. Range: {df['VehicleAge'].min()} to {df['VehicleAge'].max()} years")
    
    return df

def clean_data(df):
    """Clean and validate data"""
    logger.info("Cleaning data...")
    
    initial_rows = len(df)
    
    # Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    if duplicates_removed > 0:
        logger.warning(f"Removed {duplicates_removed} duplicate rows")
    
    # Handle missing values
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        logger.warning(f"Missing values found: {missing_counts[missing_counts > 0].to_dict()}")
        
        # Fill numeric columns with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())
                logger.info(f"Filled missing values in {col} with median")
        
        # Fill categorical columns with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])
                logger.info(f"Filled missing values in {col} with mode")
    else:
        logger.info("No missing values found")
    
    return df

def save_metrics(df, output_path):
    """Save preprocessing metrics"""
    metrics = {
        'preprocessing': {
            'original_rows': int(len(df)),
            'duplicates_removed': int(duplicates_removed) if 'duplicates_removed' in locals() else 0,
            'final_rows': int(len(df)),
            'columns_count': int(len(df.columns)),
            'memory_usage_mb': float(df.memory_usage().sum() / 1024 / 1024)
        },
        'business_metrics': {
            'overall_loss_ratio': float(df['LossRatio'].mean()) if 'LossRatio' in df.columns else None,
            'claim_frequency': float(df['HasClaim'].mean()) if 'HasClaim' in df.columns else None,
            'total_premium': float(df['TotalPremium'].sum()) if 'TotalPremium' in df.columns else None,
            'total_claims': float(df['TotalClaims'].sum()) if 'TotalClaims' in df.columns else None
        }
    }
    
    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info(f"Metrics saved to {output_path}")
    return metrics

def main():
    """Main preprocessing function"""
    logger.info("Starting data preprocessing pipeline...")
    
    # Load configuration
    config = load_config()
    logger.info(f"Loaded configuration from config/params.yaml")
    
    # Load data
    input_path = "data/raw/insurance_data.csv"
    output_path = "data/processed/cleaned_data.csv"
    metrics_path = "reports/metrics/preprocess_metrics.json"
    
    logger.info(f"Loading data from {input_path}")
    try:
        df = pd.read_csv(input_path)
        logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        logger.error(f"File not found: {input_path}")
        raise
    
    # Process data
    df = calculate_business_metrics(df)
    df = clean_data(df)
    
    # Save processed data
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Processed data saved to {output_path}")
    
    # Save metrics
    metrics = save_metrics(df, metrics_path)
    
    logger.info("Preprocessing pipeline completed successfully!")
    return df

if __name__ == "__main__":
    main()
