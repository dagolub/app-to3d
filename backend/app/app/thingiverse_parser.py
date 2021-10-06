import typer
from libs.thingiverse import Thingiverse
import requests
import json


def main():
    print("Start parser")
    thingiverse = Thingiverse()
    thingiverse.login()
    items = thingiverse.parse_items()
    requests.post("http://localhost:8001/api/v1/items/upload/1",
                  data=json.dumps({'data': items}),
                  headers={'Content-Type': 'application/json'})


if __name__ == "__main__":
    typer.run(main)
