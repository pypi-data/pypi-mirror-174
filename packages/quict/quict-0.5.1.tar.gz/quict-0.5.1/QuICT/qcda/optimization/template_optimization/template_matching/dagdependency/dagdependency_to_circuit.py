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

"""Helper function for converting a dag dependency to a circuit"""
from QuICT.core import *    # pylint: disable=unused-wildcard-import


def dagdependency_to_circuit(dagdependency):
    """Build a ``Circuit`` object from a ``DAGDependency``.

    Args:
        dagdependency (DAGDependency): the input dag.

    Return:
        Circuit: the circuit representing the input dag dependency.
    """

    circuit = Circuit(dagdependency.num_qubits)
    circuit.name = dagdependency.name or None

    for node_id in dagdependency.get_nodes():
        node = dagdependency.get_node(node_id)
        circuit.gates.append(node.gate)

    return circuit
