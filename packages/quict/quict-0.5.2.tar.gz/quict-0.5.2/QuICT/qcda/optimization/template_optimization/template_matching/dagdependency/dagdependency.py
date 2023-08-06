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

"""DAGDependency class for representing non-commutativity in a circuit.
"""

import heapq
import numpy as np

from .diagraph import DAG
from .dagdepnode import DAGDepNode


class DAGDependency:
    """Object to represent a quantum circuit as a directed acyclic graph
    via operation dependencies (i.e. lack of commutation).

    The nodes in the graph are operations represented by quantum gates.
    The edges correspond to non-commutation between two operations
    (i.e. a dependency). A directed edge from node A to node B means that
    operation A does not commute with operation B.
    The object's methods allow circuits to be constructed.

    The nodes in the graph have the following attributes:
    'operation', 'successors', 'predecessors'.

    **Example:**

    Bell circuit with no measurement.

    .. parsed-literal::

              ┌───┐
        qr_0: ┤ H ├──■──
              └───┘┌─┴─┐
        qr_1: ─────┤ X ├
                   └───┘

    The dependency DAG for the above circuit is represented by two nodes.
    The first one corresponds to Hadamard gate, the second one to the CNOT gate
    as the gates do not commute there is an edge between the two nodes.

    **Reference:**

    [1] Iten, R., Moyard, R., Metger, T., Sutter, D. and Woerner, S., 2020.
    Exact and practical pattern matching for quantum circuit optimization.
    `arXiv:1909.05270 <https://arxiv.org/abs/1909.05270>`_

    """

    def __init__(self):
        """
        Create an empty DAGDependency.
        """
        # Circuit name
        self.name = None

        # Number of qubits
        self.num_qubits = 0

        # Directed graph whose nodes are gates and edges
        # represent non-commutativity between two gates.
        self._graph = DAG()

    def size(self):
        """ Returns the number of gates in the circuit"""
        return len(self._graph)

    def _add_graph_node(self, node):
        """
        Args:
            node (DAGDepNode): considered node.

        Returns:
            node_id(int): corresponding label to the added node.
        """
        self._graph.add_node(node)

    def get_nodes(self):
        """
        Returns:
            generator(dict): iterator over all the nodes.
        """
        return iter(self._graph.nodes())

    def get_node(self, node_id):
        """
        Args:
            node_id (int): label of considered node.

        Returns:
            node: corresponding to the label.
        """
        return self._graph.get_node_data(node_id)

    def _add_graph_edge(self, src_id, dest_id):
        """
        Function to add an edge from given data (dict) between two nodes.

        Args:
            src_id (int): label of the first node.
            dest_id (int): label of the second node.
            data (dict): data contained on the edge.

        """
        self._graph.add_edge(src_id, dest_id)

    def get_all_edges(self):
        """
        Enumaration of all edges.

        Returns:
            List: corresponding to the label.
        """

        return [(src, dest)
                for src_node in self._graph.nodes()
                for (src, dest)
                in self._graph.out_edges(src_node)]

    def get_in_edges(self, node_id):
        """
        Enumeration of all incoming edges for a given node.

        Args:
            node_id (int): label of considered node.

        Returns:
            List: corresponding incoming edges data.
        """
        return self._graph.in_edges(node_id)

    def get_out_edges(self, node_id):
        """
        Enumeration of all outgoing edges for a given node.

        Args:
            node_id (int): label of considered node.

        Returns:
            List: corresponding outgoing edges data.
        """
        return self._graph.out_edges(node_id)

    def direct_successors(self, node_id):
        """
        Direct successors id of a given node as sorted list.

        Args:
            node_id (int): label of considered node.

        Returns:
            List: direct successors id as a sorted list
        """
        return sorted(self._graph.successors(node_id))

    def direct_predecessors(self, node_id):
        """
        Direct predecessors id of a given node as sorted list.

        Args:
            node_id (int): label of considered node.

        Returns:
            List: direct predecessors id as a sorted list
        """
        return sorted(self._graph.predecessors(node_id))

    def successors(self, node_id):
        """
        Successors id of a given node as sorted list.

        Args:
            node_id (int): label of considered node.

        Returns:
            List: all successors id as a sorted list
        """
        return self._graph.get_node_data(node_id).successors

    def predecessors(self, node_id):
        """
        Predecessors id of a given node as sorted list.

        Args:
            node_id (int): label of considered node.

        Returns:
            List: all predecessors id as a sorted list
        """
        return self._graph.get_node_data(node_id).predecessors

    def add_op_node(self, gate, qargs, nid):
        """Add a DAGDepNode to the graph and update the edges.

        Args:
            gate (gate): quantum gate
            qargs (list[Qubit]): qubits of the gate
            nid (int): the node_id of given gate(by the sequence of performation)
        """

        new_node = DAGDepNode(gate=gate, qargs=qargs, successors=[],
                              predecessors=[], nid=nid)
        self._add_graph_node(new_node)
        self._update_edges()

    def _gather_pred(self, node_id, direct_pred):
        """Function set an attribute predecessors and gather multiple lists
        of direct predecessors into a single one.

        Args:
            node_id (int): label of the considered node in the DAG
            direct_pred (list): list of direct successors for the given node

        Returns:
            DAGDependency: A multigraph with update of the attribute ['predecessors']
            the lists of direct successors are put into a single one
        """
        gather = self._graph
        gather.get_node_data(node_id).predecessors = []
        for d_pred in direct_pred:
            gather.get_node_data(node_id).predecessors.append([d_pred])
            pred = self._graph.get_node_data(d_pred).predecessors
            gather.get_node_data(node_id).predecessors.append(pred)
        return gather

    def _gather_succ(self, node_id, direct_succ):
        """
        Function set an attribute successors and gather multiple lists
        of direct successors into a single one.

        Args:
            node_id (int): label of the considered node in the DAG
            direct_succ (list): list of direct successors for the given node

        Returns:
            MultiDiGraph: with update of the attribute ['predecessors']
            the lists of direct successors are put into a single one
        """
        gather = self._graph
        for d_succ in direct_succ:
            gather.get_node_data(node_id).successors.append([d_succ])
            succ = gather.get_node_data(d_succ).successors
            gather.get_node_data(node_id).successors.append(succ)
        return gather

    def _list_pred(self, node_id):
        """
        Use _gather_pred function and merge_no_duplicates to construct
        the list of predecessors for a given node.

        Args:
            node_id (int): label of the considered node
        """
        direct_pred = self.direct_predecessors(node_id)
        self._graph = self._gather_pred(node_id, direct_pred)
        self._graph.get_node_data(node_id).predecessors = list(
            merge_no_duplicates(*(self._graph.get_node_data(node_id).predecessors)))

    def _update_edges(self):
        """
        Function to verify the commutation relation and reachability
        for predecessors, the nodes do not commute and
        if the predecessor is reachable. Update the DAGDependency by
        introducing edges and predecessors(attribute)
        """
        max_node_id = len(self._graph) - 1
        max_node = self._graph.get_node_data(max_node_id)

        for current_node_id in range(0, max_node_id):
            self._graph.get_node_data(current_node_id).reachable = True
        # Check the commutation relation with reachable node, it adds edges if it does not commute
        for prev_node_id in range(max_node_id - 1, -1, -1):
            if self._graph.get_node_data(prev_node_id).reachable and not _does_commute(
                    self._graph.get_node_data(prev_node_id), max_node):
                self._graph.add_edge(prev_node_id, max_node_id)
                self._list_pred(max_node_id)
                list_predecessors = self._graph.get_node_data(max_node_id).predecessors
                for pred_id in list_predecessors:
                    self._graph.get_node_data(pred_id).reachable = False

    def _add_successors(self):
        """
        Use _gather_succ and merge_no_duplicates to create the list of successors
        for each node. Update DAGDependency 'successors' attribute. It has to
        be used when the DAGDependency() object is complete (i.e. converters).
        """
        for node_id in range(len(self._graph) - 1, -1, -1):
            direct_successors = self.direct_successors(node_id)

            self._graph = self._gather_succ(node_id, direct_successors)

            self._graph.get_node_data(node_id).successors = list(
                merge_no_duplicates(*self._graph.get_node_data(node_id).successors))

    def copy(self):
        """
        Function to copy a DAGDependency object.
        Returns:
            DAGDependency: a copy of a DAGDependency object.
        """

        dag = DAGDependency()
        dag.name = self.name

        for node_id in self.get_nodes():
            node = self._graph.get_node_data(node_id)
            dag._graph.add_node(node)
        for edges in self.get_all_edges():
            dag._graph.add_edge(edges[0], edges[1])
        return dag


