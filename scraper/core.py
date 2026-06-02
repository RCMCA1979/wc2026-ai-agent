"""
Core scraper functionality with multi-threading support.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from pydantic import BaseModel, Field
from dataclasses import dataclass
import time


class ScraperConfig(BaseModel):
    """Configuration for web scraper."""
    max_workers: int = 10
    timeout: int = 10
    retries: int = 3
    rate_limit: float = 1.0  # seconds between requests
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    verify_ssl: bool = True
    proxy_list: Optional[List[str]] = None
    
    class Config:
        arbitrary_types_allowed = True


class WebScraper:
    """Enterprise-grade web scraper with threading and retry logic."""
    
    def __init__(self, config: Optional[ScraperConfig] = None, verbose: bool = True):
        """Initialize scraper with configuration."""
        self.config = config or ScraperConfig()
        self.verbose = verbose
        self.session = self._create_session()
        self.last_request_time = 0
        
        if verbose:
            logger.info(f"🚀 Scraper initialized with config: {self.config}")
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with connection pooling."""
        session = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=self.config.max_workers,
            pool_maxsize=self.config.max_workers,
            max_retries=self.config.retries
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"User-Agent": self.config.user_agent})
        return session
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.config.rate_limit:
            time.sleep(self.config.rate_limit - elapsed)
        self.last_request_time = time.time()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch_url(self, url: str) -> str:
        """Fetch URL with retry logic."""
        self._apply_rate_limit()
        
        try:
            response = self.session.get(
                url,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching {url}: {str(e)}")
            raise
    
    def _parse_html(self, html: str, selector: str, extract_fields: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Parse HTML and extract data."""
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(selector)
        
        results = []
        for element in elements:
            if extract_fields:
                data = {}
                for field_name, field_selector in extract_fields.items():
                    try:
                        found = element.select_one(field_selector)
                        data[field_name] = found.get_text(strip=True) if found else None
                    except Exception as e:
                        logger.debug(f"Field extraction error for {field_name}: {e}")
                        data[field_name] = None
                results.append(data)
            else:
                results.append({"content": element.get_text(strip=True)})
        
        return results
    
    def scrape_urls(
        self,
        urls: List[str],
        selector: str,
        extract_fields: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """Scrape multiple URLs concurrently."""
        all_results = []
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            future_to_url = {
                executor.submit(self._fetch_url, url): url
                for url in urls
            }
            
            completed = 0
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    html = future.result()
                    results = self._parse_html(html, selector, extract_fields)
                    all_results.extend(results)
                    completed += 1
                    
                    if self.verbose:
                        logger.info(f"✅ Scraped {url} ({completed}/{len(urls)})")
                except Exception as e:
                    logger.error(f"❌ Failed to scrape {url}: {str(e)}")
        
        if self.verbose:
            logger.info(f"🎯 Total items scraped: {len(all_results)}")
        
        return all_results
    
    def close(self):
        """Close the session."""
        self.session.close()
        if self.verbose:
            logger.info("🔌 Scraper session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
