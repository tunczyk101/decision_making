from .processor import calculate_weights_np
import numpy as np
from random import shuffle
from scipy.stats import gmean


def EVM_ranking(M: np.ndarray, method) -> np.ndarray:
    if M.size == 1:
        return np.array([1])
    return calculate_weights_np(M)[1]


def SAATY_index(M: np.ndarray, method) -> float:
    n = M.shape[0]
    if n == 1:
        return 0
    return (calculate_weights_np(M)[0] - n) / (n - 1)


def make_criteria_ranking(criteria_matrix: np.ndarray, method: str) -> np.ndarray:
    return EVM_ranking(criteria_matrix, method)


# propositions_matrices[criteria, proposition, proposition]
def make_propositions_criteria_rankings(
    propositions_matrices: np.ndarray,
    method: str
) -> np.ndarray:
    propositions_rankings = np.zeros(
        (propositions_matrices.shape[0], propositions_matrices.shape[1]), dtype=float
    )
    for i in range(propositions_matrices.shape[0]):
        propositions_rankings[i, :] = EVM_ranking(propositions_matrices[i, :, :], method)
    return propositions_rankings


# propositions_rankings[criteria, proposition]
# criteria_ranking[criteria]
def make_final_ranking(
    propositions_rankings: np.ndarray, criteria_ranking: np.ndarray
) -> (np.ndarray, list[int]):
    final_ranking: np.ndarray = propositions_rankings.T @ criteria_ranking
    indexes = list(range(final_ranking.size))
    indexes.sort(reverse=True, key=lambda x: final_ranking[x])
    return final_ranking, indexes


def aggregate_rankings(rankings: list[np.ndarray]) -> np.ndarray:
    rankings = np.array(rankings)
    return gmean(rankings, axis=0)


def generate_expert_questions(no_criteria, no_propositions):
    questions = []
    for c in range(no_criteria):
        for i in range(no_propositions):
            for j in range(i + 1, no_propositions):
                p = [i, j]
                shuffle(p)
                questions.append((c, p))

    shuffle(questions)
    return questions


def generate_customer_questions(actual_criteria: list[int]) -> list[(int, int)]:
    questions = []
    for i in range(len(actual_criteria)):
        for j in range(i + 1, len(actual_criteria)):
            p = [(actual_criteria[i], i), (actual_criteria[j], j)]
            shuffle(p)
            questions.append(p)
    shuffle(questions)
    return questions
