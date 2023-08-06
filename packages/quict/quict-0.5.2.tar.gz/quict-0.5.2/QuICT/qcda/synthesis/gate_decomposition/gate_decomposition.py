"""
Decompose gates except for BasicGates in a CompositeGate or a Circuit
"""
from QuICT.core import Circuit
from QuICT.core.gate import BasicGate, CompositeGate, UnitaryGate
from QuICT.qcda.synthesis.unitary_decomposition import UnitaryDecomposition
from QuICT.qcda.utility import OutputAligner


class GateDecomposition(object):
    """ Gate decomposition method """
    @OutputAligner()
    def execute(self, gates):
        """
        Decompose gates except for BasicGates in a CompositeGate or a Circuit
        to BasicGates with the `build_gate` method if it is implemented.
        Otherwise the `UnitaryDecomposition` would be used.

        Args:
            gates(CompositeGate/Circuit): gates to be decomposed

        Returns:
            CompositeGate: Decomposed CompositeGate

        Raises:
            If the objective could not be resolved as any of the above types.
        """
        assert isinstance(gates, CompositeGate) or isinstance(gates, Circuit),\
            TypeError('gates to be decomposed must be CompositeGate or Circuit')
        gates = CompositeGate(gates=gates.gates)

        # Decomposition of complex gates
        gates_decomposed = CompositeGate()
        for gate in gates:
            if isinstance(gate, UnitaryGate):
                UD = UnitaryDecomposition()
                gate_mat, _ = UD.execute(gate.matrix)
                gate_mat & gate.targs
                gates_decomposed.extend(gate_mat)
            elif isinstance(gate, BasicGate):
                try:
                    gates_decomposed.extend(gate.build_gate())
                except Exception:
                    gates_decomposed.append(gate)
            else:
                raise ValueError('Unknown gate encountered')

        return gates_decomposed
