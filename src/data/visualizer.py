"""
Data Visualizer Module
Creates charts and visualizations for lottery data analysis.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for cross-platform support
import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, List
from pathlib import Path


class DataVisualizer:
    """Creates visualizations for lottery data and statistics."""
    
    def __init__(self, style: str = 'default', logger: Optional[logging.Logger] = None):
        """
        Initialize data visualizer.
        
        Args:
            style: Matplotlib style to use.
            logger: Optional logger instance. If None, creates a default logger.
        """
        self.style = style
        self.logger = logger or logging.getLogger(__name__)
        
        try:
            if style != 'default':
                plt.style.use(style)
        except Exception as e:
            self.logger.warning(f"Failed to set matplotlib style '{style}': {e}")
    
    def plot_frequency_chart(self, frequency_data: Dict[int, int], 
                            title: str = "Number Frequency Analysis",
                            save_path: Optional[str] = None) -> str:
        """
        Create a bar chart showing frequency of each number.
        
        Args:
            frequency_data: Dictionary mapping number to frequency.
            title: Chart title.
            save_path: Optional path to save the chart image.
            
        Returns:
            Path to saved chart or empty string if not saved.
            
        Raises:
            ValueError: If frequency_data is empty or invalid.
        """
        if not frequency_data:
            raise ValueError("Frequency data cannot be empty")
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            numbers = sorted(frequency_data.keys())
            frequencies = [frequency_data[n] for n in numbers]
            
            ax.bar(numbers, frequencies, color='steelblue', alpha=0.7)
            ax.set_xlabel('Number', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
                plt.close()
                self.logger.info(f"Frequency chart saved to {save_path}")
                return save_path
            
            plt.close()
            return ""
        except Exception as e:
            self.logger.error(f"Error creating frequency chart: {e}", exc_info=True)
            plt.close('all')
            return ""
    
    def plot_hot_cold_numbers(self, hot_numbers: List[int], cold_numbers: List[int],
                             title: str = "Hot vs Cold Numbers",
                             save_path: Optional[str] = None) -> str:
        """
        Create visualization comparing hot and cold numbers.
        
        Args:
            hot_numbers: List of hot (frequently drawn) numbers.
            cold_numbers: List of cold (rarely drawn) numbers.
            title: Chart title.
            save_path: Optional path to save the chart image.
            
        Returns:
            Path to saved chart or empty string if not saved.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Hot numbers
        if hot_numbers:
            ax1.bar(range(len(hot_numbers)), [1] * len(hot_numbers), 
                   tick_label=hot_numbers, color='red', alpha=0.7)
            ax1.set_title('Hot Numbers', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Number', fontsize=10)
            ax1.set_ylabel('Status', fontsize=10)
        
        # Cold numbers
        if cold_numbers:
            ax2.bar(range(len(cold_numbers)), [1] * len(cold_numbers), 
                   tick_label=cold_numbers, color='blue', alpha=0.7)
            ax2.set_title('Cold Numbers', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Number', fontsize=10)
            ax2.set_ylabel('Status', fontsize=10)
        
        fig.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            return save_path
        
        plt.close()
        return ""
    
    def plot_number_distribution(self, data: pd.DataFrame, 
                                number_column: str = 'numbers',
                                title: str = "Number Distribution Over Time",
                                save_path: Optional[str] = None) -> str:
        """
        Create a scatter plot showing number distribution over time.
        
        Args:
            data: DataFrame with lottery data.
            number_column: Column containing lottery numbers.
            title: Chart title.
            save_path: Optional path to save the chart image.
            
        Returns:
            Path to saved chart or empty string if not saved.
        """
        if data.empty:
            return ""
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Extract all numbers with their draw indices
        draw_indices = []
        numbers = []
        
        for idx, row in data.iterrows():
            nums = row[number_column]
            if isinstance(nums, (list, tuple)):
                for num in nums:
                    draw_indices.append(idx)
                    numbers.append(num)
        
        ax.scatter(draw_indices, numbers, alpha=0.5, c=numbers, cmap='viridis')
        ax.set_xlabel('Draw Index', fontsize=12)
        ax.set_ylabel('Number', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        plt.colorbar(ax.collections[0], ax=ax, label='Number Value')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            return save_path
        
        plt.close()
        return ""
    
    def plot_odd_even_distribution(self, data: pd.DataFrame,
                                   number_column: str = 'numbers',
                                   title: str = "Odd vs Even Distribution",
                                   save_path: Optional[str] = None) -> str:
        """
        Create a pie chart showing odd vs even number distribution.
        
        Args:
            data: DataFrame with lottery data.
            number_column: Column containing lottery numbers.
            title: Chart title.
            save_path: Optional path to save the chart image.
            
        Returns:
            Path to saved chart or empty string if not saved.
        """
        if data.empty:
            return ""
        
        odd_count = 0
        even_count = 0
        
        for idx, row in data.iterrows():
            nums = row[number_column]
            if isinstance(nums, (list, tuple)):
                for num in nums:
                    if num % 2 == 0:
                        even_count += 1
                    else:
                        odd_count += 1
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        sizes = [odd_count, even_count]
        labels = [f'Odd ({odd_count})', f'Even ({even_count})']
        colors = ['#ff9999', '#66b3ff']
        explode = (0.05, 0.05)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            return save_path
        
        plt.close()
        return ""
    
    def plot_prediction_comparison(self, predictions: Dict[str, List[int]],
                                  title: str = "Prediction Comparison",
                                  save_path: Optional[str] = None) -> str:
        """
        Create a visualization comparing different prediction algorithms.
        
        Args:
            predictions: Dictionary mapping algorithm name to predicted numbers.
            title: Chart title.
            save_path: Optional path to save the chart image.
            
        Returns:
            Path to saved chart or empty string if not saved.
        """
        if not predictions:
            return ""
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        algorithms = list(predictions.keys())
        num_algorithms = len(algorithms)
        
        for i, (algo, numbers) in enumerate(predictions.items()):
            y_positions = [i] * len(numbers)
            ax.scatter(numbers, y_positions, s=100, alpha=0.7, label=algo)
        
        ax.set_yticks(range(num_algorithms))
        ax.set_yticklabels(algorithms)
        ax.set_xlabel('Predicted Numbers', fontsize=12)
        ax.set_ylabel('Algorithm', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            return save_path
        
        plt.close()
        return ""
    
    def create_analysis_dashboard(self, frequency_data: Dict[int, int],
                                 hot_numbers: List[int],
                                 cold_numbers: List[int],
                                 data: pd.DataFrame,
                                 save_path: str) -> str:
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            frequency_data: Number frequency dictionary.
            hot_numbers: List of hot numbers.
            cold_numbers: List of cold numbers.
            data: DataFrame with lottery data.
            save_path: Path to save the dashboard image.
            
        Returns:
            Path to saved dashboard.
        """
        fig = plt.figure(figsize=(16, 10))
        
        # Frequency chart
        ax1 = plt.subplot(2, 2, 1)
        if frequency_data:
            numbers = sorted(frequency_data.keys())
            frequencies = [frequency_data[n] for n in numbers]
            ax1.bar(numbers, frequencies, color='steelblue', alpha=0.7)
            ax1.set_title('Number Frequency', fontweight='bold')
            ax1.set_xlabel('Number')
            ax1.set_ylabel('Frequency')
            ax1.grid(axis='y', alpha=0.3)
        
        # Hot vs Cold
        ax2 = plt.subplot(2, 2, 2)
        if hot_numbers or cold_numbers:
            categories = []
            values = []
            colors = []
            
            if hot_numbers:
                categories.extend([f'Hot ({len(hot_numbers)})'])
                values.extend([len(hot_numbers)])
                colors.extend(['red'])
            
            if cold_numbers:
                categories.extend([f'Cold ({len(cold_numbers)})'])
                values.extend([len(cold_numbers)])
                colors.extend(['blue'])
            
            ax2.bar(categories, values, color=colors, alpha=0.7)
            ax2.set_title('Hot vs Cold Numbers', fontweight='bold')
            ax2.set_ylabel('Count')
        
        # Odd/Even distribution
        ax3 = plt.subplot(2, 2, 3)
        if not data.empty:
            odd_count = 0
            even_count = 0
            
            for idx, row in data.iterrows():
                nums = row.get('numbers', [])
                if isinstance(nums, (list, tuple)):
                    for num in nums:
                        if num % 2 == 0:
                            even_count += 1
                        else:
                            odd_count += 1
            
            if odd_count > 0 or even_count > 0:
                ax3.pie([odd_count, even_count], labels=['Odd', 'Even'],
                       autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
                ax3.set_title('Odd/Even Distribution', fontweight='bold')
        
        # Recent trends
        ax4 = plt.subplot(2, 2, 4)
        if not data.empty and len(data) > 0:
            recent_count = min(20, len(data))
            recent_data = data.tail(recent_count)
            
            draw_nums = list(range(len(recent_data)))
            # Calculate average number per draw
            avg_numbers = []
            for idx, row in recent_data.iterrows():
                nums = row.get('numbers', [])
                if isinstance(nums, (list, tuple)) and len(nums) > 0:
                    avg_numbers.append(sum(nums) / len(nums))
                else:
                    avg_numbers.append(0)
            
            ax4.plot(draw_nums, avg_numbers, marker='o', linestyle='-', color='green')
            ax4.set_title('Recent Draw Trends (Avg Number)', fontweight='bold')
            ax4.set_xlabel('Recent Draws')
            ax4.set_ylabel('Average Number')
            ax4.grid(alpha=0.3)
        
        fig.suptitle('Lottery Analysis Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return save_path
