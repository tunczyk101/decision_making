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
    expert_questions = []
    curr_question_nr = -1
    actual_criteria = []
    customer_questions = []
    curr_criteria_nr = -1

    def __init__(self, criteria, propositions):
        self.criteria = criteria
        self.propositions = propositions
        l_c = len(criteria)
        self.criteria_matrix = [[None for _ in range(l_c)] for _ in range(l_c)]
        l_p = len(propositions)
        self.propositions_matrices = [
            [[None for _ in range(l_p)] for _ in range(l_p)] for _ in range(l_c)
        ]

    def EVM_ranking(self, M):
        return calculate_weights(M)[1]

    def SAATY_index(self, M):
        n = len(M)
        return (calculate_weights(M)[0] - n) / (n - 1)

    def make_criteria_ranking(self):
        self.criteria_ranking = self.EVM_ranking(self.criteria_matrix)

    def make_propositions_criteria_rankings(self):
        for i in range(len(self.actual_criteria)):
            print(self.propositions_matrices[i])
            self.propositions_rankings.append(self.EVM_ranking(self.propositions_matrices[i]))

    def count_final_weight(self, i):
        result = 0
        print(self.propositions_rankings)
        for j in range(len(self.actual_criteria)):
            print("j= ", j)
            print(self.propositions_rankings[self.actual_criteria[j]][i])
            result += self.criteria_ranking[j] * self.propositions_rankings[j][i]

        return result

    def make_final_ranking(self):
        for i in self.actual_criteria:
            print("i=", i)
            self.final_ranking.append((i, self.count_final_weight(i)))
        self.final_ranking.sort(reverse=True, key=lambda x: x[1])

    def make_ranking_for_customer(self):
        self.make_criteria_ranking()
        print(1)
        self.make_propositions_criteria_rankings()
        print(1)
        self.make_final_ranking()
        print(1)
        self.print_final_ranking()
        print(1)

    def print_final_ranking(self):
        for i, w in self.final_ranking:
            print(self.propositions[i])

    def generate_expert_questions(self):
        self.curr_question_nr = -1
        questions = []
        for c in range(len(self.criteria)):
            for i in range(len(self.propositions)):
                for j in range(i + 1, len(self.propositions)):
                    p = [i, j]
                    shuffle(p)
                    questions.append((c, p))

        shuffle(questions)
        self.expert_questions = questions

    def generate_customer_questions(self):
        self.curr_criteria_nr = -1
        questions = []
        for i in range(len(self.actual_criteria)):
            for j in range(i + 1, len(self.actual_criteria)):
                p = [(self.actual_criteria[i], i), (self.actual_criteria[j], j)]
                shuffle(p)
                questions.append(p)
        shuffle(questions)
        self.customer_questions = questions
        l_c = len(self.actual_criteria)
        self.criteria_matrix = [[None for _ in range(l_c)] for _ in range(l_c)]
        self.fill_customer_diagonal()

    def check_next_expert_question(self):
        self.curr_question_nr += 1
        if self.curr_question_nr + 1 >= len(self.expert_questions):
            return True
        return False

    def check_next_customer_question(self):
        self.curr_criteria_nr += 1
        if self.curr_criteria_nr + 1 >= len(self.customer_questions):
            return True
        return False

    def get_category(self):
        return self.criteria[self.expert_questions[self.curr_question_nr][0]]

    def save_expert_value(self, c):
        c = float(c)
        q = self.expert_questions[self.curr_criteria_nr]
        self.propositions_matrices[q[0]][q[1][0]][q[1][1]] = c
        self.propositions_matrices[q[0]][q[1][1]][q[1][0]] = 1 / c

    def save_customer_value(self, c):
        c = float(c)
        q = self.customer_questions[self.curr_criteria_nr]
        self.criteria_matrix[q[0][1]][q[1][1]] = c
        self.criteria_matrix[q[1][1]][q[0][1]] = 1 / c

    def fill_expert_diagonals(self):
        for M in self.propositions_matrices:
            complete_principal_diagonal(M)

    def fill_customer_diagonal(self):
        complete_principal_diagonal(self.criteria_matrix)

    def get_left(self):
        return self.propositions[self.expert_questions[self.curr_question_nr][1][0]]

    def get_right(self):
        return self.propositions[self.expert_questions[self.curr_question_nr][1][1]]

    def get_left_cat(self):
        return self.criteria[self.customer_questions[self.curr_criteria_nr][0][0]]

    def get_right_cat(self):
        return self.criteria[self.customer_questions[self.curr_criteria_nr][1][0]]

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

    def ask_criteria_questions(self):
        self.generate_customer_questions()
        questions = self.customer_questions

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
