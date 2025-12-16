"""
Prediction Engine Module
Generates lottery number predictions based on historical data analysis.
Supports multiple lottery types including Chinese sports lottery games.
"""

import numpy as np
import random
from typing import List, Dict, Tuple, Optional
from collections import Counter
from .data_analyzer import DataAnalyzer
from ..config.lottery_types import LotteryType, get_lottery_type


class PredictionEngine:
    """Generates predictions for lottery numbers using various algorithms."""
    
    def __init__(self, config: Optional[dict] = None, lottery_type: str = "双色球"):
        """
        Initialize prediction engine with configuration.
        
        Args:
            config: Configuration dictionary.
            lottery_type: Type of lottery game (8 types: 大乐透, 七星彩, 排列三, 排列五, 双色球, 快乐8, 七乐彩, 福彩3D).
        """
        self.config = config or {}
        self.lottery_type = get_lottery_type(lottery_type)
        self.analyzer = DataAnalyzer(config)
        self.algorithms = self.config.get('prediction_algorithms', ['frequency', 'hot_cold', 'pattern'])
        self.confidence_threshold = self.config.get('confidence_threshold', 0.6)
    
    def load_historical_data(self, data) -> None:
        """
        Load historical lottery data for predictions.
        
        Args:
            data: DataFrame containing historical lottery draws.
        """
        self.analyzer.load_data(data)
    
    def predict_by_frequency(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> List[int]:
        """
        Predict numbers based on historical frequency analysis.
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            List of predicted numbers.
        """
        frequency = self.analyzer.get_frequency_analysis()
        
        if not frequency:
            # If no data, return random numbers
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Sort by frequency and select top numbers
        sorted_numbers = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        predicted = [num for num, _ in sorted_numbers[:count]]
        
        # If we don't have enough numbers, fill with random ones
        if len(predicted) < count:
            available = set(range(number_range[0], number_range[1] + 1)) - set(predicted)
            additional = random.sample(list(available), count - len(predicted))
            predicted.extend(additional)
        
        return sorted(predicted[:count])
    
    def predict_by_hot_numbers(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> List[int]:
        """
        Predict numbers based on hot (frequently drawn) numbers.
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            List of predicted numbers.
        """
        hot_numbers, _ = self.analyzer.get_hot_cold_numbers()
        
        if not hot_numbers:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Select from hot numbers
        if len(hot_numbers) >= count:
            predicted = random.sample(hot_numbers, count)
        else:
            predicted = hot_numbers.copy()
            available = set(range(number_range[0], number_range[1] + 1)) - set(predicted)
            additional = random.sample(list(available), count - len(predicted))
            predicted.extend(additional)
        
        return sorted(predicted)
    
    def predict_by_pattern(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> List[int]:
        """
        Predict numbers based on pattern analysis (balanced odd/even, high/low).
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            List of predicted numbers.
        """
        patterns = self.analyzer.get_pattern_analysis()
        
        predicted = []
        mid_point = (number_range[0] + number_range[1]) // 2
        
        # Try to maintain balanced odd/even ratio
        odd_count = count // 2
        even_count = count - odd_count
        
        # Get frequency for weighted random selection
        frequency = self.analyzer.get_frequency_analysis()
        
        all_numbers = list(range(number_range[0], number_range[1] + 1))
        
        # If we have frequency data, use weighted selection
        if frequency:
            weights = [frequency.get(n, 1) for n in all_numbers]
        else:
            weights = [1] * len(all_numbers)
        
        # Select odd numbers
        odd_numbers = [n for n in all_numbers if n % 2 == 1]
        odd_weights = [weights[all_numbers.index(n)] for n in odd_numbers]
        
        if len(odd_numbers) >= odd_count:
            selected_odd = random.choices(odd_numbers, weights=odd_weights, k=odd_count * 2)
            selected_odd = list(set(selected_odd))[:odd_count]
        else:
            selected_odd = odd_numbers
        
        predicted.extend(selected_odd)
        
        # Select even numbers
        even_numbers = [n for n in all_numbers if n % 2 == 0 and n not in predicted]
        even_weights = [weights[all_numbers.index(n)] for n in even_numbers]
        
        remaining = count - len(predicted)
        if len(even_numbers) >= remaining:
            selected_even = random.choices(even_numbers, weights=even_weights, k=remaining * 2)
            selected_even = list(set(selected_even))[:remaining]
        else:
            selected_even = even_numbers[:remaining]
        
        predicted.extend(selected_even)
        
        # Fill if needed
        if len(predicted) < count:
            available = set(all_numbers) - set(predicted)
            additional = random.sample(list(available), count - len(predicted))
            predicted.extend(additional)
        
        return sorted(predicted[:count])
    
    def predict_by_weighted_frequency(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> List[int]:
        """
        Predict numbers using weighted frequency (recent draws have more weight).
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            List of predicted numbers.
        """
        if self.analyzer.data.empty:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Calculate weighted frequency (more weight to recent draws)
        weighted_freq = {}
        total_draws = len(self.analyzer.data)
        
        for idx, row in self.analyzer.data.iterrows():
            nums = row.get('numbers', [])
            if isinstance(nums, (list, tuple)):
                # Weight decreases exponentially for older draws
                weight = np.exp(-(total_draws - idx) / (total_draws * 0.3))
                for num in nums:
                    weighted_freq[num] = weighted_freq.get(num, 0) + weight
        
        if not weighted_freq:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Sort by weighted frequency
        sorted_numbers = sorted(weighted_freq.items(), key=lambda x: x[1], reverse=True)
        predicted = [num for num, _ in sorted_numbers[:count]]
        
        # Fill if needed
        if len(predicted) < count:
            available = set(range(number_range[0], number_range[1] + 1)) - set(predicted)
            additional = random.sample(list(available), count - len(predicted))
            predicted.extend(additional)
        
        return sorted(predicted[:count])
    
    def predict_by_gap_analysis(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> List[int]:
        """
        Predict numbers based on gap analysis (numbers that are "due" to appear).
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            List of predicted numbers.
        """
        if self.analyzer.data.empty:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Calculate gap (draws since last appearance) for each number
        gaps = {}
        all_numbers = set(range(number_range[0], number_range[1] + 1))
        
        # Initialize gaps
        for num in all_numbers:
            gaps[num] = len(self.analyzer.data)  # Max gap initially
        
        # Calculate actual gaps from most recent draw backwards
        for idx in range(len(self.analyzer.data) - 1, -1, -1):
            row = self.analyzer.data.iloc[idx]
            nums = row.get('numbers', [])
            
            if isinstance(nums, (list, tuple)):
                for num in nums:
                    if num in gaps and gaps[num] == len(self.analyzer.data):
                        gaps[num] = len(self.analyzer.data) - idx - 1
        
        # Sort by gap (largest gaps = most "due")
        sorted_gaps = sorted(gaps.items(), key=lambda x: x[1], reverse=True)
        
        # Select numbers with largest gaps, but add some randomness
        top_due = [num for num, _ in sorted_gaps[:count * 2]]
        predicted = random.sample(top_due, min(count, len(top_due)))
        
        # Fill if needed
        if len(predicted) < count:
            available = set(all_numbers) - set(predicted)
            additional = random.sample(list(available), count - len(predicted))
            predicted.extend(additional)
        
        return sorted(predicted[:count])
    
    def predict_by_moving_average(self, count: int = 6, number_range: Tuple[int, int] = (1, 49), 
                                  window: int = 10) -> List[int]:
        """
        Predict numbers using moving average of recent draws.
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            window: Number of recent draws to consider.
            
        Returns:
            List of predicted numbers.
        """
        if self.analyzer.data.empty or len(self.analyzer.data) < window:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Calculate frequency in recent window
        recent_freq = {}
        recent_data = self.analyzer.data.tail(window)
        
        for idx, row in recent_data.iterrows():
            nums = row.get('numbers', [])
            if isinstance(nums, (list, tuple)):
                for num in nums:
                    recent_freq[num] = recent_freq.get(num, 0) + 1
        
        if not recent_freq:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Sort by recent frequency
        sorted_numbers = sorted(recent_freq.items(), key=lambda x: x[1], reverse=True)
        predicted = [num for num, _ in sorted_numbers[:count]]
        
        # Fill if needed
        if len(predicted) < count:
            available = set(range(number_range[0], number_range[1] + 1)) - set(predicted)
            additional = random.sample(list(available), count - len(predicted))
            predicted.extend(additional)
        
        return sorted(predicted[:count])
    
    def predict_by_cyclic_pattern(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> List[int]:
        """
        Predict numbers based on cyclic patterns in draws.
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            List of predicted numbers.
        """
        if self.analyzer.data.empty or len(self.analyzer.data) < 3:
            return sorted(random.sample(range(number_range[0], number_range[1] + 1), count))
        
        # Analyze appearance cycles for each number
        cycles = {}
        all_numbers = set(range(number_range[0], number_range[1] + 1))
        
        for num in all_numbers:
            appearances = []
            for idx, row in self.analyzer.data.iterrows():
                nums = row.get('numbers', [])
                if isinstance(nums, (list, tuple)) and num in nums:
                    appearances.append(idx)
            
            if len(appearances) >= 2:
                # Calculate average cycle length
                gaps = [appearances[i+1] - appearances[i] for i in range(len(appearances)-1)]
                avg_cycle = np.mean(gaps) if gaps else 0
                
                # Predict if current gap approaches average cycle
                last_appearance = appearances[-1]
                current_gap = len(self.analyzer.data) - last_appearance - 1
                
                # Score based on how close to expected cycle
                if avg_cycle > 0:
                    cycle_score = 1.0 - abs(current_gap - avg_cycle) / avg_cycle
                    cycles[num] = max(0, cycle_score)
                else:
                    cycles[num] = 0
            else:
                cycles[num] = random.random() * 0.5  # Low score for insufficient data
        
        # Sort by cycle score
        sorted_cycles = sorted(cycles.items(), key=lambda x: x[1], reverse=True)
        predicted = [num for num, _ in sorted_cycles[:count]]
        
        return sorted(predicted[:count])
    
    def predict_combined(self, count: int = 6, number_range: Tuple[int, int] = (1, 49)) -> Dict[str, List[int]]:
        """
        Generate predictions using multiple algorithms and combine them.
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            Dictionary with predictions from each algorithm.
        """
        predictions = {}
        
        # Original algorithms
        if 'frequency' in self.algorithms:
            predictions['frequency'] = self.predict_by_frequency(count, number_range)
        
        if 'hot_cold' in self.algorithms:
            predictions['hot_cold'] = self.predict_by_hot_numbers(count, number_range)
        
        if 'pattern' in self.algorithms:
            predictions['pattern'] = self.predict_by_pattern(count, number_range)
        
        # New statistical models
        if 'weighted_frequency' in self.algorithms:
            predictions['weighted_frequency'] = self.predict_by_weighted_frequency(count, number_range)
        
        if 'gap_analysis' in self.algorithms:
            predictions['gap_analysis'] = self.predict_by_gap_analysis(count, number_range)
        
        if 'moving_average' in self.algorithms:
            predictions['moving_average'] = self.predict_by_moving_average(count, number_range)
        
        if 'cyclic_pattern' in self.algorithms:
            predictions['cyclic_pattern'] = self.predict_by_cyclic_pattern(count, number_range)
        
        # Generate ensemble prediction by voting
        all_predicted = []
        for pred_list in predictions.values():
            all_predicted.extend(pred_list)
        
        # Count votes for each number
        votes = Counter(all_predicted)
        ensemble = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        ensemble_numbers = [num for num, _ in ensemble[:count]]
        
        # If we don't have enough, fill with highest voted remaining
        if len(ensemble_numbers) < count:
            available = set(range(number_range[0], number_range[1] + 1)) - set(ensemble_numbers)
            additional = random.sample(list(available), count - len(ensemble_numbers))
            ensemble_numbers.extend(additional)
        
        predictions['ensemble'] = sorted(ensemble_numbers[:count])
        
        return predictions
    
    def generate_prediction_with_confidence(self, count: int = 6, 
                                           number_range: Tuple[int, int] = (1, 49)) -> Dict[str, any]:
        """
        Generate prediction with confidence score.
        
        Args:
            count: Number of lottery numbers to predict.
            number_range: Range of valid lottery numbers (min, max).
            
        Returns:
            Dictionary with prediction and metadata.
        """
        predictions = self.predict_combined(count, number_range)
        
        # Calculate confidence based on data availability and consistency
        data_points = len(self.analyzer.data)
        min_data = self.config.get('min_data_points', 10)
        
        confidence = min(1.0, data_points / (min_data * 5))  # Scale confidence
        
        return {
            'predictions': predictions,
            'recommended': predictions.get('ensemble', predictions.get('frequency', [])),
            'confidence': confidence,
            'data_points_used': data_points,
            'algorithms_used': self.algorithms
        }
    
    def predict_for_lottery_type(self) -> Dict[str, any]:
        """
        Generate predictions specifically for the configured lottery type.
        
        Returns:
            Dictionary with lottery-type specific predictions.
        """
        ranges = self.lottery_type.get_number_ranges()
        
        if self.lottery_type.game_type == "大乐透":
            # Super Lotto: 5 main + 2 bonus
            main_pred = self.generate_prediction_with_confidence(count=5, number_range=(1, 35))
            bonus_pred = self.generate_prediction_with_confidence(count=2, number_range=(1, 12))
            
            return {
                'lottery_type': self.lottery_type.name,
                'main_numbers': main_pred['recommended'][:5],
                'bonus_numbers': bonus_pred['recommended'][:2],
                'formatted': self.lottery_type.format_prediction(
                    main_pred['recommended'][:5] + bonus_pred['recommended'][:2]
                ),
                'confidence': (main_pred['confidence'] + bonus_pred['confidence']) / 2,
                'algorithms_used': main_pred['algorithms_used']
            }
        
        elif self.lottery_type.game_type in ["七星彩", "排列三", "排列五"]:
            # Digit-based lotteries
            digit_count = self.lottery_type.get_number_count()
            digits = []
            
            # Predict each digit independently
            # For digit lotteries, we use a different approach since each position is 0-9
            for i in range(digit_count):
                # Use weighted random based on historical digit frequency in this position
                # For now, use simple random since we don't have digit-specific historical data
                digit = random.randint(0, 9)
                digits.append(digit)
            
            return {
                'lottery_type': self.lottery_type.name,
                'digits': digits,
                'formatted': self.lottery_type.format_prediction(digits),
                'confidence': 0.5,  # Lower confidence without digit-specific data
                'algorithms_used': ['random']  # Using random for now
            }
        
        else:
            # General lottery
            count = self.lottery_type.get_number_count()
            if ranges:
                number_range = ranges[0]
            else:
                number_range = (1, 49)
            
            result = self.generate_prediction_with_confidence(count=count, number_range=number_range)
            result['lottery_type'] = self.lottery_type.name
            result['formatted'] = self.lottery_type.format_prediction(result['recommended'])
            
            return result
