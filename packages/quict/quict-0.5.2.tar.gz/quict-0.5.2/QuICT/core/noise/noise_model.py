from numpy.random import random
from copy import deepcopy
from typing import Union, List
from collections import defaultdict

from .noise_error import QuantumNoiseError
from .readout_error import ReadoutError
from QuICT.core.gate import BasicGate, GateType, GATE_TYPE_TO_CLASS
from QuICT.core.operator import NoiseGate


class NoiseModel:
    """
    The Noise Model, which contains the QuantumNoiseErrors and can translated circuit with the given QuantumNoiseError.

    Args:
        name (str, optional): The name of this NoiseModel. Defaults to "Noise Model".
        basic_gates (List, optional): The list of quantum gates will apply the NoiseError.
            Defaults to GateType.__members__.keys().
    """
    def __init__(self, name: str = "Noise Model", basic_gates: List = GateType.__members__.keys()):
        self._name = name
        self._basic_gates = list(basic_gates)

        # self._instruction stores the mapping of NoiseError and its limitation of Gates and Qubits.
        # Dict{"specific": List[Tuple(NoiseError, Qubits, Gates)],
        #      "all-qubits": List[Tuple(NoiseError, Gates)],
        #      "readout": List[ReadoutError]}
        self._instruction = defaultdict(list)
        self._all_qubits_error_gates = []   # Collect all-qubits NoiseError's gate type
        self._specified_error_gates = []    # Collect specified-qubits NoiseError's gate type
        self._readout_errors = []           # Collect Readout Error's qubits

    def __str__(self):
        nm_str = f"{self._name}:\nBasic Gates: {self._basic_gates}\nNoise Errors:\n"
        if self._all_qubits_error_gates:
            nm_str += f"Gates with all qubits: {set(self._all_qubits_error_gates)}\n"

        if self._specified_error_gates:
            nm_str += "Gates with specified qubits:"
            for _, q, g in self._instruction["specific"]:
                nm_str += f"[qubits: {q}, gates: {g}] "

        if self._readout_errors:
            nm_str += "Measured Gates with Readout Error:"
            for idx, re_qubit in enumerate(self._readout_errors):
                readout_error = self._instruction["readout"][idx]
                nm_str += f"[qubits: {re_qubit}, Readout Error Prob: {readout_error.prob}]"

        return nm_str

    def _qubits_normalize(self, qubits: Union[int, List[int]]):
        if isinstance(qubits, int):
            qubits = [qubits]
        elif not isinstance(qubits, (list, tuple)):
            raise TypeError("The qubits must be interger of list[integer].")

        for q in qubits:
            if q < 0 or not isinstance(q, int):
                raise KeyError("The qubits must be positive integer.")

    def _gates_normalize(self, noise: QuantumNoiseError, gates: Union[str, List[str]]):
        assert isinstance(noise, QuantumNoiseError), "Unsupportted noise error here."
        if not gates:
            raise KeyError("Must specified quantum gates for noise model.")

        if isinstance(gates, str):
            gates = [gates]
        elif not isinstance(gates, (list, tuple)):
            raise TypeError("The gates must be string of gate of list[string].")

        for g in gates:
            if g not in self._basic_gates:
                raise KeyError(f"The gate is not in based gates. Please use one of {self._basic_gates}.")

            gate = GATE_TYPE_TO_CLASS[GateType.__members__[g]]()
            if gate.controls + gate.targets != noise.qubits:
                raise KeyError(
                    f"Un-matched qubits number between gate {gate.controls + gate.targets}" +
                    f"with noise error {noise.qubits}."
                )

    def add(self, noise: QuantumNoiseError, gates: Union[str, List[str]], qubits: Union[int, List[int]] = None):
        """ Add noise which will affect target quantum gates with special qubits in the circuit.

        Args:
            noise (QuantumNoiseError): The noise error.
            gates (Union[str, List[str]]): The affected quantum gates.
            qubits (Union[int, List[int]], optional): The affected qubits, if None, same as add_noise_for_all_qubits.
                Defaults to None.
        """
        if qubits is None:
            self.add_noise_for_all_qubits(noise, gates)
            return

        # Input normalization
        self._qubits_normalize(qubits)
        self._gates_normalize(noise, gates)

        # Add noise in the NoiseModel
        self._instruction["specific"].append((noise, qubits, gates))
        self._specified_error_gates += gates if isinstance(gates, list) else [gates]

    def add_noise_for_all_qubits(self, noise: QuantumNoiseError, gates: Union[str, List[str]]):
        """ Add noise which will affect all qubits in the circuit.

        Args:
            noise (QuantumNoiseError): The noise error
            gates (Union[str, List[str]]): The affected quantum gates.
        """
        # Input normalization
        self._gates_normalize(noise, gates)

        # Add noise in the NoiseModel
        self._instruction["all-qubits"].append((noise, gates))
        self._all_qubits_error_gates += gates if isinstance(gates, list) else [gates]

    def add_readout_error(self, noise: ReadoutError, qubits: Union[int, List[int]]):
        """ Add Readout error in the noise model.

        Example:
            1. Add 1-qubit Readout Error for all target qubits.
                noisemodel.add_readout_error(1-qubit ReadoutError, [0, 1, 2, etc])
            2. Add multi-qubits Readout Error for specified qubits (the number of qubits equal to ReadoutError.qubits).
                noisemodel.add_readout_error(multi-qubits ReadoutError, [1, 3, etc])

        Important:
            Supports to apply more than one Readout Error with the same target qubits, but do not support the
            combination of the Readout Error with the different qubits currently.

        Args:
            noise (ReadoutError): The Readout Error.
            qubits (Union[int, List[int]]): The target qubits for the Readout error
        """
        assert isinstance(noise, ReadoutError)
        if isinstance(qubits, int):
            qubits = [qubits]

        # Deal with 1-qubits ReadoutError apply for multi-qubits
        if noise.qubits == 1:
            for qubit in qubits:
                assert isinstance(qubit, int) and qubit >= 0
                self._add_readout_error(noise, qubit)

            return

        # Deal with multi-qubits ReadoutError
        assert noise.qubits == len(qubits)
        for qubit in qubits:
            assert isinstance(qubit, int) and qubit >= 0

        self._add_readout_error(noise, qubits)

    def _add_readout_error(self, noise: ReadoutError, qubit: Union[int, List[int]]):
        # Deal with Readout Error with the same qubits limitation
        if qubit in self._readout_errors:
            noise_idx = self._readout_errors.index(qubit)
            self._instruction["readout"][noise_idx] = self._instruction["readout"][noise_idx].compose(noise)

        if isinstance(qubit, int):
            qubit = [qubit]

        for qubit_key in self._readout_errors:
            if set(qubit_key) & set(qubit):
                raise ValueError("Currently do not support multi-qubits readout error combined.")

        # Append new Readout Error and qubits limitation
        self._readout_errors.append(qubit)
        self._instruction["readout"].append(noise)

    def transpile(self, circuit):
        """ Apply all noise in the Noise Model to the given circuit, replaced related gate with the NoiseGate

        Args:
            circuit (Circuit): The given circuit.

        Returns:
            Circuit: The circuit with NoiseGates
        """
        noised_circuit = deepcopy(circuit)
        for idx, gate in enumerate(circuit.gates):
            if not isinstance(gate, BasicGate):
                continue

            gate_str = gate.type.name
            noise_list = []
            if gate_str in self._all_qubits_error_gates:
                noise_list += self._kraus_matrix_for_all_qubits(gate)

            if gate_str in self._specified_error_gates:
                noise_list += self._kraus_matrix_for_specified_qubits(gate)

            if not noise_list:
                continue

            based_noise = noise_list[0]
            if len(noise_list) > 1:
                for n in noise_list[1:]:
                    based_noise = based_noise.compose(n)

            noise_gate = NoiseGate(gate, based_noise)
            noised_circuit.replace_gate(idx, noise_gate)

        return noised_circuit

    def apply_readout_error(self, qubits):
        """ Apply readout error to target qubits.

        Args:
            qubits (Qureg): The circuits' qubits.
        """
        prob = random()
        for noise_idx, qubit_idxes in enumerate(self._readout_errors):
            try:
                prob_idx = int(qubits[qubit_idxes])     # Get measured result
            except:
                continue        # do nothing if not all qubits measured

            # Depending on the Readout Error probs, find noised measured result
            readout_error = self._instruction["readout"][noise_idx]
            readout_error_probs = readout_error.prob[prob_idx]
            for idx, error_prob in enumerate(readout_error_probs):
                if prob <= error_prob:
                    noised_measured = idx
                    break
                else:
                    prob -= error_prob

            # Change truly measured result with noised measured result
            if noised_measured != prob_idx:
                for qubit_idx in qubit_idxes[::-1]:
                    qubits[qubit_idx].measured = (noised_measured & 1)
                    noised_measured >>= 1

    def _kraus_matrix_for_all_qubits(self, gate):
        gate_str = gate.type.name
        noise_list = []
        for noise, gate_list in self._instruction["all-qubits"]:
            if gate_str in gate_list:
                noise_list.append(noise)

        return noise_list

    def _kraus_matrix_for_specified_qubits(self, gate):
        gate_str = gate.type.name
        gate_idx = gate.cargs + gate.targs
        noise_list = []
        for noise, qubit, gate_list in self._instruction["specific"]:
            if isinstance(qubit, int):
                # Check 1-qubit noises
                qubit_intersection = qubit in gate_idx
            else:
                # Check multi-qubits noises
                qubit_intersection = (set(qubit) & set(gate_idx)) == set(qubit)

            if gate_str in gate_list and qubit_intersection:
                noise_list.append(noise)

        return noise_list
