import json

import numpy as np


def load() -> (list[int], list[int]):
    # input_path = input("prosze podac sciezke do pliku z pytaniami>")
    with open("example_data/questions.json", "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]

    return criteria, propositions


def save_expert(
    criteria: list[str],
    propositions: list[str],
    propositions_matrices: np.ndarray,
    expert_name: str,
):
    # output_path = input("prosze podac sciezke gdzie zapisac wyniki>")
    output_path = "./example_data/expert_responses/expert_" + expert_name + ".json"

    with open(output_path, "w") as f:
        json.dump(
            {
                "criteria": criteria,
                "propositions": propositions,
                "matrix": propositions_matrices.tolist(),
            },
            f,
        )
