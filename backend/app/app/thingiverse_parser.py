import typer
from libs.thingiverse import Thingiverse
import requests
import json


def main():
    print("Start parser")
    thingiverse = Thingiverse()
    thingiverse.login()
    items = thingiverse.parse_items()
    with open('data.json', 'w') as outfile:
        json.dump(items, outfile)


if __name__ == "__main__":
    try:
        typer.run(main)
    except Exception:
        pass
