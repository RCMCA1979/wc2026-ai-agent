"""
CSV export functionality.
"""

import csv
from typing import List, Dict, Any
from .base import BaseExporter
from loguru import logger


class CSVExporter(BaseExporter):
    """Export data to CSV format."""
    
    def export(self, data: List[Dict[str, Any]]) -> None:
        """Export data to CSV file."""
        self._validate_data(data)
        
        try:
            fieldnames = list(data[0].keys())
            
            with open(self.output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"✅ Exported {len(data)} items to {self.output_path}")
        except Exception as e:
            logger.error(f"❌ CSV export failed: {str(e)}")
            raise
