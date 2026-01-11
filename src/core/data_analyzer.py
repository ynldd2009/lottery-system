"""
Data Analyzer Module
Provides statistical analysis and data processing for lottery data.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from collections import Counter
from datetime import datetime, timedelta


class DataAnalyzer:
    """Analyzes lottery data and generates statistics."""
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize data analyzer with configuration.
        
        Args:
            config: Configuration dictionary.
        """
        self.config = config or {}
        self.data = pd.DataFrame()
        self.statistics = {}
    
    def load_data(self, data: pd.DataFrame) -> None:
        """
        Load lottery data for analysis.
        
        Args:
            data: DataFrame containing lottery draw data.
        """
        self.data = data.copy()
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])
    
    def get_frequency_analysis(self, number_column: str = 'numbers') -> Dict[int, int]:
        """
        Analyze the frequency of each number appearing in draws.
        
        Args:
            number_column: Column name containing lottery numbers.
            
        Returns:
            Dictionary mapping number to frequency count.
        """
        if self.data.empty or number_column not in self.data.columns:
            return {}
        
        all_numbers = []
        for numbers in self.data[number_column]:
            if isinstance(numbers, (list, tuple)):
                all_numbers.extend(numbers)
            elif isinstance(numbers, str):
                # Parse string representation of numbers
                nums = [int(n.strip()) for n in numbers.split(',') if n.strip().isdigit()]
                all_numbers.extend(nums)
        
        return dict(Counter(all_numbers))
    
    def get_hot_cold_numbers(self, number_column: str = 'numbers', 
                            hot_threshold: float = 0.7, 
                            cold_threshold: float = 0.3) -> Tuple[List[int], List[int]]:
        """
        Identify hot (frequently drawn) and cold (rarely drawn) numbers.
        
        Args:
            number_column: Column name containing lottery numbers.
            hot_threshold: Percentile threshold for hot numbers (default: 70%).
            cold_threshold: Percentile threshold for cold numbers (default: 30%).
            
        Returns:
            Tuple of (hot_numbers, cold_numbers).
        """
        frequency = self.get_frequency_analysis(number_column)
        
        if not frequency:
            return [], []
        
        frequencies = list(frequency.values())
        hot_cutoff = np.percentile(frequencies, hot_threshold * 100)
        cold_cutoff = np.percentile(frequencies, cold_threshold * 100)
        
        hot_numbers = [num for num, freq in frequency.items() if freq >= hot_cutoff]
        cold_numbers = [num for num, freq in frequency.items() if freq <= cold_cutoff]
        
        return sorted(hot_numbers), sorted(cold_numbers)
    
    def get_pattern_analysis(self, number_column: str = 'numbers', 
                            window: int = 5) -> Dict[str, any]:
        """
        Analyze patterns in lottery draws.
        
        Args:
            number_column: Column name containing lottery numbers.
            window: Number of recent draws to analyze.
            
        Returns:
            Dictionary with pattern statistics.
        """
        if self.data.empty or len(self.data) < window:
            return {}
        
        recent_data = self.data.tail(window)
        patterns = {
            'consecutive_numbers': 0,
            'odd_even_ratio': 0.0,
            'high_low_ratio': 0.0,
            'sum_range': (0, 0)
        }
        
        all_draws = self._extract_draws_from_data(recent_data, number_column)
        
        if not all_draws:
            return patterns
        
        # Count consecutive numbers
        patterns['consecutive_numbers'] = self._count_consecutive_numbers(all_draws)
        
        # Calculate ratios
        all_nums = [num for draw in all_draws for num in draw]
        if all_nums:
            patterns['odd_even_ratio'] = self._calculate_odd_even_ratio(all_nums)
            patterns['high_low_ratio'] = self._calculate_high_low_ratio(all_nums)
            patterns['sum_range'] = self._calculate_sum_range(all_draws)
        
        return patterns
    
    def _extract_draws_from_data(self, data, number_column: str) -> List[List[int]]:
        """Extract and parse draw numbers from data."""
        all_draws = []
        for numbers in data[number_column]:
            if isinstance(numbers, (list, tuple)):
                all_draws.append(sorted(numbers))
            elif isinstance(numbers, str):
                nums = sorted([int(n.strip()) for n in numbers.split(',') if n.strip().isdigit()])
                all_draws.append(nums)
        return all_draws
    
    def _count_consecutive_numbers(self, draws: List[List[int]]) -> int:
        """Count consecutive numbers in draws."""
        consecutive_count = 0
        for draw in draws:
            for i in range(len(draw) - 1):
                if draw[i+1] - draw[i] == 1:
                    consecutive_count += 1
        return consecutive_count
    
    def _calculate_odd_even_ratio(self, numbers: List[int]) -> float:
        """Calculate ratio of odd numbers."""
        if not numbers:
            return 0.0
        odd_count = sum(1 for n in numbers if n % 2 == 1)
        return odd_count / len(numbers)
    
    def _calculate_high_low_ratio(self, numbers: List[int]) -> float:
        """Calculate ratio of high numbers (above midpoint)."""
        if not numbers:
            return 0.0
        max_num = max(numbers)
        mid_point = max_num / 2
        high_count = sum(1 for n in numbers if n > mid_point)
        return high_count / len(numbers)
    
    def _calculate_sum_range(self, draws: List[List[int]]) -> Tuple[int, int]:
        """Calculate min and max sum of draws."""
        if not draws:
            return (0, 0)
        draw_sums = [sum(draw) for draw in draws]
        return (min(draw_sums), max(draw_sums))
    
    def get_statistics_summary(self, number_column: str = 'numbers') -> Dict[str, any]:
        """
        Generate comprehensive statistics summary.
        
        Args:
            number_column: Column name containing lottery numbers.
            
        Returns:
            Dictionary with various statistics.
        """
        frequency = self.get_frequency_analysis(number_column)
        hot_nums, cold_nums = self.get_hot_cold_numbers(number_column)
        patterns = self.get_pattern_analysis(number_column)
        
        summary = {
            'total_draws': len(self.data),
            'frequency_distribution': frequency,
            'hot_numbers': hot_nums,
            'cold_numbers': cold_nums,
            'patterns': patterns,
            'most_common': sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10] if frequency else [],
            'least_common': sorted(frequency.items(), key=lambda x: x[1])[:10] if frequency else []
        }
        
        self.statistics = summary
        return summary
    
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Filter data by date range.
        
        Args:
            start_date: Start date for filtering.
            end_date: End date for filtering.
            
        Returns:
            Filtered DataFrame.
        """
        if 'date' not in self.data.columns:
            return self.data
        
        mask = (self.data['date'] >= start_date) & (self.data['date'] <= end_date)
        return self.data[mask]
