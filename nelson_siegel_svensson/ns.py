from numbers import Number
from dataclasses import dataclass

import numpy as np
from numpy import exp

EPS = np.finfo(float).eps


@dataclass
class NelsonSiegelCurve:
    beta0: float
    beta1: float
    beta2: float
    tau: float

    def factors(self, T):
        tau = self.tau
        if isinstance(T, Number) and T <= 0:
            return 1, 0
        elif isinstance(T, np.ndarray):
            zero_idx = T <= 0
            T[zero_idx] = EPS  # avoid warnings in calculations
        exp_tt0 = exp(-T/tau)
        factor1 = (1 - exp_tt0) / (T / tau)
        factor2 = factor1 - exp_tt0
        if isinstance(T, np.ndarray):
            T[zero_idx] = 0
            factor1[zero_idx] = 1
            factor2[zero_idx] = 0
        return factor1, factor2

    def zero(self, T):
        factor1, factor2 = self.factors(T)
        return self.beta0 + self.beta1*factor1 + self.beta2*factor2

    def __call__(self, T):
        return self.zero(T)