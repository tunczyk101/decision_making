from random import shuffle


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

    def __init__(self, criteria, propositions):
        self.criteria = criteria
        self.propositions = propositions
        l_c = len(criteria)
        self.criteria_matrix = [[None for _ in range(l_c)] for _ in range(l_c)]
        l_p = len(propositions)
        self.propositions_matrices = [[[None for _ in range(l_p)] for _ in range(l_p)] for _ in range(l_c)]

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
            print("Porownaj:(1) ", self.propositions[q[1][0]] + " oraz (2) " + self.propositions[q[1][1]])
            print(" w kategorii " + self.criteria[q[0]] + "(1):(2)")
            c = input()
            while not is_float(c):
                c = input("Podaj poprawna wart: ")
            c = float(c)
            self.propositions_matrices[q[0]][q[1][0]][q[1][1]] = c
            self.propositions_matrices[q[0]][q[1][1]][q[1][0]] = 1/c

        for M in self.propositions_matrices:
            complete_principal_diagonal(M)
            print_matrix(M)


    def ask_criteria_questions(self):
        questions = self.generate_criteria_questions()

        for q in questions:
            print("Porownaj kategorie:(1) ", self.criteria[q[0]] + " oraz (2) " + self.criteria[q[1]])
            c = input("(1):(2)> ")
            while not is_float(c):
                c = input("Podaj poprawna wart: ")
            c = float(c)
            self.criteria_matrix[q[0]][q[1]] = c
            self.criteria_matrix[q[1]][q[0]] = 1 / c

        complete_principal_diagonal(self.criteria_matrix)
        print_matrix(self.criteria_matrix)
