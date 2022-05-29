import importlib.util
import json
import os
import sys


def make_soups(recipes):
    for recipe in recipes:
        flavour = recipe["flavour"]
        ingredients = recipe["ingredients"]
        instructions = recipe["instructions"]
        bowl = recipe["bowl"]

        module = importlib.import_module(f"soups.{instructions}")
        soup = module.Soup()
        for ingredient in ingredients:
            soup.add_ingredient(**{flavour: ingredient})
        soup.pour(bowl)


def clean_bowls(bowls):
    for bowl in bowls:
        if os.path.exists(bowl):
            os.remove(bowl)


if __name__ == "__main__":
    try:
        config_path = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: python {sys.argv[0]} <config_path>")

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    soup_recipes = config["soups"]
    clean_bowls([soup_recipe["bowl"] for soup_recipe in soup_recipes])
    make_soups(soup_recipes)
