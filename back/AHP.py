from random import shuffle
from .expert_data import expert_propositions_matrices, expert_criteria_matrix
from .processor import calculate_weights


def is_float(element):
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def print_matrix(M):
    for line in M:
        print(line)


def complete_principal_diagonal(M):
    for i in range(len(M)):
        M[i][i] = 1.0


class AHP:
    criteria_ranking = None
    propositions_rankings = []
    final_ranking = []

    def __init__(self, criteria, propositions):
        self.criteria = criteria
        self.propositions = propositions
        l_c = len(criteria)
        self.criteria_matrix = [[None for _ in range(l_c)] for _ in range(l_c)]
        l_p = len(propositions)
        self.propositions_matrices = [
            [[None for _ in range(l_p)] for _ in range(l_p)] for _ in range(l_c)
        ]

    def generate_questions(self):
        questions = []
        for c in range(len(self.criteria)):
            for i in range(len(self.propositions)):
                for j in range(i + 1, len(self.propositions)):
                    p = [i, j]
                    shuffle(p)
                    questions.append((c, p))

        shuffle(questions)
        return questions

    def generate_criteria_questions(self):
        questions = []
        for i in range(len(self.criteria)):
            for j in range(i + 1, len(self.criteria)):
                p = [i, j]
                shuffle(p)
                questions.append(p)

        shuffle(questions)
        return questions

    def ask_questions(self):
        questions = self.generate_questions()

        for q in questions:
            print(
                "Porownaj:(1) ",
                self.propositions[q[1][0]] + " oraz (2) " + self.propositions[q[1][1]],
            )
            print(" w kategorii " + self.criteria[q[0]] + "(1):(2)")
            c = input()
            while not is_float(c):
                c = input("Podaj poprawna wart: ")
            c = float(c)
            self.propositions_matrices[q[0]][q[1][0]][q[1][1]] = c
            self.propositions_matrices[q[0]][q[1][1]][q[1][0]] = 1 / c

        for M in self.propositions_matrices:
            complete_principal_diagonal(M)
            # print_matrix(M)

    def ask_criteria_questions(self):
        questions = self.generate_criteria_questions()

        for q in questions:
            print(
                "Porownaj kategorie:(1) ",
                self.criteria[q[0]] + " oraz (2) " + self.criteria[q[1]],
            )
            c = input("(1):(2)> ")
            while not is_float(c):
                c = input("Podaj poprawna wart: ")
            c = float(c)
            self.criteria_matrix[q[0]][q[1]] = c
            self.criteria_matrix[q[1]][q[0]] = 1 / c

        complete_principal_diagonal(self.criteria_matrix)
        # print_matrix(self.criteria_matrix)

    def EVM_ranking(self, M):
        return calculate_weights(M)[1]

    def SAATY_index(self, M):
        n = len(M)
        return (calculate_weights(M)[0] - n) / (n - 1)

    def make_criteria_ranking(self):
        self.criteria_ranking = self.EVM_ranking(self.criteria_matrix)

    def make_propositions_criteria_rankings(self):
        for c in self.propositions_matrices:
            self.propositions_rankings.append(self.EVM_ranking(c))

    def count_final_weight(self, i):
        result = 0
        for j in range(len(self.criteria)):
            result += self.criteria_ranking[j] * self.propositions_rankings[j][i]

        return result

    def make_final_ranking(self):
        for i in range(len(self.propositions)):
            self.final_ranking.append((i, self.count_final_weight(i)))
        self.final_ranking.sort(reverse=True, key=lambda x: x[1])

    def print_final_ranking(self):
        for i, w in self.final_ranking:
            print(self.propositions[i])

    def start(self):
        c = input(
            "if you want to trust our expert type x or type anything else and then type your preferences> "
        )
        if c != "x":
            self.ask_questions()

            self.ask_criteria_questions()
        else:
            self.criteria_matrix = expert_criteria_matrix
            self.propositions_matrices = expert_propositions_matrices

        self.make_criteria_ranking()
        self.make_propositions_criteria_rankings()

        self.make_final_ranking()
        self.print_final_ranking()
