import numpy as np


def calculate_weights(matrix: list[list[float]]) -> list[float]:
    mat = np.array(matrix)
    u, vector = rayleigh_quotient_iteration(mat)
    if np.min(vector) < 0:
        if np.max(vector) > 0:
            raise ValueError("cannot compute matrix")
        vector *= -1
    return u, list(vector / np.sum(vector))


def rayleigh_quotient_iteration(matrix: np.ndarray, threshold=1e-7, max_iterations=1000) -> (float, np.ndarray):
    identity = np.eye(matrix.shape[0])
    b = np.ones(matrix.shape[0]) / matrix.shape[0]
    u = np.dot(b, matrix @ b) / np.dot(b, b)
    old_u = u + 1000 * threshold

    for i in range(max_iterations):
        temp = np.linalg.solve(matrix - u * identity, b)
        b = temp / np.linalg.norm(temp)
        u = np.dot(b, matrix @ b) / np.dot(b, b)
        if abs(u - old_u) < threshold:
            break
        old_u = u
    return u, b


def power_iteration(matrix: np.ndarray, threshold=1e-7, max_iterations=1000) -> (float, np.ndarray):
    b = np.random.rand(matrix.shape[0])
    old_b = b + 1000 * threshold
    for i in range(max_iterations):
        tmp = matrix @ b
        b = tmp / np.linalg.norm(tmp)
        if np.linalg.norm(b - old_b) < threshold:
            break
        old_b = b
    return np.dot(b, matrix @ b) / np.dot(b, b), b


if __name__ == "__main__":
    tmp = np.array([[1, 2, 3], [1, 2, 1], [3, 2, 1]])
    print(power_iteration(tmp))
    print(rayleigh_quotient_iteration(tmp))
