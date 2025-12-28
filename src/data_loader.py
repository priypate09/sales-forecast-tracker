"""
Load and data validation of forecast files
"""
import pandas as pd
from datetime import datetime


def load_forecast_data(filepath):
    """
    Load forecast snapshot from CSV
    
    columns:
    - rep_name: Sales rep name
    - opportunity_id: Unique deal ID
    - amount: Deal size
    - forecast_category: best_case, commit, or pipeline
    - close_date: Expected close date
    - snapshot_date: When forecast was submitted
    """
    df = pd.read_csv(filepath)
    
    # Basic validation
    required_cols = ['rep_name', 'opportunity_id', 'amount', 
                     'forecast_category', 'close_date', 'snapshot_date']
    
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    # Convert dates
    df['close_date'] = pd.to_datetime(df['close_date'])
    df['snapshot_date'] = pd.to_datetime(df['snapshot_date'])
    
    return df


def load_actual_results(filepath):
    """
    Load actual closed deals
    
    columns:
    - opportunity_id: Unique deal ID
    - amount: Actual closed amount
    - close_date: Actual close date
    - status: won or lost
    """
    df = pd.read_csv(filepath)
    
    required_cols = ['opportunity_id', 'amount', 'close_date', 'status']
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    df['close_date'] = pd.to_datetime(df['close_date'])
    
    return df


if __name__ == "__main__":
    # Quick test
    print("Data loader module ready")