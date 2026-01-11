"""
Data Handler Module
Handles importing and exporting lottery data in various formats (CSV, JSON, Excel).
"""

import pandas as pd
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime


class DataHandler:
    """Handles data import/export operations for lottery data."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize data handler.
        
        Args:
            logger: Optional logger instance. If None, creates a default logger.
        """
        self.data = pd.DataFrame()
        self.logger = logger or logging.getLogger(__name__)
    
    def import_csv(self, filepath: str, date_column: str = 'date', 
                   number_column: str = 'numbers') -> pd.DataFrame:
        """
        Import lottery data from CSV file.
        
        Args:
            filepath: Path to CSV file.
            date_column: Name of the date column.
            number_column: Name of the numbers column.
            
        Returns:
            DataFrame with imported data.
        """
        try:
            df = pd.read_csv(filepath)
            
            # Parse date column if it exists
            if date_column in df.columns:
                df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            
            # Parse numbers column if it's a string
            if number_column in df.columns:
                df[number_column] = df[number_column].apply(self._parse_numbers)
            
            self.data = df
            return df
        except FileNotFoundError as e:
            self.logger.error(f"CSV file not found: {filepath}")
            return pd.DataFrame()
        except pd.errors.EmptyDataError as e:
            self.logger.error(f"CSV file is empty: {filepath}")
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error importing CSV from {filepath}: {e}", exc_info=True)
            return pd.DataFrame()
    
    def import_json(self, filepath: str) -> pd.DataFrame:
        """
        Import lottery data from JSON file.
        
        Args:
            filepath: Path to JSON file.
            
        Returns:
            DataFrame with imported data.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            df = pd.DataFrame(data)
            
            # Parse date column if it exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Parse numbers column if it's a string
            if 'numbers' in df.columns:
                df['numbers'] = df['numbers'].apply(self._parse_numbers)
            
            self.data = df
            return df
        except FileNotFoundError:
            self.logger.error(f"JSON file not found: {filepath}")
            return pd.DataFrame()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {filepath}: {e}")
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error importing JSON from {filepath}: {e}", exc_info=True)
            return pd.DataFrame()
    
    def import_excel(self, filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        """
        Import lottery data from Excel file.
        
        Args:
            filepath: Path to Excel file.
            sheet_name: Sheet name or index to read.
            
        Returns:
            DataFrame with imported data.
        """
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            
            # Parse date column if it exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Parse numbers column if it's a string
            if 'numbers' in df.columns:
                df['numbers'] = df['numbers'].apply(self._parse_numbers)
            
            self.data = df
            return df
        except FileNotFoundError:
            self.logger.error(f"Excel file not found: {filepath}")
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error importing Excel from {filepath}: {e}", exc_info=True)
            return pd.DataFrame()
    
    def export_csv(self, filepath: str, data: Optional[pd.DataFrame] = None, 
                   include_index: bool = False) -> bool:
        """
        Export data to CSV file.
        
        Args:
            filepath: Path to save CSV file.
            data: DataFrame to export. If None, uses internal data.
            include_index: Whether to include row index in export.
            
        Returns:
            True if export successful, False otherwise.
        """
        try:
            df = data if data is not None else self.data
            
            if df.empty:
                print("No data to export")
                return False
            
            # Convert lists to strings for CSV export
            df_export = df.copy()
            for col in df_export.columns:
                if df_export[col].apply(lambda x: isinstance(x, (list, tuple))).any():
                    df_export[col] = df_export[col].apply(lambda x: ','.join(map(str, x)) if isinstance(x, (list, tuple)) else x)
            
            df_export.to_csv(filepath, index=include_index)
            self.logger.info(f"Successfully exported data to CSV: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting CSV to {filepath}: {e}", exc_info=True)
            return False
    
    def export_json(self, filepath: str, data: Optional[pd.DataFrame] = None, 
                    orient: str = 'records') -> bool:
        """
        Export data to JSON file.
        
        Args:
            filepath: Path to save JSON file.
            data: DataFrame to export. If None, uses internal data.
            orient: JSON orientation ('records', 'index', 'columns').
            
        Returns:
            True if export successful, False otherwise.
        """
        try:
            df = data if data is not None else self.data
            
            if df.empty:
                self.logger.warning("No data to export")
                return False
            
            # Convert datetime to string for JSON serialization
            df_export = df.copy()
            for col in df_export.columns:
                if pd.api.types.is_datetime64_any_dtype(df_export[col]):
                    df_export[col] = df_export[col].dt.strftime('%Y-%m-%d')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(df_export.to_dict(orient=orient), f, indent=2)
            
            self.logger.info(f"Successfully exported data to JSON: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting JSON to {filepath}: {e}", exc_info=True)
            return False
    
    def export_excel(self, filepath: str, data: Optional[pd.DataFrame] = None, 
                     sheet_name: str = 'Lottery Data') -> bool:
        """
        Export data to Excel file.
        
        Args:
            filepath: Path to save Excel file.
            data: DataFrame to export. If None, uses internal data.
            sheet_name: Name of the Excel sheet.
            
        Returns:
            True if export successful, False otherwise.
        """
        try:
            df = data if data is not None else self.data
            
            if df.empty:
                self.logger.warning("No data to export")
                return False
            
            # Convert lists to strings for Excel export
            df_export = df.copy()
            for col in df_export.columns:
                if df_export[col].apply(lambda x: isinstance(x, (list, tuple))).any():
                    df_export[col] = df_export[col].apply(lambda x: ','.join(map(str, x)) if isinstance(x, (list, tuple)) else x)
            
            df_export.to_excel(filepath, sheet_name=sheet_name, index=False)
            self.logger.info(f"Successfully exported data to Excel: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting Excel to {filepath}: {e}", exc_info=True)
            return False
    
    def _parse_numbers(self, value):
        """
        Parse lottery numbers from various formats.
        
        Args:
            value: Input value (string, list, or tuple).
            
        Returns:
            List of integers.
        """
        if isinstance(value, (list, tuple)):
            return list(value)
        elif isinstance(value, str):
            # Try to parse comma-separated numbers
            try:
                return [int(n.strip()) for n in value.split(',') if n.strip().isdigit()]
            except:
                return []
        else:
            return []
    
    def create_sample_data(self, num_draws: int = 100, 
                          num_count: int = 6, 
                          num_range: tuple = (1, 49)) -> pd.DataFrame:
        """
        Create sample lottery data for testing and demonstration.
        
        Args:
            num_draws: Number of lottery draws to generate.
            num_count: Number of numbers per draw.
            num_range: Range of lottery numbers (min, max).
            
        Returns:
            DataFrame with sample lottery data.
        """
        import random
        
        data = []
        start_date = pd.Timestamp.now() - pd.Timedelta(days=num_draws)
        
        for i in range(num_draws):
            draw_date = start_date + pd.Timedelta(days=i)
            numbers = sorted(random.sample(range(num_range[0], num_range[1] + 1), num_count))
            
            data.append({
                'date': draw_date,
                'draw_number': i + 1,
                'numbers': numbers
            })
        
        self.data = pd.DataFrame(data)
        return self.data
