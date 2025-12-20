"""Generate sample forecast and actual data for testing"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed
np.random.seed(42)

# Sales rep names
reps = ['Alice Johnson', 'Bob Chen', 'Charlie Martinez', 'Diana Smith', 'Eric Wilson']

# forecast data (50 deals)
num_deals = 50
forecast_data = []

for i in range(num_deals):
    forecast_data.append({
        'rep_name': np.random.choice(reps),
        'opportunity_id': f'OPP-{i+1:03d}',
        'amount': np.random.randint(10, 500) * 1000,
        'forecast_category': np.random.choice(
            ['best_case', 'commit', 'pipeline'], 
            p=[0.2, 0.5, 0.3]
        ),
        'close_date': datetime(2024, 12, 31) + timedelta(days=np.random.randint(-30, 30)),
        'snapshot_date': datetime(2024, 11, 15)
    })

df_forecast = pd.DataFrame(forecast_data)

# Generate actual results
actual_data = []

for opp in forecast_data:
    # Win rate depends on forecast category
    if opp['forecast_category'] == 'best_case':
        won = np.random.random() < 0.85
    elif opp['forecast_category'] == 'commit':
        won = np.random.random() < 0.70
    else:
        won = np.random.random() < 0.40
    
    actual_data.append({
        'opportunity_id': opp['opportunity_id'],
        'amount': opp['amount'] if won else 0,
        'close_date': opp['close_date'] + timedelta(days=np.random.randint(-10, 20)),
        'status': 'won' if won else 'lost'
    })

df_actual = pd.DataFrame(actual_data)

# Save to CSV
df_forecast.to_csv('data/sample_forecast.csv', index=False)
df_actual.to_csv('data/sample_actuals.csv', index=False)

# Print summary
print("Sample data generated successfully!")
print(f"\nForecast data:")
print(f"  - {len(df_forecast)} opportunities")
print(f"  - Total forecast: ${df_forecast['amount'].sum():,.0f}")
print(f"\nActual results:")
print(f"  - Won: {(df_actual['status']=='won').sum()} deals")
print(f"  - Lost: {(df_actual['status']=='lost').sum()} deals")
print(f"  - Win rate: {(df_actual['status']=='won').sum() / len(df_actual):.1%}")
print(f"  - Total closed: ${df_actual[df_actual['status']=='won']['amount'].sum():,.0f}")