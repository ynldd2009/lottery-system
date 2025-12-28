"""
Test suite for lottery types support.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.lottery_types import LotteryType, get_lottery_type, LOTTERY_GAMES
from src.core import PredictionEngine
from src.data import DataHandler


def test_lottery_type_initialization():
    """Test lottery type initialization."""
    print("Testing lottery type initialization...")
    
    # Test each lottery type
    for game_type in ["大乐透", "七星彩", "排列三", "排列五", "通用"]:
        lottery = get_lottery_type(game_type)
        assert lottery.game_type == game_type
        assert lottery.name is not None
        print(f"  ✓ {game_type}: {lottery.name}")
    
    print("✓ Lottery type initialization test passed")


def test_daleto_config():
    """Test Da Le Tou (Super Lotto) configuration."""
    print("\nTesting 大乐透 (Super Lotto) configuration...")
    
    lottery = get_lottery_type("大乐透")
    
    # Check number counts
    assert lottery.get_number_count() == 7  # 5 main + 2 bonus
    
    # Check ranges
    ranges = lottery.get_number_ranges()
    assert len(ranges) == 7
    assert ranges[0] == (1, 35)  # Main numbers
    assert ranges[5] == (1, 12)  # Bonus numbers
    
    # Check validation
    valid_numbers = [1, 5, 10, 20, 35, 1, 12]
    assert lottery.validate_numbers(valid_numbers)
    
    invalid_numbers = [1, 5, 10, 20, 36, 1, 12]  # 36 > 35
    assert not lottery.validate_numbers(invalid_numbers)
    
    # Check formatting
    formatted = lottery.format_prediction(valid_numbers)
    assert "Main:" in formatted
    assert "Bonus:" in formatted
    
    print(f"  ✓ Number count: {lottery.get_number_count()}")
    print(f"  ✓ Ranges: {ranges[:3]}...")
    print(f"  ✓ Formatted: {formatted}")
    print("✓ 大乐透 configuration test passed")


def test_qixingcai_config():
    """Test Qi Xing Cai (7-Star) configuration."""
    print("\nTesting 七星彩 (7-Star Lottery) configuration...")
    
    lottery = get_lottery_type("七星彩")
    
    # Check digit count
    assert lottery.get_number_count() == 7
    
    # Check ranges (each digit 0-9)
    ranges = lottery.get_number_ranges()
    assert len(ranges) == 7
    assert all(r == (0, 9) for r in ranges)
    
    # Check validation
    valid_digits = [1, 2, 3, 4, 5, 6, 7]
    assert lottery.validate_numbers(valid_digits)
    
    invalid_digits = [1, 2, 3, 4, 5, 6, 10]  # 10 > 9
    assert not lottery.validate_numbers(invalid_digits)
    
    # Check formatting (should be digit string)
    formatted = lottery.format_prediction([1, 2, 3, 4, 5, 6, 7])
    assert formatted == "1234567"
    
    print(f"  ✓ Digit count: {lottery.get_number_count()}")
    print(f"  ✓ Formatted: {formatted}")
    print("✓ 七星彩 configuration test passed")


def test_pailie3_config():
    """Test Pai Lie San (Pick 3) configuration."""
    print("\nTesting 排列三 (Pick 3) configuration...")
    
    lottery = get_lottery_type("排列三")
    
    # Check digit count
    assert lottery.get_number_count() == 3
    
    # Check ranges
    ranges = lottery.get_number_ranges()
    assert len(ranges) == 3
    assert all(r == (0, 9) for r in ranges)
    
    # Check formatting
    formatted = lottery.format_prediction([1, 2, 3])
    assert formatted == "123"
    
    print(f"  ✓ Digit count: {lottery.get_number_count()}")
    print(f"  ✓ Formatted: {formatted}")
    print("✓ 排列三 configuration test passed")


def test_pailie5_config():
    """Test Pai Lie Wu (Pick 5) configuration."""
    print("\nTesting 排列五 (Pick 5) configuration...")
    
    lottery = get_lottery_type("排列五")
    
    # Check digit count
    assert lottery.get_number_count() == 5
    
    # Check ranges
    ranges = lottery.get_number_ranges()
    assert len(ranges) == 5
    assert all(r == (0, 9) for r in ranges)
    
    # Check formatting
    formatted = lottery.format_prediction([1, 2, 3, 4, 5])
    assert formatted == "12345"
    
    print(f"  ✓ Digit count: {lottery.get_number_count()}")
    print(f"  ✓ Formatted: {formatted}")
    print("✓ 排列五 configuration test passed")


def test_prediction_engine_with_lottery_types():
    """Test prediction engine with different lottery types."""
    print("\nTesting prediction engine with lottery types...")
    
    # Create test data
    handler = DataHandler()
    data = handler.create_sample_data(num_draws=50)
    
    # Test 大乐透
    print("\n  Testing 大乐透 predictions...")
    engine_daleto = PredictionEngine(lottery_type="大乐透")
    engine_daleto.load_historical_data(data)
    result = engine_daleto.predict_for_lottery_type()
    
    assert 'lottery_type' in result
    assert 'main_numbers' in result
    assert 'bonus_numbers' in result
    assert len(result['main_numbers']) == 5
    assert len(result['bonus_numbers']) == 2
    print(f"    ✓ Prediction: {result['formatted']}")
    
    # Test 七星彩
    print("\n  Testing 七星彩 predictions...")
    engine_qxc = PredictionEngine(lottery_type="七星彩")
    engine_qxc.load_historical_data(data)
    result = engine_qxc.predict_for_lottery_type()
    
    assert 'lottery_type' in result
    assert 'digits' in result
    assert len(result['digits']) == 7
    assert len(result['formatted']) == 7
    print(f"    ✓ Prediction: {result['formatted']}")
    
    # Test 排列三
    print("\n  Testing 排列三 predictions...")
    engine_pl3 = PredictionEngine(lottery_type="排列三")
    engine_pl3.load_historical_data(data)
    result = engine_pl3.predict_for_lottery_type()
    
    assert 'digits' in result
    assert len(result['digits']) == 3
    assert len(result['formatted']) == 3
    print(f"    ✓ Prediction: {result['formatted']}")
    
    # Test 排列五
    print("\n  Testing 排列五 predictions...")
    engine_pl5 = PredictionEngine(lottery_type="排列五")
    engine_pl5.load_historical_data(data)
    result = engine_pl5.predict_for_lottery_type()
    
    assert 'digits' in result
    assert len(result['digits']) == 5
    assert len(result['formatted']) == 5
    print(f"    ✓ Prediction: {result['formatted']}")
    
    print("\n✓ Prediction engine with lottery types test passed")


def test_available_games():
    """Test getting available games list."""
    print("\nTesting available games list...")
    
    games = LotteryType.get_available_games()
    assert len(games) == 5
    assert "大乐透" in games
    assert "七星彩" in games
    assert "排列三" in games
    assert "排列五" in games
    assert "通用" in games
    
    print(f"  ✓ Available games: {games}")
    print("✓ Available games test passed")


def run_all_tests():
    """Run all lottery types tests."""
    print("\n=== Testing Lottery Types Support ===\n")
    
    try:
        test_lottery_type_initialization()
        test_daleto_config()
        test_qixingcai_config()
        test_pailie3_config()
        test_pailie5_config()
        test_available_games()
        test_prediction_engine_with_lottery_types()
        
        print("\n=== All Lottery Types Tests Passed! ===\n")
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
