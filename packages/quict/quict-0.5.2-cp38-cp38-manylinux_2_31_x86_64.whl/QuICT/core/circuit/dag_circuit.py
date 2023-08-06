import networkx as nx
import matplotlib.pyplot as plt

from QuICT.core.gate import BasicGate


class DAGNode:
    """ The node in DAG Circuit, represent a quantum gate in circuit.

    Args:
        id (int): The unique identity, usually be the quantum gates' index
        gate (BasicGate): The quantum gate
        successors (list, optional): The successors for nodes. Defaults to [].
        predecessors (list, optional): The predecessors for nodes. Defaults to [].
    """
    @property
    def id(self):
        return self._id

    @property
    def gate(self):
        return self._gate

    @property
    def name(self):
        return self._name

    @property
    def cargs(self):
        return self._cargs

    @property
    def targs(self):
        return self._targs

    @property
    def qargs(self):
        return self._qargs

    @property
    def successors(self):
        return self._successors

    @successors.setter
    def successors(self, sces: list):
        self._successors = sces

    @property
    def predecessors(self):
        return self._predecessors

    @predecessors.setter
    def predecessors(self, pdces: list):
        self._predecessors = pdces

    def __init__(self, id: int, gate: BasicGate, successors: list = [], predecessors: list = []):
        self._id = id
        self._gate = gate
        self._name = gate.qasm_name
        self._cargs = gate.cargs
        self._targs = gate.targs
        self._qargs = gate.cargs + gate.targs
        self._successors = successors
        self._predecessors = predecessors