def merge_no_duplicates(*iterables):
    """Merge K list without duplicate using python heapq ordered merging

    Args:
        *iterables: A list of k sorted lists

    Yields:
        Iterator: List from the merging of the k ones (without duplicates
    """
    last = object()
    for val in heapq.merge(*iterables):
        if val != last:
            last = val
            yield val


def _does_commute(node1, node2):
    """Function to verify commutation relation between two nodes in the DAG.

    Args:
        node1 (DAGnode): first node operation
        node2 (DAGnode): second node operation

    Return:
        bool: True if the nodes commute and false if it is not the case.
    """

    # return True if the qubits do not intersect
    if not set(node1.qargs) & set(node2.qargs):
        return True

    def _matrix_commute(mat1, mat2):
        mat12 = np.dot(mat1.reshape([2, 2]), mat2.reshape([2, 2]))
        mat21 = np.dot(mat2.reshape([2, 2]), mat1.reshape([2, 2]))
        return np.allclose(mat12, mat21)

    # Double 1-qubit gates: simply compute the matrices
    if node1.gate.is_single() and node2.gate.is_single():
        return _matrix_commute(node1.gate.matrix, node2.gate.matrix)

    # One 1-qubit gate and one controlled gate
    # Be aware that by construction, not is_single() just means
    # is_control_single() or is_ccx()
    # Assume node1 is the 1-qubit gate, otherwise exchange them
    if not node1.gate.is_single() and node2.gate.is_single():
        node1, node2 = node2, node1
    if node1.gate.is_single() and not node2.gate.is_single():
        # Here are two cases
        if node1.targs[0] in node2.cargs:
            # Only S, S_dagger, Z, T, T_dagger allowed here
            # (they only change the phase of |1>)
            if node1.name in ['s', 'sdg', 'z', 't', 'tdg']:
                return True
            else:
                return False
        if node1.targs[0] in node2.targs:
            # Now the matrix must commute
            return _matrix_commute(node1.gate.target_matrix, node2.gate.target_matrix)

    # Double controlled gates
    # TODO: More precise judgment needed, here only the CX gate and CCX gate
    # are guarantee to be dealt with correctly(therefore they are the only
    # allowed gate in the circuit)
    if not node1.gate.is_single() and not node2.gate.is_single():
        if not set(node1.cargs) & set(node2.targs) and\
           not set(node2.cargs) & set(node1.targs):
            return True
        else:
            return False
