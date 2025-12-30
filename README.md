# Sales Forecast Accuracy Tracker

Analyzes sales forecast accuracy to help identify which reps are on track and which forecasts are reliable.

## Why I Built This

Sales ops teams always struggle with forecast accuracy. Reps might be optimistic or conservative, and it's hard to know who to trust. This tool helps by comparing what was forecasted vs what actually closed.

## What It Does

- Calculates accuracy by sales rep
- Shows accuracy by forecast category (best_case, commit, pipeline)
- Identifies top performers and biggest misses
- Generates summary reports

Pretty straightforward analysis but helpful for weekly forecast reviews.

## Setup

**Requirements:**
- Python 3.10 or 3.11
- Basic libraries (pandas, numpy)

**Installation:**
```bash
git clone https://github.com/priypate09/sales-forecast-tracker.git
cd sales-forecast-tracker

python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

## How to Use

First, generate some sample data to test with:
```bash
python generate_sample_data.py
```

Then run the analysis:
```bash
python main.py
```

You'll get output showing accuracy by rep, by category, and overall summary.

## Example Output
```
======================================================================
SALES FORECAST ACCURACY ANALYSIS
======================================================================

Accuracy by Sales Rep
----------------------------------------------------------------------
          rep_name  forecast_amount  actual_amount  accuracy_pct
   Charlie Martinez          3120000        2450000          78.5
    Alice Johnson            2450000        1680000          68.6

Accuracy by Forecast Category  
----------------------------------------------------------------------
     category  forecast_amount  actual_amount  accuracy_pct
    best_case          1850000        1560000          84.3
       commit          6340000        4120000          65.0
     pipeline          2050000         820000          40.0

Overall Summary
----------------------------------------------------------------------
Total Forecasted:    $10,240,000
Total Closed:        $ 6,500,000
Overall Accuracy:           63.5%
```

## Data Format

The tool expects two CSV files:

**Forecast data** should have:
- rep_name
- opportunity_id  
- amount
- forecast_category (best_case, commit, or pipeline)
- close_date
- snapshot_date

**Actual results** should have:
- opportunity_id (matching forecast)
- amount (actual closed)
- close_date
- status (won or lost)

## Project Structure
```
sales-forecast-tracker/
├── src/
│   ├── data_loader.py       # loads and validates CSV files
│   └── analyzer.py          # calculates accuracy metrics
├── data/
│   ├── sample_forecast.csv
│   └── sample_actuals.csv
├── main.py                  # runs the analysis
├── generate_sample_data.py  # creates test data
└── requirements.txt
```

## Use Cases

I built this for a few scenarios:
- Weekly forecast reviews to see who needs coaching
- Understanding which forecast categories are actually reliable
- Tracking if reps improve their accuracy over time
- Setting realistic quotas based on historical performance

## Possible Improvements

Some things I might add later:
- Trend analysis over multiple quarters
- Charts and visualizations
- Export to Excel
- Win rate analysis by deal size
- Maybe integrate with Salesforce API

## Notes

This is a personal project I built while learning more about sales analytics. The code isn't perfect but it gets the job done. Feel free to use or modify however you want.

## License

MIT