from typing import Dict, List

from scraper.scrapers import SCRAPERS
from scraper.scrapers.base import BaseScraper


class Scraper:
    def _parse_scrapers(self, scrapers: list[str]) -> List[BaseScraper]:
        return [SCRAPERS[scraper]() for scraper in scrapers]

    def scrape(
        self, recipes_per_scraper_count: int, keyword: str, scrapers: List[str]
    ) -> List[Dict]:
        parsed_scrapers: List[BaseScraper] = self._parse_scrapers(scrapers)
        results: List[Dict] = []

        for scraper in parsed_scrapers:
            print(f"Scraping with {scraper.__class__.__name__,} scraper...")
            results.append(
                {
                    "scraper": scraper.__class__.__name__,
                    "items": scraper.scrape(recipes_per_scraper_count, keyword),
                }
            )

        return results
