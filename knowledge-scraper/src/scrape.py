import sys
from src.soups.itexams import ItExamsSoup

if __name__ == "__main__":
    try:
        config_filepath = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: python {sys.argv[0]} <config_filepath>")


