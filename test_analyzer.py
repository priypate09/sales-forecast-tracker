"""
Basic tests for the analyzer functions
"""
import pandas as pd
from src.analyzer import calculate_accuracy, calculate_category_accuracy


def test_accuracy_basic():
    """Test basic accuracy calculation"""
    print("Testing accuracy calculation...")
    
    # Creating simple test data
    forecast = pd.DataFrame({
        'rep_name': ['Alice', 'Alice', 'Bob'],
        'opportunity_id': ['OPP-1', 'OPP-2', 'OPP-3'],
        'amount': [100000, 50000, 200000],
        'forecast_category': ['commit', 'commit', 'commit'],
        'close_date': ['2024-12-31'] * 3,
        'snapshot_date': ['2024-11-15'] * 3
    })
    
    actuals = pd.DataFrame({
        'opportunity_id': ['OPP-1', 'OPP-2', 'OPP-3'],
        'amount': [100000, 50000, 0],
        'close_date': ['2024-12-31'] * 3,
        'status': ['won', 'won', 'lost']
    })
    
    result = calculate_accuracy(forecast, actuals)
    
    # Checkin results
    alice = result[result['rep_name'] == 'Alice'].iloc[0]
    bob = result[result['rep_name'] == 'Bob'].iloc[0]
    
    # Alice should have 100% accuracy
    assert alice['accuracy_pct'] == 100.0, f"Expected 100%, got {alice['accuracy_pct']}"
    
    # Bob should have 0% accuracy  
    assert bob['accuracy_pct'] == 0.0, f"Expected 0%, got {bob['accuracy_pct']}"
    
    print("Basic accuracy test passed")


def test_category_accuracy():
    """Test category accuracy calculation"""
    print("Testing category accuracy...")
    
    forecast = pd.DataFrame({
        'rep_name': ['Alice'] * 3,
        'opportunity_id': ['OPP-1', 'OPP-2', 'OPP-3'],
        'amount': [100000, 100000, 100000],
        'forecast_category': ['best_case', 'commit', 'pipeline'],
        'close_date': ['2024-12-31'] * 3,
        'snapshot_date': ['2024-11-15'] * 3
    })
    
    actuals = pd.DataFrame({
        'opportunity_id': ['OPP-1', 'OPP-2', 'OPP-3'],
        'amount': [100000, 100000, 0],
        'close_date': ['2024-12-31'] * 3,
        'status': ['won', 'won', 'lost']
    })
    
    result = calculate_category_accuracy(forecast, actuals)
    
    # Should have all three categories
    assert len(result) == 3, f"Expected 3 categories, got {len(result)}"
    
    # Check pipeline has 0% accuracy
    pipeline = result[result['category'] == 'pipeline'].iloc[0]
    assert pipeline['accuracy_pct'] == 0.0, "Pipeline should be 0%"
    
    print("Category accuracy test passed")


def test_empty_data():
    """Test handling of empty datasets"""
    print("Testing empty data handling...")
    
    forecast = pd.DataFrame(columns=['rep_name', 'opportunity_id', 'amount', 
                                     'forecast_category', 'close_date', 'snapshot_date'])
    actuals = pd.DataFrame(columns=['opportunity_id', 'amount', 'close_date', 'status'])
    
    result = calculate_accuracy(forecast, actuals)
    
    # Empty input should return empty result
    assert len(result) == 0, "Empty data should return empty result"
    
    print("Empty data test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Tests - Sales Forecast Tracker")
    print("=" * 60)
    
    try:
        test_accuracy_basic()
        test_category_accuracy()
        test_empty_data()
        
        print()
        print("=" * 60)
        print("All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        
    except Exception as e:
        print(f"\nError running tests: {e}")