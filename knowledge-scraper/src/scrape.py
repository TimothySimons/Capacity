import importlib.util
import json
import sys


def make_soup(ingredients, recipe, bowl):
    module = importlib.import_module(f"soups.{recipe}")
    module.Soup(ingredients, bowl).soup_to_csv()


if __name__ == "__main__":
    try:
        config_file_path = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: python {sys.argv[0]} <config_filepath>")

    with open(config_file_path) as config_file:
        config = json.load(config_file)

    for soup in config["soups"]:
        make_soup(soup["ingredients"], soup["recipe"], config["bowl"])