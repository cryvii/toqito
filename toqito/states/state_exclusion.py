"""Calculates probability of state exclusion."""
import cvxpy as cvx
import numpy as np

from typing import List


def state_exclusion(states: List[np.ndarray],
                    probs: List[float] = None) -> float:
    """
    Computes probability of state exclusion.

    State exclusion implies that ability to discard (with certainty) at least
    one out of the "n" possible quantum states by applying a measurment.

    References:
        [1] "On the reality of the quantum state"
            Pusey, Matthew F., Jonathan Barrett, and Terry Rudolph.
            Nature Physics 8.6 (2012): 475-478.
            arXiv:1111.3328
        [2] "Conclusive exclusion of quantum states"
            Bandyopadhyay, Somshubhro, et al.
            Physical Review A 89.2 (2014): 022336.
            arXiv:1306.4683
    """
    # Assume uniform probability if no specific distribution is given.
    if probs is None:
        probs = [1/len(states)] * len(states)
    if sum(probs) != 1:
        raise ValueError("Invalid: Probabilities must sum to 1.")

    if len(states) >= 1:
        dim = states[0].shape

        obj_func = []
        measurements = []
        constraints = []
        for i in range(len(states)):
            measurements.append(cvx.Variable(dim, PSD=True))

            obj_func.append(probs[i] * cvx.trace(
                states[i].conj().T * measurements[i]))

        constraints.append(sum(measurements) == np.identity(dim[0]))

        objective = cvx.Minimize(sum(obj_func))
        problem = cvx.Problem(objective, constraints)
        sol_default = problem.solve()

        return 1/len(states) * sol_default

