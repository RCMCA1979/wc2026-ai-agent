"""
Example: E-commerce Product Scraper
"""

from scraper import WebScraper, ScraperConfig
from exporters import CSVExporter, DatabaseExporter


def scrape_ecommerce():
    """Scrape e-commerce products."""
    
    # Configure scraper
    config = ScraperConfig(
        max_workers=10,
        timeout=10,
        rate_limit=1.0
    )
    
    scraper = WebScraper(config=config, verbose=True)
    
    # URLs to scrape
    urls = [
        "https://example-shop.com/products?page=1",
        "https://example-shop.com/products?page=2",
        "https://example-shop.com/products?page=3",
    ]
    
    # Define extraction fields
    extract_fields = {
        "product_id": "data-id",
        "name": "h3.product-name",
        "price": "span.price",
        "rating": "div.rating",
        "in_stock": "span.stock",
    }
    
    # Scrape
    products = scraper.scrape_urls(
        urls=urls,
        selector="div.product",
        extract_fields=extract_fields
    )
    
    # Export to CSV
    csv_exporter = CSVExporter("products.csv")
    csv_exporter.export(products)
    
    # Export to database
    db_exporter = DatabaseExporter("products.db")
    db_exporter.export(products, table_name="products")
    
    print(f"✅ Scraped {len(products)} products!")
    scraper.close()


if __name__ == "__main__":
    scrape_ecommerce()
