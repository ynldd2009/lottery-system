#!/usr/bin/env python3
"""
Test the refactored utility functions
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.time_utils import calculate_countdown
from src.utils.api_client import load_api_config
from src.utils.logger import setup_logger


def test_calculate_countdown():
    """Test the calculate_countdown function"""
    print("Testing calculate_countdown function...")
    
    # Test with a future time (should return countdown)
    countdown, is_urgent = calculate_countdown(23, 59)
    print(f"  Countdown to 23:59: {countdown}, Urgent: {is_urgent}")
    assert isinstance(countdown, str), "Countdown should be a string"
    assert isinstance(is_urgent, bool), "is_urgent should be a boolean"
    
    # Test with a past time (should return '已截止')
    countdown, is_urgent = calculate_countdown(0, 0)
    print(f"  Countdown to 00:00: {countdown}, Urgent: {is_urgent}")
    
    print("  ✓ calculate_countdown tests passed!")


def test_load_api_config():
    """Test the load_api_config function"""
    print("\nTesting load_api_config function...")
    
    # Create a logger
    logger = setup_logger('test')
    
    # Test with non-existent file
    result = load_api_config(Path('nonexistent.json'), logger)
    assert result is False, "Should return False for non-existent file"
    print("  ✓ Non-existent file test passed")
    
    # Test with example file if it exists
    example_path = Path(__file__).parent / 'api_config.json.example'
    if example_path.exists():
        result = load_api_config(example_path, logger)
        print(f"  Example file result: {result}")
    
    print("  ✓ load_api_config tests passed!")


def main():
    """Run all tests"""
    print("=" * 60)
    print("  Testing Refactored Utility Functions")
    print("=" * 60)
    
    test_calculate_countdown()
    test_load_api_config()
    
    print("\n" + "=" * 60)
    print("  All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
