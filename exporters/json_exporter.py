"""
JSON export functionality.
"""

import json
from typing import List, Dict, Any
from .base import BaseExporter
from loguru import logger
from datetime import datetime


class JSONExporter(BaseExporter):
    """Export data to JSON format."""
    
    def export(self, data: List[Dict[str, Any]]) -> None:
        """Export data to JSON file."""
        self._validate_data(data)
        
        try:
            with open(self.output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, default=str, ensure_ascii=False)
            
            logger.info(f"✅ Exported {len(data)} items to {self.output_path}")
        except Exception as e:
            logger.error(f"❌ JSON export failed: {str(e)}")
            raise
