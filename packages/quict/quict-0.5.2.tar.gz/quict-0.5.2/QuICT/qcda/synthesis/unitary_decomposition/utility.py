from typing import *
import numpy as np

from QuICT.core import *
from QuICT.core.gate import *


def add_factor_shift_into_phase(gates: CompositeGate, shift: complex) -> CompositeGate:
    phase = np.log(shift) / 1j
    phase_gate = GPhase.copy()
    phase_gate.pargs = [phase]
    phase_gate.targs = [0]
    gates.append(phase_gate)
    return gates


def quantum_shannon_decompose(
        u1: np.ndarray,
        u2: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Decompose a block diagonal even-size unitary matrix.
    block_diag(u1,u2) == block_diag(v, v) @ block_diag(d, d_dagger) @ block_diag(w, w)

    Args:
        u1 (np.ndarray): upper-left block
        u2 (np.ndarray): right-bottom block

    Returns:
        Tuple[np.ndarray,np.ndarray,np.ndarray]
    """
    s = u1 @ u2.conj().T

    eig_values, v = np.linalg.eig(s)
    v_dagger = v.conj().T
    d = np.sqrt(np.diag(eig_values))

    # u1 @ u2_dagger == v @ d_square @ v_dagger

    w = d @ v_dagger @ u2

    return v, d, w


def shift_ratio(mat1: np.ndarray, mat2: np.ndarray) -> complex:
    mat_size = mat1.shape[0]
    shift = 1.0 + 0.0j
    for j in range(mat_size):
        if not np.isclose(0, mat2[0, j]):
            shift = mat1[0, j] / mat2[0, j]
    return shift
