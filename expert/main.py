from back.AHP import AHP
import json

input_path = input("prosz� poda� �cie�k� do pliku z pytaniami>")
with open(input_path, "r") as f:
    data = json.load(f)
criteria = data["criteria"]
propositions = data["propositions"]

ahp = AHP(criteria, propositions)
ahp.ask_questions()

output_path = input("prosz� poda� �cie�k� gdzie zapisa� wyniki>")
with open(output_path,"w") as f:
    json.dump({
        "criteria": criteria,
        "propositions": propositions,
        "matrix": ahp.propositions_matrices
    }, f)