class DAGCircuit:
    """ The DAG Circuit using networkx.DiGraph()

    The nodes in the graph represented the quantum gates, and the edges means the two quantum
    gates is non-commutation. In other words, a directed edge between node A with quantum gate GA
    and node B with quantum gate GB, the quantum gate GA does not commute with GB.

    The nodes in the graph have the following attributes:
    'name', 'gate', 'cargs', 'targs', 'qargs', 'successors', 'predecessors'.

    **Reference:**

    [1] Iten, R., Moyard, R., Metger, T., Sutter, D. and Woerner, S., 2020.
    Exact and practical pattern matching for quantum circuit optimization.
    `arXiv:1909.05270 <https://arxiv.org/abs/1909.05270>`_

    Args:
        circuit (Circuit): The quantum circuit.
    """
    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def width(self) -> int:
        return self._width

    def __init__(self, circuit):
        self._circuit = circuit
        self._name = f"DAG_{self._circuit.name}"
        self._size = self._circuit.size()
        self._width = self._circuit.width()
        self._graph = nx.DiGraph()
        # Build DAG Circuit
        self._to_dag_circuit()

    ####################################################################
    ############         DAGCircuit Nodes and Edges         ############
    ####################################################################
    def __getitem__(self, item):
        """ to fit the slice operator, overloaded this function.

        get a smaller qureg/qubit from this circuit

        Args:
            item(int/slice): slice passed in.
        Return:
            Qubit/Qureg: the result or slice
        """
        return self.nodes()[item]

    def nodes(self) -> list:
        """ Get all nodes in DAG.

        Returns:
            list: The list of nodes
        """
        return list(self._graph.nodes)

    def add_node(self, node: DAGNode):
        """ Add a node into DAG.

        Args:
            node (DAGNode): The DAG Node
        """
        assert isinstance(node, DAGNode)
        if not self._graph.has_node(node.id):
            self._graph.add_node(node.id, node=node)

    def get_node(self, node_id: int):
        """ Get DAG node's data.

        Args:
            node_id (int): the unique identity for node
        """
        return self._graph.nodes[node_id]["node"]

    def edges(self) -> list:
        """ Get all edges in DAG.

        Returns:
            list: The list of edges of DAG.
        """
        return list(self._graph.edges)

    def in_edges(self, node_id: int):
        """ Get all in-edges of node with given node id.

        Args:
            node_id (int): the unique identity for node
        """
        return self._graph.in_edges(node_id)

    def out_edges(self, node_id: int):
        """ Get all out-edges of node with given node id.

        Args:
            node_id (int): the unique identity for node
        """
        return self._graph.out_edges(node_id)

    ####################################################################
    ############                Circuit to DAG              ############
    ####################################################################
    def _to_dag_circuit(self):
        """ Algorithm to generate DAG circuit. """
        gates = self._circuit.gates
        endpoints = []      # The endpoint of current DAG graph
        for idx, gate in enumerate(gates):
            # Add new node into DAG Graph
            assert isinstance(gate, BasicGate), "Only support BasicGate in DAGCircuit."
            current_node = DAGNode(idx, gate)
            self.add_node(current_node)

            # Check the relationship of current node and previous node
            updated_endpoints = []
            for previous_node in endpoints:
                self._backward_trace(previous_node, current_node)
                if self._graph.edges(idx) != 0:
                    updated_endpoints.append(current_node)
                    if not self._graph.has_edge(previous_node.id, idx):
                        updated_endpoints.append(previous_node)
                else:
                    updated_endpoints.append(previous_node)

            # if no edges add, create new original node
            if self._graph.degree(idx) == 0:
                endpoints.insert(0, current_node)
            else:
                endpoints = self._endpoints_order(updated_endpoints)

        # Add successors and predecessors for all nodes
        for node_id in range(self.size):
            node_sces = self._graph.successors(node_id)
            node_pdces = self._graph.predecessors(node_id)
            self.get_node(node_id).successors = list(node_sces)
            self.get_node(node_id).predecessors = list(node_pdces)

    def _backward_trace(self, previous_node, current_node):
        """ Trace the commutation of DAG Nodes by backward way.

        Args:
            previous_node (Union[DAGNode, int]): The previous DAG node
            current_node (DAGNode): The added DAG node

        Returns:
            bool: Whether there is a edge between current node and previous
            node or its predecessors.
        """
        cgate = current_node.gate
        point = [previous_node]
        visited = [current_node.id]
        while len(point) != 0:
            pnode = point.pop()
            if isinstance(pnode, int):
                pnode = self.get_node(pnode)

            if not pnode.gate.commutative(cgate):
                self._graph.add_edge(pnode.id, current_node.id)
                # Check whether matched node's successors can have a edge with current node
                self._forward_trace(pnode, current_node, visited)

            if not self._graph.has_edge(pnode.id, current_node.id):
                pred_list = list(self._graph.predecessors(pnode.id))
                point += pred_list

            visited.append(pnode.id)

    def _forward_trace(self, previous_node, current_node, visited_nodes):
        """ Check whether previous node has a successors which can have a edge with
        current node.

        Args:
            previous_node (Union[DAGNode, int]): The previous DAG node
            current_node (DAGNode): The added DAG node
            visited_nodes (List[int]): The visited nodes' id of current node during
            the backward trace

        Returns:
            bool: Whether there is a successor node can have a edge with current node
        """
        point = list(self._graph.successors(previous_node.id))
        cgate = current_node.gate
        while len(point) != 0:
            pnode = point.pop()
            if isinstance(pnode, int):
                pnode = self.get_node(pnode)

            if pnode.id not in visited_nodes:
                if not pnode.gate.commutative(cgate):
                    self._graph.remove_edge(previous_node.id, current_node.id)
                    break

            succ_list = list(self._graph.successors(pnode.id))
            point += succ_list

    def _endpoints_order(self, endpoints: list):
        node_ids = [endpoint.id for endpoint in endpoints]
        # remove duplicated item and sort by decreasing
        node_ids = list(set(node_ids))
        node_ids.sort(reverse=True)

        return [self.get_node(nid) for nid in node_ids]

    ####################################################################
    ############              DAG_Circuit utils             ############
    ####################################################################
    def draw(self, layout=nx.shell_layout):
        """ Draw a DAG circuit, save as jpg file.

        Args:
            layout (layout, optional): The networkx.layout. Defaults to nx.shell_layout.
        """
        graph_name = f"{self.name}.jpg"
        plt.figure()
        nx.draw(self._graph, pos=layout(self._graph), with_labels=True)
        plt.savefig(graph_name)
