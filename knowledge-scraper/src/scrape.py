import importlib.util
import json
import sys


def make_soup(flavour, ingredient, recipe, bowl):
    module = importlib.import_module(f"soups.{recipe}")
    module.Soup(bowl, **{flavour: ingredient}).soup_to_csv("a")


if __name__ == "__main__":
    try:
        config_file_path = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: python {sys.argv[0]} <config_filepath>")

    with open(config_file_path) as config_file:
        config = json.load(config_file)

    for soup in config["soups"]:
        for ingredient in soup["ingredients"]:
            make_soup(soup["flavour"], ingredient, soup["recipe"], config["bowl"])
