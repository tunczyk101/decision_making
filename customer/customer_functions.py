import json

from back.AHP import AHP


def load():
    with open("example_data/questions.json", "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]

    return AHP(criteria, propositions)
