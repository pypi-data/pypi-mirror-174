from itertools import product
import math
import numpy as np
from typing import List, Tuple

from QuICT.ops.linalg.cpu_calculator import tensor, dot
from QuICT.core.gate import ID, X, Y, Z
from .utils import is_kraus_ops, NoiseChannel


class QuantumNoiseError:
    """ The based class for quantum noise error.

    Example:
        quantum_error = QuantumNoiseError([(error_matrix1, 0.4), (error_matrix2, 0.6)])

    Args:
        ops (List[Tuple(error_matrix: np.ndarray, prob: float)]): The noise error operators, the sum of
            the probabilities should be 1.
        kraus_ops (List[np.ndarray]): The specified kraus operators, used for damping error.
            If None, kraus = [np.sqrt(prob) * error_matrix]. Default to be None.
    """
    @property
    def kraus(self):
        """ The kraus operator """
        return self._kraus_operators

    @property
    def kraus_ct(self):
        """ The kraus operator's conjugate transpose. """
        return self._kraus_conj_ops

    @property
    def operators(self):
        """ The noise error's matrix. """
        return self._operators

    @property
    def probabilties(self):
        """ The probability of each noise error's matrix. """
        return self._probs

    @property
    def type(self):
        """ The type of noise error. """
        return self._type

    @type.setter
    def type(self, channel: NoiseChannel):
        assert isinstance(channel, NoiseChannel)
        self._type = channel

    @property
    def qubits(self):
        """ The number of qubits. """
        return self._qubits

    def __init__(self, ops: List[Tuple[np.ndarray, float]], kraus_ops: List[np.ndarray] = None):
        if not isinstance(ops, list):
            raise TypeError("Wrong input for Noise Error.")

        # Initial error matrix and probability
        self._operators = [matrix for matrix, _ in ops]
        self._probs = [prob for _, prob in ops]
        if not math.isclose(sum(self._probs), 1, rel_tol=1e-6):
            raise KeyError("The sum of probability of operators should be 1.")

        self._kraus_operators = [np.sqrt(prob) * mat for mat, prob in ops] if kraus_ops is None else kraus_ops
        self._kraus_conj_ops = [np.transpose(k).conjugate() for k in self._kraus_operators]
        if not is_kraus_ops(self._kraus_operators):
            raise KeyError("There is not a Kraus operator.")

        self._qubits = int(np.log2(self._operators[0].shape[0]))
        self._type = NoiseChannel.unitary

    def __str__(self):
        ne_str = f"{self.type.value} with {self.qubits} qubits.\n"
        for i, nm in enumerate(self._operators):
            ne_str += f"Noise with probability {self._probs[i]}: {nm}\n"

        return ne_str

    def compose(self, other):
        """ generate composed noise error with self and other. """
        assert other.qubits == self.qubits and isinstance(other, QuantumNoiseError)

        composed_ops = []
        for i, noise_matrix in enumerate(self._operators):
            self_prob = self._probs[i]
            for j, other_noise_matrix in enumerate(other.operators):
                other_prob = other.probabilties[j]
                composed_ops.append((dot(noise_matrix, other_noise_matrix), self_prob * other_prob))

        return QuantumNoiseError(composed_ops)

    def tensor(self, other):
        """ generate tensor noise error with self and other. """
        assert other.qubits == self.qubits and isinstance(other, QuantumNoiseError)

        composed_ops = []
        for i, noise_matrix in enumerate(self._operators):
            self_prob = self._probs[i]
            for j, other_noise_matrix in enumerate(other.operators):
                other_prob = other.probabilties[j]
                composed_ops.append((tensor(noise_matrix, other_noise_matrix), self_prob * other_prob))

        return QuantumNoiseError(composed_ops)

    def apply_to_gate(self, matrix: np.ndarray):
        """ generate kraus operator with given gate's matrix. """
        assert matrix.shape == (2 ** self._qubits, 2 ** self._qubits)

        return [dot(ops, matrix) for ops in self.kraus]

    def prob_mapping_operator(self, prob: float) -> np.ndarray:
        """ Return the related noise error's matrix with given probability. """
        for idx, error_prob in enumerate(self._probs):
            if prob < error_prob:
                return self._operators[idx]

            prob -= error_prob


