import math
from abc import ABC, abstractmethod
from decimal import DivisionByZero
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scraper.models.recipe import Recipe, RecipeLink


class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[RecipeLink]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content)
        raise Exception("Cannot reach content!")

    @abstractmethod
    def _retrieve_recipe_info(self, link: RecipeLink) -> Optional[Recipe]:
        pass

    def scrape(self, recipes_count: int, keyword: str) -> List[Recipe]:
        try:
            pages_count = math.ceil(recipes_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise AttributeError("Recipes per page is set to 0!")
        recipe_links = self._retrieve_items_list(pages_count, keyword)
        scraped_recipes: List[Optional[Recipe]] = []
        for recipe_link in tqdm(recipe_links):
            scraped_recipe = self._retrieve_recipe_info(recipe_link)
            if scraped_recipe:
                scraped_recipes.append(scraped_recipe)
        return scraped_recipes
