"""Advanced Data Pipeline Scraper package."""

from .core import WebScraper, ScraperConfig
from .validators import ScraperValidator

__version__ = "1.0.0"
__all__ = ["WebScraper", "ScraperConfig", "ScraperValidator"]