class PauliError(QuantumNoiseError):
    """ Pauli Error; Including Bit Flip and Phase Flip

    Example:
        PauliError([('i', 0.3), ('x', 0.7)])

    Args:
        ops (List[Tuple[str, float]]): The operators for pauli error.
        num_qubits (int): The number of target qubits. Defaults to 1.
    """
    _BASED_GATE_MATRIX = {
        'i': ID.matrix,
        'x': X.matrix,
        'y': Y.matrix,
        'z': Z.matrix
    }

    def __init__(self, ops: List[Tuple[str, float]], num_qubits: int = 1):
        if not isinstance(ops, (list, tuple)):
            raise TypeError("Wrong input for Pauli Error.")

        # Building noise error operators List[(pauli_matrix, prob)].
        operators = []
        for op, prob in ops:
            if prob < 0 or prob > 1 or (len(op) != num_qubits and num_qubits > 1):
                raise KeyError("Pauli Error get wrong input.")

            based_matrix = None
            for g in op:
                if g not in list(self._BASED_GATE_MATRIX.keys()):
                    raise KeyError("Pauli Error get wrong input.")

                if based_matrix is None:
                    based_matrix = self._BASED_GATE_MATRIX[g]
                    continue

                if num_qubits > 1:
                    based_matrix = tensor(based_matrix, self._BASED_GATE_MATRIX[g])
                else:
                    based_matrix = dot(based_matrix, self._BASED_GATE_MATRIX[g])

            operators.append((based_matrix, prob))

        # Initial PauilError
        super().__init__(operators)
        self.type = NoiseChannel.pauil


class BitflipError(PauliError):
    """ Special Case for PauilError, with fixed Pauil Operator:
        [('x', prob), ('i', 1 - prob)]

    Args:
        prob (float): The probability to flip the qubit.
    """
    def __init__(self, prob: float):
        assert prob >= 0 and prob <= 1, "Wrong input for Bitflip Error."
        ops = [('i', 1 - prob), ('x', prob)]

        super().__init__(ops)


class PhaseflipError(PauliError):
    """ Special Case for PauilError, with fixed Pauil Operator:
        [('z', prob), ('i', 1 - prob)]

    Args:
        prob (float): The probability to flip the phase.
    """
    def __init__(self, prob: float):
        assert prob >= 0 and prob <= 1, "Wrong input for Phaseflip Error."
        ops = [('i', 1 - prob), ('z', prob)]

        super().__init__(ops)


class PhaseBitflipError(PauliError):
    """ Special Case for PauilError, with fixed Pauil Operator:
        [('y', prob), ('i', 1 - prob)]

    Args:
        prob (float): The probability to flip the qubit and phase.
    """
    def __init__(self, prob: float):
        assert prob >= 0 and prob <= 1, "Wrong input for PhaseBitflip Error."
        ops = [('i', 1 - prob), ('y', prob)]

        super().__init__(ops)


class DepolarizingError(PauliError):
    """ The Depolarizing Error

    Args:
        prob (float): The probability of depolarizing.
        num_qubits (int, optional): The number of qubits have depolarizing error. Defaults to 1.
    """
    def __init__(self, prob: float, num_qubits: int = 1):
        if not isinstance(prob, float) and not isinstance(num_qubits, int):
            raise TypeError("Wrong input for Depolarizing Error.")

        assert num_qubits >= 1, "number of qubits must be positive integer."
        num_ops = 4 ** num_qubits
        max_prob = num_ops / (num_ops - 1)
        if prob < 0 or prob > max_prob:
            raise KeyError(f"Depolarizing prob must between 0 and {max_prob}")

        probs = [1 - prob / max_prob] + [prob / num_ops] * (num_ops - 1)
        ops = [''.join(i) for i in product(self._BASED_GATE_MATRIX.keys(), repeat=num_qubits)]

        super().__init__(list(zip(ops, probs)), num_qubits)
        self.type = NoiseChannel.depolarizing


