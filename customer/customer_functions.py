import json
from glob import iglob
from back.AHP import AHP


def geometric_mean(x):
    tmp = 1
    for i in x:
        tmp *= i
    return tmp / len(x)

def load():
    with open("example_data/questions.json", "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]

    return AHP(criteria, propositions)


def ranking(ahp: AHP):
    criteria = ahp.criteria
    propositions = ahp.propositions
    expert_responses_directory = "example_data/expert_responses"
    expert_responses = []
    print("val")

    for file in iglob(expert_responses_directory + "/*"):
        with open(file, "r") as f:
            data = json.load(f)
        if criteria != data["criteria"] or propositions != data["propositions"]:
            print(
                f"plik z odpowiedziami {file} zostal wygenerowany z innymi parametrami niz podane, zostanie zignorowany"
            )
            continue
        ahp.propositions_matrices = data["matrix"]
        ahp.propositions_rankings = []
        ahp.make_propositions_criteria_rankings()
        expert_responses.append(ahp.propositions_rankings)
    print("files")
    if len(expert_responses) == 0:
        print("nie znaleziono plikow z odpowiedziami expertow")
        return
    ahp.propositions_rankings = [
        [
            geometric_mean([response[i][j] for response in expert_responses])
            for j in range(len(expert_responses[0][0]))
        ]
        for i in range(len(expert_responses[0]))
    ]
    print("rank geom: ")
    ahp.make_criteria_ranking()
    ahp.make_final_ranking()
    print("ostateczny ranking:")
    print("=" * 16)
    ahp.print_final_ranking()
    print("=" * 16)
