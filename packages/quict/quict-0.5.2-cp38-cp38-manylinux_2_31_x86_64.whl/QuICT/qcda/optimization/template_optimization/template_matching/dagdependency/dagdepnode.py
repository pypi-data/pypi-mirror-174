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

# pylint: disable=redefined-builtin

"""Object to represent the information at a node in the DAGCircuit."""


class DAGDepNode:
    """Object to represent the information at a node in the DAGDependency().

    It is used as the return value from `*_nodes()` functions and can
    be supplied to functions that take a node.
    """

    __slots__ = ['gate', 'name', 'cargs', 'targs', 'qargs', 'node_id', 'successors',
                 'predecessors', 'reachable', 'matchedwith', 'isblocked', 'successorstovisit']

    def __init__(
        self,
        gate=None,
        qargs=None,
        successors=None,
        predecessors=None,
        reachable=None,
        matchedwith=None,
        successorstovisit=None,
        isblocked=None,
        nid=-1
    ):

        self.gate = gate
        self.name = gate.qasm_name if gate is not None else 'Error'
        self.qargs = qargs if qargs is not None else []
        control = self.gate.controls if gate is not None else 0
        self.cargs = self.qargs[:control]
        self.targs = self.qargs[control::]
        self.node_id = nid
        self.successors = successors if successors is not None else []
        self.predecessors = predecessors if predecessors is not None else []
        self.reachable = reachable
        self.matchedwith = matchedwith if matchedwith is not None else []
        self.isblocked = isblocked
        self.successorstovisit = successorstovisit if successorstovisit is not None else []

    @staticmethod
    def semantic_eq(node1, node2):
        """
        Check if DAG nodes are considered equivalent, e.g., as a node_match for nx.is_isomorphic.

        Args:
            node1 (DAGDepNode): A node to compare.
            node2 (DAGDepNode): The other node to compare.

        Return:
            Bool: If node1 == node2
        """
        # For barriers, qarg order is not significant so compare as sets
        if node1.name == node2.name == 'barrier':
            return set(node1.targs) == set(node2.targs)
        result = False
        if node1.name == node2.name:
            if node1.cargs == node2.cargs:
                if node1.targs == node2.targs:
                    result = True
        return result

    def copy(self):
        """
        Function to copy a DAGDepNode object.
        Returns:
            DAGDepNode: a copy of a DAGDepNode objectto.
        """

        dagdepnode = DAGDepNode()

        dagdepnode.gate = self.gate
        dagdepnode.name = self.name
        dagdepnode.qargs = self.qargs
        dagdepnode.cargs = self.cargs
        dagdepnode.targs = self.targs
        dagdepnode.node_id = self.node_id
        dagdepnode.successors = self.successors
        dagdepnode.predecessors = self.predecessors
        dagdepnode.reachable = self.reachable
        dagdepnode.isblocked = self.isblocked
        dagdepnode.successorstovisit = self.successorstovisit
        dagdepnode.matchedwith = self.matchedwith.copy()

        return dagdepnode
