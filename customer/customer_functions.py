import json
from glob import iglob
import numpy as np
import back.ahp as fahp


def load() -> (list[str], list[str]):
    with open("example_data/questions.json", "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]

    return criteria, propositions


def ranking(
    criteria: list[str],
    propositions: list[str],
    actual_criteria: list[int],
    criteria_matrix: np.ndarray,
):
    expert_responses_directory = "example_data/expert_responses"
    expert_responses = []

    for file in iglob(expert_responses_directory + "/*"):
        with open(file, "r") as f:
            data = json.load(f)
        if criteria != data["criteria"] or propositions != data["propositions"]:
            print(
                f"plik z odpowiedziami {file} zostal wygenerowany z innymi parametrami niz podane, zostanie zignorowany"
            )
            continue
        propositions_matrices = np.array(data["matrix"])[actual_criteria, :, :]
        expert_responses.append(
            fahp.make_propositions_criteria_rankings(propositions_matrices)
        )
    if len(expert_responses) == 0:
        print("nie znaleziono plikow z odpowiedziami expertow")
        return
    propositions_rankings = fahp.aggregate_rankings(expert_responses)
    criteria_ranking = fahp.make_criteria_ranking(criteria_matrix)
    return fahp.make_final_ranking(propositions_rankings, criteria_ranking)
