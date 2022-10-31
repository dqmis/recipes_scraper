from typing import List, Optional

from bs4 import BeautifulSoup

from scraper.models.recipe import Recipe, RecipeLink
from scraper.scrapers.base import BaseScraper


class Lamaistas(BaseScraper):
    __items_per_page__: int = 44
    __domain__: str = "https://www.lamaistas.lt"

    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[RecipeLink]:
        results: List[RecipeLink] = []

        for page_num in range(2, pages_count + 2):
            content = self._get_page_content(f"paieska?q={keyword}&p={page_num}")
            if content:
                recipes_list_div = content.find("div", class_="searchResultSegment")
                if not recipes_list_div:
                    break
                all_recipes_div = recipes_list_div.find_all("div", class_="frame")
                for recipe_div in all_recipes_div:
                    link_to_recipe = recipe_div.find("a")["href"]
                    results.append(RecipeLink(url=link_to_recipe[25:]))
            else:
                continue
        return results

    def _extract_ingredients(self, content: BeautifulSoup) -> str:
        ingredients_div = content.find("div", class_="ingredients")
        ingredients_table = ingredients_div.find("table")
        tr_rows = ingredients_table.find_all("tr")
        ingredients: List[str] = []
        try:
            for tr_row in tr_rows:
                spans = tr_row.find_all("span")
                ingredients.append(f"{spans[0].text.strip()} - {spans[1].text.strip()}")
        except IndexError:
            pass
        return ", ".join(ingredients)

    def _extract_making_steps(self, content: BeautifulSoup) -> str:
        making_steps: List[str] = []
        description_divs = (
            content.find("div", class_="method")
            .find("div", class_="infoA")
            .find_all("div", class_="description")
        )
        for step, description_div in enumerate(description_divs):
            making_steps.append(f"{step + 1} - {description_div.find('div', class_='text').text}")
        return ", ".join(making_steps)

    def _retrieve_recipe_info(self, link: RecipeLink) -> Optional[Recipe]:
        content = self._get_page_content(link.url)
        if content:
            try:
                recipe_title = content.find("div", class_="recipeTitleSegment").find("h1").text
                about_recipe = content.find("div", class_="authorAboutRecipeSegment").text
            except AttributeError:
                return None

            making_time = (
                content.find("div", class_="method")
                .find("div", class_="info")
                .text.strip()
                .replace("Paruošimo laikas: ", "")
            )

            try:
                main_recipe_image = (
                    content.find("div", {"class": ["smallImgItem", "image"]})
                    .find("img")
                    .get("src")
                )
            except KeyError:
                main_recipe_image = None

            return Recipe(
                title=recipe_title,
                image_url=main_recipe_image,
                about=about_recipe.strip(),
                making_time=making_time,
                ingredients=self._extract_ingredients(content),
                making_steps=self._extract_making_steps(content),
            )
        else:
            return None
