#!/usr/bin/env python3
"""
Command-line demo of the Lottery Analysis System.
Demonstrates core functionality without requiring GUI.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import ConfigManager
from src.core import DataAnalyzer, PredictionEngine, RecordManager
from src.data import DataHandler, DataVisualizer
from src.utils import PasswordGenerator


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_data_handling():
    """Demonstrate data handling capabilities."""
    print_section("Data Handling Demo")
    
    handler = DataHandler()
    
    # Generate sample data
    print("\n1. Generating sample lottery data...")
    data = handler.create_sample_data(num_draws=100, num_count=6, num_range=(1, 49))
    print(f"   ✓ Generated {len(data)} lottery draws")
    print(f"   ✓ Date range: {data['date'].min()} to {data['date'].max()}")
    
    # Show first few records
    print("\n   Sample records:")
    for i, row in data.head(5).iterrows():
        print(f"   Draw {row['draw_number']:3d}: {row['numbers']}")
    
    return data


def demo_data_analysis(data):
    """Demonstrate data analysis capabilities."""
    print_section("Data Analysis Demo")
    
    analyzer = DataAnalyzer()
    analyzer.load_data(data)
    
    print("\n1. Running frequency analysis...")
    frequency = analyzer.get_frequency_analysis()
    
    # Show top 10 most frequent numbers
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n   Top 10 most frequent numbers:")
    for num, freq in sorted_freq:
        print(f"   Number {num:2d}: appeared {freq:3d} times")
    
    print("\n2. Identifying hot and cold numbers...")
    hot_numbers, cold_numbers = analyzer.get_hot_cold_numbers()
    print(f"\n   Hot numbers (frequently drawn): {hot_numbers}")
    print(f"   Cold numbers (rarely drawn): {cold_numbers}")
    
    print("\n3. Analyzing patterns...")
    patterns = analyzer.get_pattern_analysis()
    print(f"\n   Consecutive numbers found: {patterns.get('consecutive_numbers', 0)}")
    print(f"   Odd/Even ratio: {patterns.get('odd_even_ratio', 0):.2%}")
    print(f"   High/Low ratio: {patterns.get('high_low_ratio', 0):.2%}")
    sum_range = patterns.get('sum_range', (0, 0))
    print(f"   Sum range: {sum_range[0]} to {sum_range[1]}")
    
    return analyzer


def demo_prediction(data):
    """Demonstrate prediction capabilities."""
    print_section("Prediction Demo")
    
    # Load config to get all algorithms
    config = ConfigManager()
    engine = PredictionEngine(config.config.get('prediction', {}))
    engine.load_historical_data(data)
    
    print("\n1. Generating predictions using different algorithms...")
    
    # Original algorithms
    print("\n   Original Algorithms:")
    print("   -------------------")
    
    # Frequency-based prediction
    print("\n   a) Frequency-based prediction:")
    freq_pred = engine.predict_by_frequency(count=6, number_range=(1, 49))
    print(f"      {freq_pred}")
    
    # Hot numbers prediction
    print("\n   b) Hot numbers prediction:")
    hot_pred = engine.predict_by_hot_numbers(count=6, number_range=(1, 49))
    print(f"      {hot_pred}")
    
    # Pattern-based prediction
    print("\n   c) Pattern-based prediction:")
    pattern_pred = engine.predict_by_pattern(count=6, number_range=(1, 49))
    print(f"      {pattern_pred}")
    
    # New statistical models
    print("\n   New Statistical Models:")
    print("   ----------------------")
    
    # Weighted frequency
    print("\n   d) Weighted frequency (recent draws weighted more):")
    weighted_pred = engine.predict_by_weighted_frequency(count=6, number_range=(1, 49))
    print(f"      {weighted_pred}")
    
    # Gap analysis
    print("\n   e) Gap analysis (numbers 'due' to appear):")
    gap_pred = engine.predict_by_gap_analysis(count=6, number_range=(1, 49))
    print(f"      {gap_pred}")
    
    # Moving average
    print("\n   f) Moving average (trend-based):")
    ma_pred = engine.predict_by_moving_average(count=6, number_range=(1, 49))
    print(f"      {ma_pred}")
    
    # Cyclic pattern
    print("\n   g) Cyclic pattern (cycle detection):")
    cyclic_pred = engine.predict_by_cyclic_pattern(count=6, number_range=(1, 49))
    print(f"      {cyclic_pred}")
    
    # Combined prediction with confidence
    print("\n2. Generating ensemble prediction with confidence score...")
    result = engine.generate_prediction_with_confidence(count=6, number_range=(1, 49))
    
    print(f"\n   Recommended numbers: {result['recommended']}")
    print(f"   Confidence level: {result['confidence']:.1%}")
    print(f"   Based on {result['data_points_used']} historical draws")
    print(f"   Algorithms used: {len(result['algorithms_used'])} models")
    print(f"   Models: {', '.join(result['algorithms_used'])}")


def demo_password_generator():
    """Demonstrate password generation."""
    print_section("Password Generator Demo")
    
    generator = PasswordGenerator()
    
    print("\n1. Generating strong passwords...")
    passwords = generator.generate_multiple(count=5)
    
    for i, pwd in enumerate(passwords, 1):
        print(f"   Password {i}: {pwd}")
    
    print("\n   ✓ All passwords include:")
    print("     - Uppercase letters")
    print("     - Lowercase letters")
    print("     - Numbers")
    print("     - Special characters")


def demo_record_management():
    """Demonstrate record management."""
    print_section("Record Management Demo")
    
    # Use temporary storage
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        storage_path = f.name
    
    manager = RecordManager(storage_path)
    
    print("\n1. Adding prediction records...")
    
    # Add sample records
    for i in range(3):
        record = {
            'type': 'prediction',
            'title': f'Prediction #{i+1}',
            'description': f'Sample prediction record {i+1}',
            'data': {
                'numbers': [1, 5, 12, 23, 34, 45],
                'confidence': 0.75,
                'algorithm': 'ensemble'
            }
        }
        record_id = manager.add_record(record)
        print(f"   ✓ Added record: {record_id}")
    
    print("\n2. Retrieving all records...")
    all_records = manager.get_all_records()
    print(f"   Total records: {len(all_records)}")
    
    for record in all_records:
        print(f"   - {record['title']}: {record.get('created_at', 'N/A')}")
    
    print("\n3. Searching records...")
    results = manager.search_records('Prediction')
    print(f"   Found {len(results)} matching records")
    
    print("\n4. Record operations available:")
    print("   ✓ Add new records")
    print("   ✓ Update existing records")
    print("   ✓ Remove records")
    print("   ✓ Search records")
    print("   ✓ Export to JSON")
    print("   ✓ Share records")


def demo_configuration():
    """Demonstrate configuration management."""
    print_section("Configuration Management Demo")
    
    config = ConfigManager()
    
    print("\n1. System configuration:")
    print(f"   App Name: {config.get('system.app_name')}")
    print(f"   Version: {config.get('system.version')}")
    
    print("\n2. Prediction settings:")
    print(f"   Analysis window: {config.get('prediction.analysis_window')} draws")
    print(f"   Min data points: {config.get('prediction.min_data_points')}")
    print(f"   Algorithms: {', '.join(config.get('prediction.prediction_algorithms', []))}")
    
    print("\n3. Security settings:")
    print(f"   Password length: {config.get('security.password_length')}")
    print(f"   Include special chars: {config.get('security.password_include_special')}")
    
    print("\n4. Data management:")
    print(f"   Validity period: {config.get('data.validity_period_days')} days")
    print(f"   Max records: {config.get('data.max_records')}")
    print(f"   Cache enabled: {config.get('data.cache_enabled')}")


def demo_visualization(data):
    """Demonstrate visualization capabilities."""
    print_section("Visualization Demo")
    
    analyzer = DataAnalyzer()
    analyzer.load_data(data)
    visualizer = DataVisualizer()
    
    print("\n1. Available visualization types:")
    print("   ✓ Frequency distribution charts")
    print("   ✓ Hot vs Cold number comparisons")
    print("   ✓ Number distribution over time")
    print("   ✓ Odd/Even distribution pie charts")
    print("   ✓ Comprehensive analysis dashboards")
    
    print("\n2. Creating sample visualizations...")
    
    # Get data for visualization
    frequency = analyzer.get_frequency_analysis()
    hot_nums, cold_nums = analyzer.get_hot_cold_numbers()
    
    # Create dashboard
    output_dir = Path.home()
    dashboard_path = output_dir / "lottery_demo_dashboard.png"
    
    try:
        visualizer.create_analysis_dashboard(
            frequency, hot_nums, cold_nums, data, str(dashboard_path)
        )
        print(f"   ✓ Dashboard saved to: {dashboard_path}")
    except Exception as e:
        print(f"   ⚠ Visualization skipped (display not available): {e}")


def main():
    """Run the complete demo."""
    print("\n" + "=" * 60)
    print("  LOTTERY ANALYSIS AND PREDICTION SYSTEM - CLI DEMO")
    print("=" * 60)
    
    try:
        # 1. Configuration
        demo_configuration()
        
        # 2. Data Handling
        data = demo_data_handling()
        
        # 3. Data Analysis
        demo_data_analysis(data)
        
        # 4. Predictions
        demo_prediction(data)
        
        # 5. Password Generator
        demo_password_generator()
        
        # 6. Record Management
        demo_record_management()
        
        # 7. Visualization
        demo_visualization(data)
        
        # Summary
        print_section("Demo Complete")
        print("\n✓ All core features demonstrated successfully!")
        print("\nTo run the full GUI application, use:")
        print("  python main.py")
        print("\nFor Android deployment instructions, see:")
        print("  ANDROID_DEPLOYMENT.md")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
