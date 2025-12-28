"""
Test suite for Chinese Welfare Lottery Types
Tests for 双色球, 快乐8, 七乐彩, 福彩3D
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.config.lottery_types import LotteryType, get_lottery_type, LOTTERY_GAMES
from src.core.prediction_engine import PredictionEngine


class TestWelfareLotteryTypes(unittest.TestCase):
    """Test cases for Chinese Welfare Lottery games."""
    
    def test_shuangseqiu_configuration(self):
        """Test 双色球 (Double Color Ball) configuration."""
        lottery = get_lottery_type("双色球")
        
        # Check basic properties
        self.assertEqual(lottery.game_type, "双色球")
        self.assertEqual(lottery.name_en, "Double Color Ball")
        self.assertEqual(lottery.config['category'], "welfare")
        
        # Check number configuration
        self.assertEqual(lottery.config['main_numbers']['count'], 6)
        self.assertEqual(lottery.config['main_numbers']['range'], (1, 33))
        self.assertEqual(lottery.config['bonus_numbers']['count'], 1)
        self.assertEqual(lottery.config['bonus_numbers']['range'], (1, 16))
        
        # Check total numbers
        self.assertEqual(lottery.get_number_count(), 7)
        
        # Check prize levels
        prize_levels = lottery.get_prize_structure()
        self.assertEqual(len(prize_levels), 6)
        self.assertEqual(prize_levels[0]['level'], "一等奖")
        self.assertEqual(prize_levels[0]['base_prize'], 5000000)
    
    def test_shuangseqiu_number_ranges(self):
        """Test 双色球 number ranges."""
        lottery = get_lottery_type("双色球")
        ranges = lottery.get_number_ranges()
        
        # Should have 7 ranges (6 red + 1 blue)
        self.assertEqual(len(ranges), 7)
        
        # First 6 should be red balls (1-33)
        for i in range(6):
            self.assertEqual(ranges[i], (1, 33))
        
        # Last one should be blue ball (1-16)
        self.assertEqual(ranges[6], (1, 16))
    
    def test_shuangseqiu_validation(self):
        """Test 双色球 number validation."""
        lottery = get_lottery_type("双色球")
        
        # Valid prediction
        valid_numbers = [3, 12, 18, 25, 28, 31, 8]
        self.assertTrue(lottery.validate_numbers(valid_numbers))
        
        # Invalid - blue ball out of range
        invalid_numbers = [3, 12, 18, 25, 28, 31, 20]
        self.assertFalse(lottery.validate_numbers(invalid_numbers))
        
        # Invalid - red ball out of range
        invalid_numbers2 = [3, 12, 18, 25, 28, 40, 8]
        self.assertFalse(lottery.validate_numbers(invalid_numbers2))
    
    def test_shuangseqiu_formatting(self):
        """Test 双色球 prediction formatting."""
        lottery = get_lottery_type("双色球")
        numbers = [3, 12, 18, 25, 28, 31, 8]
        formatted = lottery.format_prediction(numbers)
        
        self.assertIn("Red:", formatted)
        self.assertIn("Blue:", formatted)
        self.assertIn("[8]", formatted)
    
    def test_kuaile8_configuration(self):
        """Test 快乐8 (Happy 8) configuration."""
        lottery = get_lottery_type("快乐8")
        
        # Check basic properties
        self.assertEqual(lottery.game_type, "快乐8")
        self.assertEqual(lottery.name_en, "Happy 8")
        self.assertEqual(lottery.config['category'], "welfare")
        
        # Check number configuration
        self.assertEqual(lottery.config['main_numbers']['count'], 10)
        self.assertEqual(lottery.config['main_numbers']['range'], (1, 80))
        self.assertEqual(lottery.config.get('draw_count'), 20)
        
        # Check prize levels
        prize_levels = lottery.get_prize_structure()
        self.assertEqual(len(prize_levels), 7)
        self.assertEqual(prize_levels[0]['description'], "10 of 10")
    
    def test_kuaile8_number_ranges(self):
        """Test 快乐8 number ranges."""
        lottery = get_lottery_type("快乐8")
        ranges = lottery.get_number_ranges()
        
        # Should have 10 number positions
        self.assertEqual(len(ranges), 10)
        
        # All should be in range (1-80)
        for r in ranges:
            self.assertEqual(r, (1, 80))
    
    def test_qilecai_configuration(self):
        """Test 七乐彩 (7 Happy Lottery) configuration."""
        lottery = get_lottery_type("七乐彩")
        
        # Check basic properties
        self.assertEqual(lottery.game_type, "七乐彩")
        self.assertEqual(lottery.name_en, "7 Happy Lottery")
        self.assertEqual(lottery.config['category'], "welfare")
        
        # Check number configuration
        self.assertEqual(lottery.config['main_numbers']['count'], 7)
        self.assertEqual(lottery.config['main_numbers']['range'], (1, 30))
        self.assertEqual(lottery.config['bonus_numbers']['count'], 1)
        self.assertEqual(lottery.config['bonus_numbers']['range'], (1, 30))
        
        # Check total numbers
        self.assertEqual(lottery.get_number_count(), 8)
        
        # Check prize levels
        prize_levels = lottery.get_prize_structure()
        self.assertEqual(len(prize_levels), 7)
    
    def test_qilecai_formatting(self):
        """Test 七乐彩 prediction formatting."""
        lottery = get_lottery_type("七乐彩")
        numbers = [3, 8, 12, 18, 22, 25, 29, 15]
        formatted = lottery.format_prediction(numbers)
        
        self.assertIn("Main:", formatted)
        self.assertIn("Special:", formatted)
        self.assertIn("[15]", formatted)
    
    def test_fucai3d_configuration(self):
        """Test 福彩3D (Welfare 3D) configuration."""
        lottery = get_lottery_type("福彩3D")
        
        # Check basic properties
        self.assertEqual(lottery.game_type, "福彩3D")
        self.assertEqual(lottery.name_en, "Welfare 3D")
        self.assertEqual(lottery.config['category'], "welfare")
        
        # Check digit configuration
        self.assertEqual(lottery.config['digits']['count'], 3)
        self.assertEqual(lottery.config['digits']['range'], (0, 9))
        
        # Check play types
        self.assertIn('play_types', lottery.config)
        self.assertEqual(len(lottery.config['play_types']), 3)
        
        # Check prize levels
        prize_levels = lottery.get_prize_structure()
        self.assertEqual(len(prize_levels), 3)
    
    def test_fucai3d_number_ranges(self):
        """Test 福彩3D number ranges."""
        lottery = get_lottery_type("福彩3D")
        ranges = lottery.get_number_ranges()
        
        # Should have 3 digit positions
        self.assertEqual(len(ranges), 3)
        
        # All should be 0-9
        for r in ranges:
            self.assertEqual(r, (0, 9))
    
    def test_fucai3d_formatting(self):
        """Test 福彩3D prediction formatting."""
        lottery = get_lottery_type("福彩3D")
        numbers = [3, 7, 9]
        formatted = lottery.format_prediction(numbers)
        
        # Should be concatenated digits
        self.assertEqual(formatted, "379")
    
    def test_all_welfare_games_available(self):
        """Test that all welfare lottery games are available."""
        available_games = LotteryType.get_available_games()
        
        welfare_games = ["双色球", "快乐8", "七乐彩", "福彩3D"]
        for game in welfare_games:
            self.assertIn(game, available_games)
    
    def test_welfare_games_category(self):
        """Test that welfare games have correct category."""
        welfare_games = ["双色球", "快乐8", "七乐彩", "福彩3D"]
        
        for game in welfare_games:
            config = LotteryType.get_game_info(game)
            self.assertEqual(config.get('category'), 'welfare')


class TestWelfareLotteryPredictions(unittest.TestCase):
    """Test predictions for welfare lottery games."""
    
    def test_shuangseqiu_prediction(self):
        """Test prediction for 双色球."""
        # Generate sample data with correct ranges
        sample_data = []
        for i in range(30):
            # 6 red balls (1-33) + 1 blue ball (1-16)
            red_balls = [(i + j) % 33 + 1 for j in range(6)]
            blue_ball = [i % 16 + 1]
            draw = red_balls + blue_ball
            sample_data.append(draw)
        
        # Create prediction engine
        engine = PredictionEngine(lottery_type="双色球")
        engine.data = sample_data
        
        # Test prediction
        result = engine.predict_for_lottery_type()
        
        self.assertIn('recommended', result)
        self.assertIn('formatted', result)
        self.assertEqual(len(result['recommended']), 7)
        
        # Verify the prediction structure is correct
        # Note: The prediction engine generates numbers based on the data,
        # so we just verify we get the right count and format
        self.assertIn('Red:', result['formatted'])
        self.assertIn('Blue:', result['formatted'])
    
    def test_kuaile8_prediction(self):
        """Test prediction for 快乐8."""
        # Generate sample data
        sample_data = []
        for i in range(30):
            draw = list(range(1, 11))
            sample_data.append(draw)
        
        # Create prediction engine
        engine = PredictionEngine(lottery_type="快乐8")
        engine.data = sample_data
        
        # Test prediction
        result = engine.predict_for_lottery_type()
        
        self.assertIn('recommended', result)
        self.assertEqual(len(result['recommended']), 10)
        
        # Validate prediction
        lottery = get_lottery_type("快乐8")
        self.assertTrue(lottery.validate_numbers(result['recommended']))
    
    def test_qilecai_prediction(self):
        """Test prediction for 七乐彩."""
        # Generate sample data
        sample_data = []
        for i in range(30):
            draw = list(range(1, 9))
            sample_data.append(draw)
        
        # Create prediction engine
        engine = PredictionEngine(lottery_type="七乐彩")
        engine.data = sample_data
        
        # Test prediction
        result = engine.predict_for_lottery_type()
        
        self.assertIn('recommended', result)
        self.assertEqual(len(result['recommended']), 8)
        
        # Validate prediction
        lottery = get_lottery_type("七乐彩")
        self.assertTrue(lottery.validate_numbers(result['recommended']))
    
    def test_fucai3d_prediction(self):
        """Test prediction for 福彩3D."""
        # Generate sample data
        sample_data = []
        for i in range(30):
            draw = [i % 10, (i + 3) % 10, (i + 7) % 10]
            sample_data.append(draw)
        
        # Create prediction engine
        engine = PredictionEngine(lottery_type="福彩3D")
        engine.data = sample_data
        
        # Test prediction
        result = engine.predict_for_lottery_type()
        
        self.assertIn('recommended', result)
        self.assertEqual(len(result['recommended']), 3)
        
        # Validate prediction
        lottery = get_lottery_type("福彩3D")
        self.assertTrue(lottery.validate_numbers(result['recommended']))
        
        # Check formatting
        formatted = result['formatted']
        self.assertEqual(len(formatted), 3)
        self.assertTrue(formatted.isdigit())


class TestAllLotteryTypes(unittest.TestCase):
    """Test all lottery types together."""
    
    def test_total_lottery_count(self):
        """Test that we have all lottery types."""
        available_games = LotteryType.get_available_games()
        
        # Should have 9 games total:
        # Sports: 大乐透, 七星彩, 排列三, 排列五
        # Welfare: 双色球, 快乐8, 七乐彩, 福彩3D
        # General: 通用
        self.assertGreaterEqual(len(available_games), 9)
    
    def test_sports_and_welfare_categories(self):
        """Test that games are properly categorized."""
        sports_games = ["大乐透", "七星彩", "排列三", "排列五"]
        welfare_games = ["双色球", "快乐8", "七乐彩", "福彩3D"]
        
        for game in sports_games:
            config = LotteryType.get_game_info(game)
            self.assertEqual(config.get('category'), 'sports')
        
        for game in welfare_games:
            config = LotteryType.get_game_info(game)
            self.assertEqual(config.get('category'), 'welfare')
    
    def test_all_games_have_prize_levels(self):
        """Test that all games have prize structure."""
        available_games = LotteryType.get_available_games()
        
        for game in available_games:
            if game != "通用":  # General might not have prize levels
                lottery = get_lottery_type(game)
                prize_levels = lottery.get_prize_structure()
                self.assertGreater(len(prize_levels), 0, 
                                 f"{game} should have prize levels")


if __name__ == '__main__':
    print("Testing Chinese Welfare Lottery Types...")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
