"""
(Temporary) implementation of Directed Acyclic Graph (DAG)
based on networkx for the use in template_matching
"""

import queue
import networkx as nx
import matplotlib.pyplot as plt


class DAGNode(object):
    """
    Class for Node in the DAG

    In practical use, a node could have more attributes (as in DAGDepNode).
    Here we emphasize the existence of node_id for the convenience to index it,
    which would be useful later. In further (perhaps) C++ implementation,
    similar attribute should also be reserved.
    """
    def __init__(self, node, node_id):
        """
        Create a node in the DAG

        Args:
            node(Any): Information of this node except for node_id,
                        just an abstraction here
            node_id(int): ID of this node
        """
        assert isinstance(node_id, int), "node_id must be an integer"
        self.node = node
        self.node_id = node_id


class DAG(object):
    """
    Directed Acyclic Graph (Temporary implementation by networkx.DiGraph)
    """
    def __init__(self):
        """
        Initialize an empty DAG
        """
        self._graph = nx.DiGraph()

    def __getitem__(self, node_id):
        """
        Index the node and edge by node_id and 2-Tuple of node_id respectively
        """
        if isinstance(node_id, int):
            assert node_id in self.nodes(), "Invalid node_id"
            return self._graph.nodes[node_id]
        elif isinstance(node_id, tuple):
            assert len(node_id) == 2, "Incorrect length of node_id tuple(expected 2)"
            src, dest = node_id
            assert src in self.nodes(), "Invalid node_id of source"
            assert dest in self.nodes(), "Invalid node_id of destination"
            return self._graph.edges[src, dest]

    def draw(self, filename='a.jpg', layout=nx.shell_layout):
        """
        Draw the graph with matplotlib
        Args:
            layout(callable): Choose a layout of nodes

            Possible choice list in networkx:
            bipartite_layout, circular_layout, kamada_kawai_layout,
            planar_layout, random_layout, rescale_layout, shell_layout,
            spring_layout, spectral_layout, spiral_layout, multipartite_layout
        """
        nx.draw(self._graph, with_labels=True, pos=layout(self._graph))
        plt.savefig(filename)

    """
    Nodes and Edges
    """
    def nodes(self):
        """
        Returns:
            List of all nodes in the graph
        """
        return list(self._graph.nodes)

    def __len__(self):
        """
        Returns:
            Number of the nodes in the graph
        """
        return self._graph.number_of_nodes()

    def get_node_data(self, node_id):
        """
        Retrieve the data stored in the given node

        Args:
            node_id(int): Processing node
        Returns:
            DAGNode-like object
        """
        return self._graph.nodes[node_id]["node"]

    def edges(self):
        """
        Returns:
            List of all edges in the graph
        """
        return list(self._graph.edges)

    def out_edges(self, node_id):
        """
        Args:
            node_id: Processing node
        Returns:
            List: Out edges starting from given node
        """
        return self._graph.out_edges(node_id)

    def in_edges(self, node_id):
        """
        Args:
            node_id: Processing node
        Returns:
            List: In edges ending in given node
        """
        return self._graph.in_edges(node_id)

    def out_degree(self, node_id):
        """
        Args:
            node_id: Processing node
        Returns:
            int: Out degree of given node
        """
        return self._graph.out_degree(node_id)

    def in_degree(self, node_id):
        """
        Args:
            node_id: Processing node
        Returns:
            int: In degree of given node
        """
        return self._graph.in_degree(node_id)

    """
    Add node(s) and edge(s) by networkx method
    """
    def add_node(self, node):
        """
        Args:
            node: Node to be added
        """
        assert hasattr(node, "node_id"), "No node_id found"
        assert node.node_id not in self.nodes(), "Replicated node_id"
        self._graph.add_node(node.node_id, node=node)

    def add_nodes_from(self, nodes):
        """
        Args:
            nodes(list): Nodes to be added
        """
        nodes_for_adding = []
        for node in nodes:
            assert hasattr(node, "node_id"), "No node_id found"
            assert node.node_id not in self.nodes(), "Replicated node_id"
            nodes_for_adding.append((node.node_id, {"node": node}))
        self._graph.add_nodes_from(nodes_for_adding)

    def add_edge(self, src, dest):
        """
        Args:
            src: Source node of edge to be added
            dest: Destination node of edge to be added
        """
        self._graph.add_edge(src, dest)

    def add_edges_from(self, edges):
        """
        Args:
            edges(list): Edges to be added
        """
        self._graph.add_edges_from(edges)

    """
    Successors and Predecessors
    """
    def successors(self, node_id):
        """
        Warning: This function evaluates the Direct Successors of given node,
        for the Successors set in the paper, use descendants() instead

        Args:
            node_id(int): Processing node
        Returns:
            List: Direct successors of node
        """
        return list(self._graph.successors(node_id))

    def descendants(self, node_id):
        """
        Evaluates the Successors set in the paper (BFS)

        Args:
            node_id(int): Processing node
        Returns:
            List: Successors of node
        """
        desc = []
        visited = set()
        q = queue.Queue()
        q.put(node_id)

        while not q.empty():
            current_node = q.get()
            for successor in self._graph.successors(current_node):
                if successor not in visited:
                    desc.append(successor)
                    q.put(successor)
                    visited.add(successor)
        return desc

    def predecessors(self, node_id):
        """
        Warning: This function evaluates the Direct Predecessors of given node,
        for the Predecessors set in the paper, use ancestors() instead

        Args:
            node_id(int): Processing node
        Returns:
            List: Direct predecessors of node
        """
        return list(self._graph.predecessors(node_id))

    def ancestors(self, node_id):
        """
        Evaluates the Predecessors set in the paper (BFS)

        Args:
            node_id(int): Processing node
        Returns:
            List: Predecessors of node
        """
        ance = []
        visited = set()
        q = queue.Queue()
        q.put(node_id)

        while not q.empty():
            current_node = q.get()
            for predecessor in self._graph.predecessors(current_node):
                if predecessor not in visited:
                    ance.append(predecessor)
                    q.put(predecessor)
                    visited.add(predecessor)
        return ance

    """
    Correctness and topological sort of DAG
    """
    def isDAG(self):
        """
        Judge whether the given graph is a DAG

        Returns:
            True if the graph is a DAG, False if not
        """
        try:
            _ = self.topological_sort()
        except ValueError:
            return False
        else:
            return True

    def topological_sort(self):
        """
        Sort nodes in topological order.

        Returns:
            List: nodes in topological order
        """
        indegree_map = {v: d for v, d in self._graph.in_degree() if d > 0}
        # These nodes have zero indegree and ready to be returned.
        zero_indegree = [v for v, d in self._graph.in_degree() if d == 0]

        node_list = []
        while zero_indegree:
            node = zero_indegree.pop()
            for _, child in self._graph.edges(node):
                indegree_map[child] -= 1
                if indegree_map[child] == 0:
                    zero_indegree.append(child)
                    del indegree_map[child]
            node_list.append(node)

        if indegree_map:
            raise ValueError("Graph contains a cycle")
        return node_list
