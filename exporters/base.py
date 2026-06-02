"""
Base exporter class.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseExporter(ABC):
    """Base class for data exporters."""
    
    def __init__(self, output_path: str):
        """Initialize exporter."""
        self.output_path = output_path
    
    @abstractmethod
    def export(self, data: List[Dict[str, Any]]) -> None:
        """Export data to specified format."""
        pass
    
    def _validate_data(self, data: List[Dict[str, Any]]) -> None:
        """Validate data before export."""
        if not isinstance(data, list):
            raise ValueError("Data must be a list of dictionaries")
        if len(data) == 0:
            raise ValueError("Data list is empty")
