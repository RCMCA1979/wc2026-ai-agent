"""
Data validation with Pydantic models.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Any
from datetime import datetime


class ScrapedItem(BaseModel):
    """Base model for scraped items."""
    
    class Config:
        arbitrary_types_allowed = True


class ProductItem(ScrapedItem):
    """Scraped product item."""
    product_id: str
    name: str
    price: float = Field(..., gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    in_stock: bool = True
    url: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


class NewsArticle(ScrapedItem):
    """Scraped news article."""
    headline: str
    summary: str
    author: Optional[str] = None
    published: datetime
    category: str
    url: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


class ScraperValidator:
    """Validator for scraped data."""
    
    @staticmethod
    def validate_product(data: dict) -> ProductItem:
        """Validate product data."""
        return ProductItem(**data)
    
    @staticmethod
    def validate_article(data: dict) -> NewsArticle:
        """Validate news article data."""
        return NewsArticle(**data)
    
    @staticmethod
    def validate_batch(items: list, model_class: type) -> list:
        """Validate batch of items."""
        validated = []
        for item in items:
            try:
                validated.append(model_class(**item))
            except Exception as e:
                print(f"Validation error for item {item}: {e}")
        return validated
