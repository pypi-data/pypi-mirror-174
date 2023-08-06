# !/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2021/4/27 2:02 下午
# @Author  : Han Yu
# @File    : _simulator
import numpy as np
from typing import Union

from QuICT.core import Circuit
from QuICT.core.noise import NoiseModel
from QuICT.simulation.state_vector import CircuitSimulator
from QuICT.simulation.unitary import UnitarySimulator
from QuICT.simulation.density_matrix import DensityMatrixSimulation
from QuICT.simulation.utils import Result, options_validation


class Simulator:
    """ The high-level simulation class, including all QuICT simulator mode.

    Args:
        device (str): The device of the simulator. One of [CPU, GPU]
        backend (str): The backend for the simulator. One of [unitary, state_vector, density_matrix]
        shots (int): The running times; must be a positive integer, default to 1.
        precision (str): The precision of simulator, one of [single, double], default to double.
        circuit_record (bool): whether record circuit's qasm in output, default to False.
        amplitude_record (bool): whether record the amplitude of qubits, default to False.
        **options (dict): other optional parameters for the simulator.
    """

    __DEVICE = ["CPU", "GPU"]
    __BACKEND = ["unitary", "state_vector", "density_matrix"]

    def __init__(
        self,
        device: str = "CPU",
        backend: str = None,
        shots: int = 1,
        precision: str = "double",
        circuit_record: bool = False,
        amplitude_record: bool = True,
        **options
    ):
        assert device in Simulator.__DEVICE, "Device should be one of [CPU, GPU]."
        self._device = device
        if backend is not None:
            assert backend in Simulator.__BACKEND, "backend should be one of [unitary, state_vector, density_matrix]."
        self._backend = backend
        self._precision = precision

        assert (shots >= 1)
        self._shots = shots
        if options_validation(options=options, device=self._device, backend=self._backend):
            self._options = options
        else:
            raise KeyError(f"Unmatched options arguments depending on {self._device} and {self._backend}.")

        # Result's arguments
        self._circuit_record = circuit_record
        self._amplitude_record = amplitude_record

    def _load_simulator(self):
        """ Initial simulator. """
        if self._device == "GPU":
            from QuICT.simulation.state_vector import ConstantStateVectorSimulator

        if self._backend == "state_vector":
            simulator = ConstantStateVectorSimulator(precision=self._precision, **self._options) \
                if self._device == "GPU" else CircuitSimulator(precision=self._precision)
        else:
            if self._backend == "unitary":
                simulator = UnitarySimulator(device=self._device, precision=self._precision)
            else:
                simulator = DensityMatrixSimulation(device=self._device, precision=self._precision)

        return simulator

    def run(
        self,
        circuit: Union[Circuit, np.ndarray],
        state_vector: np.ndarray = None,
        density_matrix: np.ndarray = None,
        noise_model: NoiseModel = None,
        use_previous: bool = False
    ):
        """ start simulator with given circuit

        Args:
            circuit Union[Circuit, np.ndarray]: The quantum circuits or unitary matrix.
            state_vector (ndarray): The initial state vector.
            density_matrix (ndarray): The initial density matrix.
            noise_model (NoiseModel, optional): The NoiseModel only for density_matrix simulator. Defaults to None.
            use_previous (bool, optional): Using the previous state vector. Defaults to False.

        Yields:
            [dict]: The Result Dict.
        """
        if not isinstance(circuit, Circuit):
            self._backend = "unitary"
        elif density_matrix is not None or noise_model is not None:
            self._backend = "density_matrix"

        if self._backend is None:
            self._backend = "state_vector"

        circuit_name = circuit.name if isinstance(circuit, Circuit) else ""
        result = Result(circuit_name, self._device, self._backend, self._shots, self._options)
        if self._circuit_record and circuit is not None:
            result.record_circuit(circuit)

        simulator = self._load_simulator()
        if self._backend == "density_matrix":
            amplitude = simulator.run(circuit, density_matrix, noise_model, use_previous)
        else:
            amplitude = simulator.run(circuit, state_vector, use_previous)

        result.record_amplitude(amplitude, self._amplitude_record)

        sample_result = simulator.sample(self._shots)
        result.record_sample(sample_result)

        return result.__dict__()
