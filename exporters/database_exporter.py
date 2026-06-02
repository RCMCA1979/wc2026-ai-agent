"""
Database export functionality.
"""

import sqlite3
from typing import List, Dict, Any
from .base import BaseExporter
from loguru import logger


class DatabaseExporter(BaseExporter):
    """Export data to SQLite database."""
    
    def export(self, data: List[Dict[str, Any]], table_name: str = "scraped_data") -> None:
        """Export data to SQLite database."""
        self._validate_data(data)
        
        try:
            conn = sqlite3.connect(self.output_path)
            cursor = conn.cursor()
            
            # Create table
            columns = list(data[0].keys())
            columns_def = ", ".join([f"{col} TEXT" for col in columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
            
            # Insert data
            placeholders = ", ".join(["?" for _ in columns])
            cursor.executemany(
                f"INSERT INTO {table_name} VALUES ({placeholders})",
                [tuple(item.get(col) for col in columns) for item in data]
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Exported {len(data)} items to {self.output_path}")
        except Exception as e:
            logger.error(f"❌ Database export failed: {str(e)}")
            raise
