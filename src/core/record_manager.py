"""
Record Manager Module
Manages lottery prediction records (add, edit, remove, share).
"""

import json
import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class RecordManager:
    """Manages lottery prediction and analysis records."""
    
    def __init__(self, storage_path: str = None, logger: Optional[logging.Logger] = None):
        """
        Initialize record manager.
        
        Args:
            storage_path: Path to store records. If None, uses default.
            logger: Optional logger instance. If None, creates a default logger.
        """
        if storage_path is None:
            storage_path = Path.home() / ".lottery_system" / "records.json"
        
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logger or logging.getLogger(__name__)
        
        self.records: List[Dict] = []
        self.load_records()
    
    def load_records(self) -> None:
        """Load records from storage."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
                self.logger.info(f"Loaded {len(self.records)} records from {self.storage_path}")
            else:
                self.records = []
                self.logger.info("No existing records file found, starting with empty records")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in records file: {e}")
            self.records = []
        except Exception as e:
            self.logger.error(f"Error loading records: {e}", exc_info=True)
            self.records = []
    
    def save_records(self) -> None:
        """Save records to storage."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, indent=2)
            self.logger.debug(f"Saved {len(self.records)} records to {self.storage_path}")
        except Exception as e:
            self.logger.error(f"Error saving records: {e}", exc_info=True)
    
    def add_record(self, record: Dict) -> str:
        """
        Add a new record.
        
        Args:
            record: Dictionary containing record data.
            
        Returns:
            Record ID.
        """
        record_id = f"record_{len(self.records) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        record['id'] = record_id
        record['created_at'] = datetime.now().isoformat()
        record['updated_at'] = datetime.now().isoformat()
        
        self.records.append(record)
        self.save_records()
        self.logger.info(f"Added new record: {record_id}")
        
        return record_id
    
    def get_record(self, record_id: str) -> Optional[Dict]:
        """
        Get a record by ID.
        
        Args:
            record_id: Record identifier.
            
        Returns:
            Record dictionary or None if not found.
        """
        for record in self.records:
            if record.get('id') == record_id:
                return record
        return None
    
    def update_record(self, record_id: str, updates: Dict) -> bool:
        """
        Update an existing record.
        
        Args:
            record_id: Record identifier.
            updates: Dictionary with fields to update.
            
        Returns:
            True if updated successfully, False otherwise.
        """
        for i, record in enumerate(self.records):
            if record.get('id') == record_id:
                record.update(updates)
                record['updated_at'] = datetime.now().isoformat()
                self.records[i] = record
                self.save_records()
                return True
        return False
    
    def remove_record(self, record_id: str) -> bool:
        """
        Remove a record by ID.
        
        Args:
            record_id: Record identifier.
            
        Returns:
            True if removed successfully, False otherwise.
        """
        for i, record in enumerate(self.records):
            if record.get('id') == record_id:
                self.records.pop(i)
                self.save_records()
                return True
        return False
    
    def get_all_records(self, filter_type: Optional[str] = None) -> List[Dict]:
        """
        Get all records, optionally filtered by type.
        
        Args:
            filter_type: Optional record type to filter by.
            
        Returns:
            List of records.
        """
        if filter_type:
            return [r for r in self.records if r.get('type') == filter_type]
        return self.records.copy()
    
    def search_records(self, query: str) -> List[Dict]:
        """
        Search records by query string.
        
        Args:
            query: Search query.
            
        Returns:
            List of matching records.
        """
        query_lower = query.lower()
        results = []
        
        for record in self.records:
            # Search in various fields
            searchable_text = ' '.join([
                str(record.get('title', '')),
                str(record.get('description', '')),
                str(record.get('type', '')),
                str(record.get('notes', ''))
            ]).lower()
            
            if query_lower in searchable_text:
                results.append(record)
        
        return results
    
    def export_to_json(self, filepath: str, record_ids: Optional[List[str]] = None) -> bool:
        """
        Export records to JSON file.
        
        Args:
            filepath: Path to export file.
            record_ids: Optional list of specific record IDs to export. If None, exports all.
            
        Returns:
            True if export successful, False otherwise.
        """
        try:
            if record_ids:
                records_to_export = [r for r in self.records if r.get('id') in record_ids]
            else:
                records_to_export = self.records
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(records_to_export, f, indent=2)
            
            self.logger.info(f"Exported {len(records_to_export)} records to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting records to {filepath}: {e}", exc_info=True)
            return False
    
    def import_from_json(self, filepath: str, merge: bool = True) -> bool:
        """
        Import records from JSON file.
        
        Args:
            filepath: Path to import file.
            merge: If True, merge with existing records. If False, replace all records.
            
        Returns:
            True if import successful, False otherwise.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_records = json.load(f)
            
            if merge:
                # Add imported records, avoiding duplicates by ID
                existing_ids = {r.get('id') for r in self.records}
                for record in imported_records:
                    if record.get('id') not in existing_ids:
                        self.records.append(record)
            else:
                self.records = imported_records
            
            self.save_records()
            self.logger.info(f"Imported {len(imported_records)} records from {filepath}")
            return True
        except FileNotFoundError:
            self.logger.error(f"Import file not found: {filepath}")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in import file {filepath}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error importing records from {filepath}: {e}", exc_info=True)
            return False
    
    def share_record(self, record_id: str, format: str = 'json') -> Optional[str]:
        """
        Generate shareable content for a record.
        
        Args:
            record_id: Record identifier.
            format: Format for sharing ('json', 'text').
            
        Returns:
            Formatted string for sharing, or None if record not found.
        """
        record = self.get_record(record_id)
        
        if not record:
            return None
        
        if format == 'json':
            return json.dumps(record, indent=2)
        elif format == 'text':
            text = f"Lottery Prediction Record\n"
            text += f"{'=' * 40}\n"
            text += f"ID: {record.get('id')}\n"
            text += f"Title: {record.get('title', 'N/A')}\n"
            text += f"Type: {record.get('type', 'N/A')}\n"
            text += f"Created: {record.get('created_at', 'N/A')}\n"
            text += f"Description: {record.get('description', 'N/A')}\n"
            text += f"\nData:\n{json.dumps(record.get('data', {}), indent=2)}\n"
            return text
        
        return None
