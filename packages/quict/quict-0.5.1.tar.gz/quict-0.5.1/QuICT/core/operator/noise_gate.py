import numpy as np

from QuICT.core.gate import BasicGate, MatrixType
from ._operator import Operator


class NoiseGate(Operator):
    """
    The quantum gate with noise error.

    Args:
        gate (BasicGate): The quantum gate.
        error (QuantumNoiseError): The noise error.
    """
    @property
    def gate(self):
        """ The based gate. """
        return self._gate

    @property
    def gate_matrix(self):
        """ The gate's matrix. """
        return self._gate.matrix

    @property
    def type(self):
        """ The gate's type. """
        return self._gate.type

    @property
    def noise_matrix(self) -> list:
        """ The noised gate matrix. """
        return self._noise_matrix

    @property
    def noise_type(self):
        """ The type of noise error. """
        return self._error.type

    @property
    def kraus(self):
        """ The noised kraus operator """
        return self._error.kraus

    @property
    def kraus_ct(self):
        """ The noised kraus operator's conjugate transpose. """
        return self._error.kraus_ct

    def __init__(self, gate: BasicGate, error):
        assert isinstance(gate, BasicGate)
        super().__init__(gate.controls + gate.targets)
        self.targs = gate.targs
        self.cargs = gate.cargs
        self._gate = gate
        self._error = error
        self._noise_matrix = self._error.apply_to_gate(gate.matrix) if gate.matrix_type != MatrixType.special else None

    def prob_mapping_operator(self, prob: float):
        """ Return the related noise error's matrix with given probability. """
        return self._error.prob_mapping_operator(prob)

    def convert_precision(self):
        self._gate.convert_precision()
        if self._noise_matrix is not None:
            for noise_matrix in self._noise_matrix:
                noise_matrix = noise_matrix.astype(np.complex64)
