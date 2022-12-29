from back.AHP import AHP
import json

def load_questions():
    # input_path = input("prosze podac sciezke do pliku z pytaniami>")
    with open("example_data/questions.json", "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]

    ahp = AHP(criteria, propositions)
    ahp.generate_expert_questions()
    return ahp

def save_expert(ahp, expert_name):
    # output_path = input("prosze podac sciezke gdzie zapisac wyniki>")
    output_path = "example_data/expert_responses/expert_" + expert_name + ".json"

    with open(output_path, "w") as f:
        json.dump(
            {
                "criteria": ahp.criteria,
                "propositions": ahp.propositions,
                "matrix": ahp.propositions_matrices,
            },
            f,
        )
