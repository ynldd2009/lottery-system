"""
Test suite for core modules: DataAnalyzer, PredictionEngine, and RecordManager.
"""

import sys
from pathlib import Path
import pandas as pd
import tempfile
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import ConfigManager
from src.core import DataAnalyzer, PredictionEngine, RecordManager
from src.data import DataHandler
from src.utils import PasswordGenerator


def test_config_manager():
    """Test configuration management."""
    print("Testing ConfigManager...")
    
    # Test default config
    config = ConfigManager()
    
    assert config.get('system.app_name') == 'Lottery Analysis System'
    assert config.get('prediction.min_data_points') == 10
    assert config.get('ui.window_width') == 1200
    
    # Test set and get
    config.set('test.value', 123)
    assert config.get('test.value') == 123
    
    print("✓ ConfigManager tests passed")


def test_data_handler():
    """Test data import/export functionality."""
    print("Testing DataHandler...")
    
    handler = DataHandler()
    
    # Generate sample data
    data = handler.create_sample_data(num_draws=50)
    
    assert len(data) == 50
    assert 'date' in data.columns
    assert 'numbers' in data.columns
    
    # Test CSV export/import
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    success = handler.export_csv(csv_path, data)
    assert success
    
    imported_data = handler.import_csv(csv_path)
    assert len(imported_data) == len(data)
    
    # Test JSON export/import
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        json_path = f.name
    
    success = handler.export_json(json_path, data)
    assert success
    
    imported_data = handler.import_json(json_path)
    assert len(imported_data) == len(data)
    
    print("✓ DataHandler tests passed")


def test_data_analyzer():
    """Test data analysis functionality."""
    print("Testing DataAnalyzer...")
    
    analyzer = DataAnalyzer()
    
    # Create test data
    test_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=20),
        'draw_number': range(1, 21),
        'numbers': [[1, 5, 12, 23, 34, 45] for _ in range(20)]
    })
    
    analyzer.load_data(test_data)
    
    # Test frequency analysis
    frequency = analyzer.get_frequency_analysis()
    assert len(frequency) > 0
    assert frequency[1] == 20  # Number 1 appears in all 20 draws
    
    # Test hot/cold numbers
    hot, cold = analyzer.get_hot_cold_numbers()
    assert len(hot) > 0
    
    # Test pattern analysis
    patterns = analyzer.get_pattern_analysis()
    assert 'odd_even_ratio' in patterns
    assert 'consecutive_numbers' in patterns
    
    # Test statistics summary
    stats = analyzer.get_statistics_summary()
    assert stats['total_draws'] == 20
    assert 'hot_numbers' in stats
    assert 'cold_numbers' in stats
    
    print("✓ DataAnalyzer tests passed")


def test_prediction_engine():
    """Test prediction functionality."""
    print("Testing PredictionEngine...")
    
    engine = PredictionEngine()
    
    # Create test data
    test_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30),
        'draw_number': range(1, 31),
        'numbers': [[i % 49 + 1, (i * 2) % 49 + 1, (i * 3) % 49 + 1, 
                    (i * 4) % 49 + 1, (i * 5) % 49 + 1, (i * 6) % 49 + 1] 
                   for i in range(30)]
    })
    
    engine.load_historical_data(test_data)
    
    # Test frequency prediction
    pred = engine.predict_by_frequency(count=6, number_range=(1, 49))
    assert len(pred) == 6
    assert all(1 <= n <= 49 for n in pred)
    
    # Test hot numbers prediction
    pred = engine.predict_by_hot_numbers(count=6, number_range=(1, 49))
    assert len(pred) == 6
    assert all(1 <= n <= 49 for n in pred)
    
    # Test pattern prediction
    pred = engine.predict_by_pattern(count=6, number_range=(1, 49))
    assert len(pred) == 6
    assert all(1 <= n <= 49 for n in pred)
    
    # Test combined prediction
    predictions = engine.predict_combined(count=6, number_range=(1, 49))
    assert 'ensemble' in predictions
    assert len(predictions['ensemble']) == 6
    
    # Test prediction with confidence
    result = engine.generate_prediction_with_confidence(count=6, number_range=(1, 49))
    assert 'predictions' in result
    assert 'confidence' in result
    assert 'recommended' in result
    assert 0 <= result['confidence'] <= 1
    
    print("✓ PredictionEngine tests passed")


def test_record_manager():
    """Test record management functionality."""
    print("Testing RecordManager...")
    
    # Create temporary storage
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        storage_path = f.name
    
    manager = RecordManager(storage_path)
    
    # Test add record
    record = {
        'type': 'prediction',
        'title': 'Test Prediction',
        'description': 'Test record',
        'data': {'numbers': [1, 2, 3, 4, 5, 6]}
    }
    
    record_id = manager.add_record(record)
    assert record_id is not None
    
    # Test get record
    retrieved = manager.get_record(record_id)
    assert retrieved is not None
    assert retrieved['title'] == 'Test Prediction'
    
    # Test update record
    success = manager.update_record(record_id, {'title': 'Updated Title'})
    assert success
    
    updated = manager.get_record(record_id)
    assert updated['title'] == 'Updated Title'
    
    # Test get all records
    all_records = manager.get_all_records()
    assert len(all_records) >= 1
    
    # Test search records
    results = manager.search_records('Updated')
    assert len(results) >= 1
    
    # Test export
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        export_path = f.name
    
    success = manager.export_to_json(export_path)
    assert success
    
    # Test share
    shared = manager.share_record(record_id, format='json')
    assert shared is not None
    assert 'Updated Title' in shared
    
    # Test remove record
    success = manager.remove_record(record_id)
    assert success
    
    removed = manager.get_record(record_id)
    assert removed is None
    
    print("✓ RecordManager tests passed")


def test_password_generator():
    """Test password generation."""
    print("Testing PasswordGenerator...")
    
    generator = PasswordGenerator()
    
    # Test single password
    password = generator.generate()
    assert len(password) == 16  # Default length
    assert any(c.isupper() for c in password)  # Has uppercase
    assert any(c.isdigit() for c in password)  # Has digits
    
    import string
    assert any(c in string.punctuation for c in password)  # Has special chars
    
    # Test custom length
    password = generator.generate(length=20)
    assert len(password) == 20
    
    # Test multiple passwords
    passwords = generator.generate_multiple(count=5)
    assert len(passwords) == 5
    assert len(set(passwords)) == 5  # All unique
    
    # Test minimum length handling
    short_password = generator.generate(length=2)
    assert len(short_password) >= 4  # Should be adjusted to minimum
    
    print("✓ PasswordGenerator tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n=== Running Lottery System Tests ===\n")
    
    try:
        test_config_manager()
        test_data_handler()
        test_data_analyzer()
        test_prediction_engine()
        test_record_manager()
        test_password_generator()
        
        print("\n=== All Tests Passed! ===\n")
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
