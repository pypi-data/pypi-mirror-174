from typing import Tuple, Union, List, Dict
from types import FunctionType

from QuICT.core.gate import CompositeGate, BasicGate
from ._operator import Operator


class Trigger(Operator):
    """
    The trigger for switch the dynamic circuit; contains the target qubits and
    related circuits with different state.
    """
    def __init__(
        self,
        targets: int,
        state_gate_mapping: Union[Dict[int, CompositeGate], List[CompositeGate], Tuple[CompositeGate], FunctionType]
    ):
        """
        Args:
            targets (int): The number of target qubits.
            state_gate_mapping: The mapping of state and related composite gates.
                (Union[Dict[int, CompositeGate], List[CompositeGate], Tuple[CompositeGate], FunctionType])

        Raises:
            TypeError: Error input parameters.
        """
        super().__init__(targets=targets)

        # Deal with state - compositegate mapping
        self._state_gate_mapping = {}
        if isinstance(state_gate_mapping, (list, tuple)):
            for idx, cgate in enumerate(state_gate_mapping):
                assert isinstance(cgate, (CompositeGate, BasicGate, type(None))), \
                    "Only accept CompositeGate or BasicGate for state_gate_mapping."
                self._state_gate_mapping[idx] = cgate
        elif isinstance(state_gate_mapping, dict):
            for key, value in state_gate_mapping.items():
                assert isinstance(key, int) and isinstance(value, (CompositeGate, BasicGate, type(None)))

            self._state_gate_mapping = state_gate_mapping
        elif isinstance(state_gate_mapping, FunctionType):
            self._check_function_validation(state_gate_mapping)
            self._state_gate_mapping = state_gate_mapping
        else:
            raise TypeError(
                f"The trigger's mapping should be one of [list, dict, Function], not {type(state_gate_mapping)}."
            )

    def mapping(self, state: int) -> CompositeGate:
        """ Return the related composite gate with given qubits' measured state.

        Args:
            state (int): The qubits' measured state.

        Returns:
            CompositeGate: The related composite gate.
        """
        assert state >= 0 and state < 2 ** self.targets, f"The state should between 0 and {2**self.targets}."

        if isinstance(self._state_gate_mapping, FunctionType):
            return self._state_gate_mapping(state)
        else:
            return self._state_gate_mapping[state]

    def _check_function_validation(self, state_gate_mapping):
        """ Validation the correctness of given state-composite mapping function. """
        for i in range(2 ** self.targets):
            if not isinstance(state_gate_mapping(i), (CompositeGate, BasicGate, type(None))):
                raise KeyError("The trigger's mapping should only return CompositeGate for all possible state.")
