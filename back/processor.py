import numpy as np


def calculate_weights(matrix: list[list[float]]) -> (float, list[float]):
    mat = np.array(matrix)
    u, vector = rayleigh_quotient_iteration(mat)
    if np.min(vector) < 0:
        if np.max(vector) > 0:
            raise ValueError("cannot compute matrix")
        vector *= -1
    return u, list(vector / np.sum(vector))


def calculate_weights_np(matrix: np.ndarray, calc_type: str = "EVM") -> (float, np.ndarray):
    methods = {
        "EVM": evm_method,
        "GMM": gmm_method,
        "LLVM": llvm_method
    }
    return methods[calc_type](matrix)


def evm_method(matrix: np.ndarray) -> (float, np.ndarray):
    matrix2 = matrix + np.diag(np.sum(matrix == 0, axis=0))
    u, vector = rayleigh_quotient_iteration(matrix2)
    if np.min(vector) < 0:
        if np.max(vector) > 0:
            raise ValueError("cannot compute matrix")
        vector *= -1
    n = matrix.shape[0]
    return (u - n) / (n - 1), vector / np.sum(vector)


def gmm_method(matrix: np.ndarray) -> (float, np.ndarray):
    matrix2 = np.zeros_like(matrix)
    matrix2[matrix == 0] = 1
    matrix2 += np.diag(matrix.shape[0] - np.sum(matrix == 0, axis=0))
    r = np.sum(np.log(matrix + (matrix == 0)), axis=1)
    w = np.exp(np.linalg.solve(matrix2, r))

    e = matrix * ((1 / w).reshape((w.size, 1)) @ w.reshape((1, w.size)))
    n = matrix.shape[0]
    triu = np.square(np.log(e + (e == 0)))
    ig = 2 / (n - 1) / (n - 2) * np.sum(np.triu(triu, 1))
    return ig, w / np.sum(w)


def llvm_method(matrix: np.ndarray) -> (float, np.ndarray):
    L = np.zeros_like(matrix)
    L -= matrix != 0
    L += np.diag(1 + np.sum(matrix != 0, axis=0))
    r = np.sum(np.log(matrix + (matrix == 0)), axis=1)
    w = np.exp(np.linalg.solve(L, r))

    expr = np.sum(np.square((matrix - w.reshape((w.size, 1)) @ (1 / w).reshape((1, w.size)))[matrix != 0]))
    return expr, w / np.sum(w)


def rayleigh_quotient_iteration(
        matrix: np.ndarray, threshold=1e-7, max_iterations=1000
) -> (float, np.ndarray):
    identity = np.eye(matrix.shape[0])
    b = np.ones(matrix.shape[0]) / matrix.shape[0]
    u = np.dot(b, matrix @ b) / np.dot(b, b)
    old_u = u + 1000 * threshold

    for i in range(max_iterations):
        matrix_prim = matrix - u * identity
        while True:
            try:
                temp = np.linalg.solve(matrix_prim, b)
                break
            except np.linalg.LinAlgError:
                matrix_prim = matrix_prim - u * identity  # remove all 0 eigenvalues

        b = temp / np.linalg.norm(temp)
        u = np.dot(b, matrix @ b) / np.dot(b, b)
        if abs(u - old_u) < threshold:
            break
        old_u = u
    return u, b


def power_iteration(
        matrix: np.ndarray, threshold=1e-7, max_iterations=1000
) -> (float, np.ndarray):
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
