"""
Main script to run forecast accuracy analysis
"""
import sys
from src.data_loader import load_forecast_data, load_actual_results
from src.analyzer import calculate_accuracy, calculate_category_accuracy
from src.analyzer import get_top_performers, get_biggest_misses


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*70)


def print_section_header(title):
    """Print a section header"""
    print("\n" + "-"*70)
    print(title)
    print("-"*70)


def main():
    """Run the complete forecast accuracy analysis"""
    
    print_separator()
    print("SALES FORECAST ACCURACY ANALYSIS")
    print_separator()
    
    # Load data
    print("\nLoading data...")
    try:
        forecast = load_forecast_data('data/sample_forecast.csv')
        actuals = load_actual_results('data/sample_actuals.csv')
        print(f" Loaded {len(forecast)} forecast records")
        print(f" Loaded {len(actuals)} actual results")
    except FileNotFoundError as e:
        print(f"\n Error: Could not find data files.")
        print(f"   Please run 'python generate_sample_data.py' first.")
        return
    except Exception as e:
        print(f"\n Error loading data: {e}")
        return
    
    # Calculate accuracy by rep
    print_section_header("Accuracy by Sales Rep")
    rep_accuracy = calculate_accuracy(forecast, actuals)
    
    # Sort by accuracy for better readability
    rep_accuracy_sorted = rep_accuracy.sort_values('accuracy_pct', ascending=False)
    print(rep_accuracy_sorted.to_string(index=False))
    
    # Calculate accuracy by category
    print_section_header("Accuracy by Forecast Category")
    cat_accuracy = calculate_category_accuracy(forecast, actuals)
    cat_accuracy_sorted = cat_accuracy.sort_values('accuracy_pct', ascending=False)
    print(cat_accuracy_sorted.to_string(index=False))
    
    # Show top performers
    print_section_header("Top Performers (Most Accurate)")
    top_performers = get_top_performers(rep_accuracy, top_n=3)
    for idx, row in top_performers.iterrows():
        print(f"  {row['rep_name']:<20} {row['accuracy_pct']:>6.1f}%")
    
    # Show biggest misses
    print_section_header("Largest Forecast Errors")
    biggest_misses = get_biggest_misses(rep_accuracy, top_n=3)
    for idx, row in biggest_misses.iterrows():
        error = row['dollar_error']
        sign = "+" if error > 0 else ""
        print(f"  {row['rep_name']:<20} {sign}${error:>,.0f}")
    
    # Overall summary
    print_section_header("Overall Summary")
    total_forecast = forecast['amount'].sum()
    total_actual = actuals[actuals['status']=='won']['amount'].sum()
    overall_accuracy = (total_actual / total_forecast * 100)
    
    print(f"  Total Forecasted:    ${total_forecast:>12,.0f}")
    print(f"  Total Closed:        ${total_actual:>12,.0f}")
    print(f"  Overall Accuracy:    {overall_accuracy:>12.1f}%")
    print(f"  Dollar Variance:     ${total_actual - total_forecast:>12,.0f}")
    
    # Win rate
    win_rate = (actuals['status']=='won').sum() / len(actuals) * 100
    print(f"  Win Rate:            {win_rate:>12.1f}%")
    
    print_separator()
    print()


if __name__ == "__main__":
    main()