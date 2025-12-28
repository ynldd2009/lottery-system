"""
Test suite for new statistical prediction models.
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import PredictionEngine
from src.data import DataHandler


def test_weighted_frequency_prediction():
    """Test weighted frequency prediction model."""
    print("Testing weighted frequency prediction...")
    
    # Create test data
    handler = DataHandler()
    data = handler.create_sample_data(num_draws=50)
    
    # Initialize engine with new algorithm
    config = {'prediction_algorithms': ['weighted_frequency']}
    engine = PredictionEngine(config)
    engine.load_historical_data(data)
    
    # Generate prediction
    prediction = engine.predict_by_weighted_frequency(count=6, number_range=(1, 49))
    
    assert len(prediction) == 6
    assert all(1 <= n <= 49 for n in prediction)
    assert len(set(prediction)) == 6  # All unique
    
    print("✓ Weighted frequency prediction test passed")


def test_gap_analysis_prediction():
    """Test gap analysis prediction model."""
    print("Testing gap analysis prediction...")
    
    handler = DataHandler()
    data = handler.create_sample_data(num_draws=50)
    
    config = {'prediction_algorithms': ['gap_analysis']}
    engine = PredictionEngine(config)
    engine.load_historical_data(data)
    
    prediction = engine.predict_by_gap_analysis(count=6, number_range=(1, 49))
    
    assert len(prediction) == 6
    assert all(1 <= n <= 49 for n in prediction)
    assert len(set(prediction)) == 6
    
    print("✓ Gap analysis prediction test passed")


def test_moving_average_prediction():
    """Test moving average prediction model."""
    print("Testing moving average prediction...")
    
    handler = DataHandler()
    data = handler.create_sample_data(num_draws=50)
    
    config = {'prediction_algorithms': ['moving_average']}
    engine = PredictionEngine(config)
    engine.load_historical_data(data)
    
    prediction = engine.predict_by_moving_average(count=6, number_range=(1, 49), window=10)
    
    assert len(prediction) == 6
    assert all(1 <= n <= 49 for n in prediction)
    assert len(set(prediction)) == 6
    
    print("✓ Moving average prediction test passed")


def test_cyclic_pattern_prediction():
    """Test cyclic pattern prediction model."""
    print("Testing cyclic pattern prediction...")
    
    handler = DataHandler()
    data = handler.create_sample_data(num_draws=50)
    
    config = {'prediction_algorithms': ['cyclic_pattern']}
    engine = PredictionEngine(config)
    engine.load_historical_data(data)
    
    prediction = engine.predict_by_cyclic_pattern(count=6, number_range=(1, 49))
    
    assert len(prediction) == 6
    assert all(1 <= n <= 49 for n in prediction)
    assert len(set(prediction)) == 6
    
    print("✓ Cyclic pattern prediction test passed")


def test_combined_with_new_models():
    """Test combined prediction with all new models."""
    print("Testing combined prediction with new models...")
    
    handler = DataHandler()
    data = handler.create_sample_data(num_draws=50)
    
    # Test with all algorithms
    config = {
        'prediction_algorithms': [
            'frequency', 'hot_cold', 'pattern',
            'weighted_frequency', 'gap_analysis', 'moving_average', 'cyclic_pattern'
        ]
    }
    engine = PredictionEngine(config)
    engine.load_historical_data(data)
    
    result = engine.generate_prediction_with_confidence(count=6, number_range=(1, 49))
    
    assert 'predictions' in result
    assert 'ensemble' in result['predictions']
    assert 'weighted_frequency' in result['predictions']
    assert 'gap_analysis' in result['predictions']
    assert 'moving_average' in result['predictions']
    assert 'cyclic_pattern' in result['predictions']
    
    # Check ensemble prediction
    ensemble = result['predictions']['ensemble']
    assert len(ensemble) == 6
    assert all(1 <= n <= 49 for n in ensemble)
    
    print("✓ Combined prediction with new models test passed")


def test_edge_cases():
    """Test edge cases for new models."""
    print("Testing edge cases...")
    
    handler = DataHandler()
    
    # Test with minimal data
    data_small = handler.create_sample_data(num_draws=3)
    
    config = {
        'prediction_algorithms': ['weighted_frequency', 'gap_analysis', 'moving_average', 'cyclic_pattern']
    }
    engine = PredictionEngine(config)
    engine.load_historical_data(data_small)
    
    # Should still generate valid predictions even with minimal data
    result = engine.generate_prediction_with_confidence(count=6, number_range=(1, 49))
    
    assert 'predictions' in result
    for algo, prediction in result['predictions'].items():
        if algo != 'ensemble':  # Skip ensemble as it depends on others
            assert len(prediction) == 6
            assert all(1 <= n <= 49 for n in prediction)
    
    print("✓ Edge cases test passed")


def run_all_tests():
    """Run all tests for new statistical models."""
    print("\n=== Testing New Statistical Models ===\n")
    
    try:
        test_weighted_frequency_prediction()
        test_gap_analysis_prediction()
        test_moving_average_prediction()
        test_cyclic_pattern_prediction()
        test_combined_with_new_models()
        test_edge_cases()
        
        print("\n=== All New Model Tests Passed! ===\n")
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
