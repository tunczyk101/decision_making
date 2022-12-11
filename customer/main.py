from glob import iglob
from back.AHP import AHP
import json

# criteria = ["lokalizacja", "obsluga", "wystroj", "ilosc smakow", "jakosc lodow", "cena", "jakosc sorbetow"]
# propositions = ["Good Lood Miasteczko AGH", "Wadowice", "Tiffany Ice Cream"]

questions_file = None
criteria_ranks_file = None
expert_responses_directory = None


def geometric_mean(x):
    tmp = 1
    for i in x:
        tmp *= i
    return tmp / len(x)


def ask_path(prompt, last_path):
    print(prompt)
    if last_path is not None:
        print(f"lub pustą linie by uzyc w poprzedniej lokalizacji [{last_path}]")
    while True:
        path = input(">")
        if path != "":
            return path
        if last_path is not None:
            return last_path
        print("prosze podac sciezke")


def gen_questions_file():
    global questions_file
    print("wprowadź kryteria, zakoncz wprowadzanie zostawiajac na koncu pusta linie")
    criteria = []
    while True:
        line = input(">")
        if line == "":
            break
        criteria.append(line)
    print("wprowadz propozycje, zakoncz wprowadzanie zostawiajac na koncu pusta linie")
    propositions = []
    while True:
        line = input(">")
        if line == "":
            break
        propositions.append(line)
    questions_file = ask_path("wprowadź ścieżkę do pliku w ktorym zapisac pytania", questions_file)
    with open(questions_file, "w") as f:
        json.dump({
            "criteria": criteria,
            "propositions": propositions
        }, f)


def ask_questions_customer():
    global questions_file, criteria_ranks_file
    questions_file = ask_path("prosze podac scierzke do pliku z pytaniami", questions_file)
    with open(questions_file, "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]
    ahp = AHP(criteria, propositions)
    ahp.ask_criteria_questions()

    criteria_ranks_file = ask_path("wprowadz sciezke do pliku w ktorym zapisac wynik", criteria_ranks_file)
    with open(criteria_ranks_file, "w") as f:
        json.dump({
            "criteria": criteria,
            "propositions": propositions,
            "criteria_matrix": ahp.criteria_matrix
        }, f)


def generate_ranking():
    global questions_file, criteria_ranks_file, expert_responses_directory
    questions_file = ask_path("prosze podac sciezke do pliku z pytaniami", questions_file)
    criteria_ranks_file = ask_path("prosze podac sciezke do pliku z hierarchia kategorii", criteria_ranks_file)
    expert_responses_directory = ask_path("prosze podac sciezke do katalogu z odpowiedziami expertow",
                                          expert_responses_directory)
    with open(questions_file, "r") as f:
        data = json.load(f)
    criteria = data["criteria"]
    propositions = data["propositions"]
    with open(criteria_ranks_file, "r") as f:
        data = json.load(f)
    if criteria != data["criteria"]:
        print("hierarchia kategorii zostala wygenerowana dla innego zbioru kategorii")
        return
    ahp = AHP(criteria, propositions)
    ahp.criteria_matrix = data["criteria_matrix"]
    ahp.make_criteria_ranking()
    expert_responses = []
    for file in iglob(expert_responses_directory + "/*"):
        with open(file, "r") as f:
            data = json.load(f)
        if criteria != data["criteria"] or propositions != data["propositions"]:
            print(
                f"plik z odpowiedziami {file} zostal wygenerowany z innymi parametrami niz podane, zostanie zignorowany")
            continue
        ahp.propositions_matrices = data["matrix"]
        ahp.propositions_rankings = []
        ahp.make_propositions_criteria_rankings()
        expert_responses.append(ahp.propositions_rankings)
    if len(expert_responses) == 0:
        print("nie znaleziono plikow z odpowiedziami expertow")
        return
    ahp.propositions_rankings = [
        [geometric_mean([response[i][j] for response in expert_responses])
            for j in range(len(expert_responses[0][0]))]
                                 for i in range(len(expert_responses[0]))]
    ahp.make_final_ranking()
    print("ostateczny ranking:")
    print("=" * 16)
    ahp.print_final_ranking()
    print("=" * 16)

while True:
    print("Prosze wybrac operacje do wykonania")
    print("1: wygenerowanie pliku z pytaniami (dla eksperta)")
    print("2: ustal hierarchie kategorii")
    print("3: wylicz ranking")
    print("4: wyjdz z programu")
    v = input(">")
    if v == "1":
        gen_questions_file()
    elif v == "2":
        ask_questions_customer()
    elif v == "3":
        generate_ranking()
    elif v == "4":
        break
