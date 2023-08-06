# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Modification Notice: Code revised for QuICT

'''Helper function for converting a circuit to a dag dependency'''

from .dagdependency import DAGDependency


def circuit_to_dagdependency(circuit):
    """Build a ``DAGDependency`` object from a ``Circuit``.

    Args:
        circuit (Circuit): the input circuits.

    Return:
        DAGDependency: the DAG representing the input circuit as a dag dependency.
    """
    dagdependency = DAGDependency()
    dagdependency.name = circuit.name
    dagdependency.num_qubits = len(circuit.qubits)

    supported_gates = ['h', 's', 'sdg', 'x', 'y', 'z', 'id', 't', 'tdg', 'cx', 'ccx']
    for nid, gate in enumerate(circuit.gates):
        # TODO: More gates allowed here, if the _does_commute() and gate.soft_compare() are done
        assert gate.qasm_name in supported_gates, \
            "Invalid gate in the circuit(only non-param 1-qubit gate, CNOT and Toffoli allowed)"
        dagdependency.add_op_node(gate, gate.cargs + gate.targs, nid)

    dagdependency._add_successors()

    return dagdependency
