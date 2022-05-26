import typer
from libs.thingiverse import Thingiverse
import requests
import json


def main(chunk: int = typer.Argument(...)):
    print("Start parser")
    thingiverse = Thingiverse()
    thingiverse.login()
    items = thingiverse.parse_items(chunk)
    with open(f"data-{chunk}.json", 'w') as outfile:
        json.dump(items, outfile)


if __name__ == "__main__":
    typer.run(main)
