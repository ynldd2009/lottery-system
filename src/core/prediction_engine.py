"""
Prediction Engine Module
Generates lottery number predictions based on historical data analysis.
"""

import numpy as np
import random
from typing import List, Dict, Tuple, Optional
from collections import Counter
from .data_analyzer import DataAnalyzer


class PredictionEngine:
    """Generates predictions for lottery numbers using various algorithms."""
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize prediction engine with configuration.
        
        Args:
            config: Configuration dictionary.
        """
        self.config = config or {}
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
        
        if 'frequency' in self.algorithms:
            predictions['frequency'] = self.predict_by_frequency(count, number_range)
        
        if 'hot_cold' in self.algorithms:
            predictions['hot_cold'] = self.predict_by_hot_numbers(count, number_range)
        
        if 'pattern' in self.algorithms:
            predictions['pattern'] = self.predict_by_pattern(count, number_range)
        
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