class DampingError(QuantumNoiseError):
    """ Amplitude Damping, Phase Damping and Amp-Phase Damping

        a = amp, b = phase, p = state prob \n
        A0 = sqrt(1 - p1) * [[1, 0], [0, sqrt(1 - a - b)]] \n
        A1 = sqrt(1 - p1) * [[0, sqrt(a)], [0, 0]] \n
        A2 = sqrt(1 - p1) * [[0, 0], [0, sqrt(b)]] \n
        B0 = sqrt(p1) * [[sqrt(1 - a - b), 0], [0, 1]] \n
        B1 = sqrt(p1) * [[0, 0], [sqrt(a), 0]] \n
        B2 = sqrt(p1) * [[sqrt(b), 0], [0, 0]] \n

    Args:
        amplitude_prob (float): The probability for damping amplitude.
        phase_prob (float): The probability for damping phase.
        dissipation_state (float, optional): The dissipation states. Defaults to 0.0.
    """
    def __init__(self, amplitude_prob: float, phase_prob: float, dissipation_state: float = 0.0):
        assert amplitude_prob >= 0 and amplitude_prob <= 1, \
            f"Amplitude prob must between 0 and 1, not {amplitude_prob}."
        assert phase_prob >= 0 and phase_prob <= 1, f"Phase prob must between 0 and 1, not {phase_prob}."
        assert dissipation_state >= 0 and dissipation_state <= 1, \
            f"state prob must between 0 and 1, not {dissipation_state}."

        if amplitude_prob + phase_prob > 1:
            raise KeyError("Invalid amplitude and phase damping prob, the sum cannot greater than 1.")

        self.amplitude_prob = amplitude_prob
        self.phase_prob = phase_prob
        self.dissipation_state = dissipation_state

        operators, kraus_ops = self._create_kraus_ops()
        super().__init__(operators, kraus_ops)
        self.type = NoiseChannel.damping

    def __str__(self):
        damp_noise = f"{self.type.value} with 1 qubit\n"
        if self.amplitude_prob != 0:
            damp_noise += f"amplitude damping prob: {self.amplitude_prob} "

        if self.phase_prob != 0:
            damp_noise += f"phase damping prob: {self.phase_prob} "

        if self.dissipation_state != 0:
            damp_noise += f"prob of stable state: {self.dissipation_state}"

        return damp_noise

    def _create_kraus_ops(self):
        """ Create damping Kraus operators. """
        m0, m1 = np.sqrt(1 - self.dissipation_state), np.sqrt(self.dissipation_state)
        sqrt_amp, sqrt_phase = np.sqrt(self.amplitude_prob), np.sqrt(self.phase_prob)
        sqrt_ap = np.sqrt(1 - self.amplitude_prob - self.phase_prob)

        k0 = m0 * np.array([[1, 0], [0, sqrt_ap]], dtype=np.complex128)
        k1 = m0 * np.array([[0, sqrt_amp], [0, 0]], dtype=np.complex128)
        k2 = m0 * np.array([[0, 0], [0, sqrt_phase]], dtype=np.complex128)
        k3 = m1 * np.array([[sqrt_ap, 0], [0, 1]], dtype=np.complex128)
        k4 = m1 * np.array([[0, 0], [sqrt_amp, 0]], dtype=np.complex128)
        k5 = m1 * np.array([[sqrt_phase, 0], [0, 0]], dtype=np.complex128)
        kraus = [k0, k1, k2, k3, k4, k5]

        probs = [a * b for a, b in product(
            [1 - self.dissipation_state, self.dissipation_state],
            [1 - self.amplitude_prob - self.phase_prob, self.amplitude_prob, self.phase_prob]
        )]
        based_operator, kraus_operator = [], []
        for idx, prob in enumerate(probs):
            if prob != 0:
                based_operator.append((kraus[idx], probs[idx]))
                kraus_operator.append(kraus[idx])

        return based_operator, kraus_operator
