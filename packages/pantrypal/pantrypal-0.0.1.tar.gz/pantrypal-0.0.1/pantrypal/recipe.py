from __future__ import annotations
from pantrypal import constants
from recipe_scrapers import scrape_me
from pantrypal.ingredient import Ingredient


class Recipe:
    def __init__(self):
        self._ingredients = []
        self._instructions = []
        self._name: str = None
        self._source: str = None

    def __repr__(self) -> str:
        if self._name is not None:
            string = f"{self._name} Recipe"
        else:
            string = "Recipe"

        return string

    @classmethod
    def from_url(cls: Recipe, url: str) -> Recipe:
        """Create a recipe instance from a website URL."""
        # Create scraper
        scraper = scrape_me(url_path=url, wild_mode=True)

        # Construct Recipe instance
        recipe: Recipe = cls()
        recipe._ingredients = scraper.ingredients()
        recipe._name = scraper.title()
        recipe._instructions = scraper.instructions_list()
        recipe._source = url

        # Also have attributes yields, total_time, nutrients ...

        return recipe

    def add_ingredient(self, ingredient: str, quantity: float, unit: str):
        """Adds an ingredient to the recipe in a specified quantity."""
        pass

    @staticmethod
    def parse_ingredient(ingredient: str) -> Ingredient:
        """Returns a PantryPall Ingredient"""
        quantities = Recipe._find_numbers(ingredient)
        units = Recipe._identify_units(ingredient)
        item = Recipe._identify_item(ingredient, quantities, units)

        # Create ingredient instance
        i = Ingredient()

        return i

    @staticmethod
    def _find_numbers(string: str) -> list:
        """Returns a list of floats contained within a given string."""
        l = []
        for t in string.split():
            try:
                l.append(float(t))
            except ValueError:
                pass
        return l

    @staticmethod
    def _identify_units(ingredient: str, quantities: list, units: str) -> str:
        """Identifies the unit of an ingredient from a string."""
        pass

    @staticmethod
    def _identify_item(ingredient: str):
        """Identifies the item of an ingredient from a string."""
        units = []
        numbers = []
        item = []
        for s in ingredient.lower().split():
            if s in constants.units:
                units.append(s)
            elif s in constants.quantities:
                numbers.append(s)
            else:
                item.append(s)

        print(units)
        print(numbers)
        print(item)
