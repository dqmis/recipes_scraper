from typing import Optional

from pydantic import BaseModel


class Recipe(BaseModel):
    title: str
    image_url: Optional[str]
    about: str
    making_time: str
    ingredients: str
    making_steps: str


class RecipeLink(BaseModel):
    url: str
