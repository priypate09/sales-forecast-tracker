"""
Analyze forecast accuracy
"""
import pandas as pd
import numpy as np


def calculate_accuracy(forecast_df, actual_df):
    """
    Calculate forecast accuracy metrics by sales rep
    
    Returns DataFrame with:
    - forecast_amount: Total forecasted
    - actual_amount: Total closed
    - accuracy_pct: Percentage accuracy
    - dollar_error: Dollar difference
    - num_deals: Number of deals
    """
    # Merge forecast and actuals
    merged = forecast_df.merge(
        actual_df[['opportunity_id', 'amount', 'status']], 
        on='opportunity_id',
        suffixes=('_forecast', '_actual')
    )
    
    # Group by rep
    results = []
    for rep in merged['rep_name'].unique():
        rep_data = merged[merged['rep_name'] == rep]
        
        forecast_amt = rep_data['amount_forecast'].sum()
        actual_amt = rep_data[rep_data['status'] == 'won']['amount_actual'].sum()
        
        # Calculate accuracy percentage
        accuracy = (actual_amt / forecast_amt * 100) if forecast_amt > 0 else 0
        
        results.append({
            'rep_name': rep,
            'forecast_amount': forecast_amt,
            'actual_amount': actual_amt,
            'accuracy_pct': round(accuracy, 1),
            'dollar_error': actual_amt - forecast_amt,
            'num_deals': len(rep_data)
        })
    
    return pd.DataFrame(results)


def calculate_category_accuracy(forecast_df, actual_df):
    """
    Calculate accuracy by forecast category (best_case, commit, pipeline)
    """
    merged = forecast_df.merge(
        actual_df[['opportunity_id', 'amount', 'status']], 
        on='opportunity_id',
        suffixes=('_forecast', '_actual')
    )
    
    results = []
    for category in merged['forecast_category'].unique():
        cat_data = merged[merged['forecast_category'] == category]
        
        forecast_amt = cat_data['amount_forecast'].sum()
        actual_amt = cat_data[cat_data['status'] == 'won']['amount_actual'].sum()
        
        accuracy = (actual_amt / forecast_amt * 100) if forecast_amt > 0 else 0
        
        results.append({
            'category': category,
            'forecast_amount': forecast_amt,
            'actual_amount': actual_amt,
            'accuracy_pct': round(accuracy, 1),
            'num_deals': len(cat_data)
        })
    
    return pd.DataFrame(results)


def get_top_performers(accuracy_df, top_n=3):
    """
    Identify top performing reps by accuracy
    """
    return accuracy_df.nlargest(top_n, 'accuracy_pct')[['rep_name', 'accuracy_pct']]


def get_biggest_misses(accuracy_df, top_n=3):
    """
    Identify reps with largest forecast errors
    """
    accuracy_df['abs_error'] = accuracy_df['dollar_error'].abs()
    return accuracy_df.nlargest(top_n, 'abs_error')[['rep_name', 'dollar_error']]


if __name__ == "__main__":
    # Test with sample data
    from data_loader import load_forecast_data, load_actual_result
    
    print("Testing analyzer module...")
    
    forecast = load_forecast_data('data/sample_forecast.csv')
    actuals = load_actual_results('data/sample_actuals.csv')
    
    print("\nRep Accuracy:")
    print(calculate_accuracy(forecast, actuals))
    
    print("\nCategory Accuracy:")
    print(calculate_category_accuracy(forecast, actuals))
    