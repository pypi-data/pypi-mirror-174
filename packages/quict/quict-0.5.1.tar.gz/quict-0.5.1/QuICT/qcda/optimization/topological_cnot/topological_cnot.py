#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2020/11/27 1:42
# @Author  : Han Yu
# @File    : topological_cnot.py

import numpy as np
from queue import Queue

from QuICT.core import Circuit
from QuICT.core.gate import build_gate, CX, H, GateType


class SteinerTree(object):
    """ the SteinerTree struct

    we use exponent time to construct the exact steiner tree
    # fix it with a 2-approximation polynomial algorithm

    Attributes:
        N(int): the number of vertexes in the graph.
        matrix(n * n boolean matrix): topological relationship for n vertexes,
                                      it is undirected.
        dp(n * 2^n np.array): dp array to struct the tree.
                dp[i][j] means the root is i, state is j's subtree.
                when subtree contain vertex k, j & (1 << k) != 0
        ST(list<int>): the indexes of vertexes in tree.
        father(list<int>): the father of vertexes in the tree.
        sons(list<int>): the son of vertexes in the tree.
        pre(np.array<int>): the state which update this state in dp.
        root(int): the root of the tree.
    """
    def __init__(self, n, topo):
        """
        Args:
            n(int): number of the vertexes in the tree
            topo(n * n boolean matrix): topological relationship for n vertexes,
                                      it is directed.
        """
        self.N = n
        self.matrix = [[False for _ in range(n)] for _ in range(n)]
        self.dp = np.array([], dtype=np.int64)
        self.ST = []
        for i in range(n):
            for j in range(i + 1, n):
                self.matrix[i][j] = self.matrix[j][i] = topo[i][j] or topo[j][i]
        self.father = []
        self.sons = []
        self.pre = np.array([], dtype=np.int64)
        self.root = 0

    def build_ST(self, ST_input: list, lower_bound):
        """ build Steiner_Tree with ST_input in it

        ST_input[-1] must be the root of the tree.

        Args:
            ST_input(list<int>): the indexes of vertexes which should be contained in the tree.
                                 ST_input[-1] should be the root.
            lower_bound(int): the minimum index of vertexes which can be used
        """
        size = len(ST_input)
        self.root = ST_input[-1]
        self.dp = -1 * np.ones((self.N, 1 << size))
        self.pre = np.zeros((self.N, 1 << size, 2), dtype=np.int64)
        self.ST = [0 for _ in range(self.N)]
        self.father = [-1 for _ in range(self.N)]
        self.sons = []
        for i in range(self.N):
            self.sons.append([])
        now = 0
        for i in range(size):
            self.ST[ST_input[i]] = 1 << i
            now |= self.ST[ST_input[i]]
        for i in range(lower_bound, self.N):
            self.dp[i][self.ST[i]] = 0

        que = Queue()
        for j in range(1 << size):
            vis = [0 for _ in range(self.N)]
            for i in range(lower_bound, self.N):
                if self.ST[i] != 0 and (self.ST[i] & j) == 0:
                    continue
                sub = j & (j - 1)
                while sub != 0:
                    subx = self.ST[i] | sub
                    suby = self.ST[i] | (j - sub)
                    if self.dp[i][subx] != -1 and self.dp[i][suby] != -1:
                        temp = self.dp[i][subx] + self.dp[i][suby]
                        if self.dp[i][sub] == -1 or temp < self.dp[i][sub]:
                            self.dp[i][sub] = temp
                            self.pre[i][sub][0] = subx
                            self.pre[i][sub][1] = suby

                    sub = (sub - 1) & j
                if self.dp[i][j] != -1:
                    que.put(i)
                    vis[i] = True

            while not que.empty():
                u = que.get()
                vis[u] = False
                for i in range(lower_bound, self.N):
                    if self.matrix[i][u] and self.dp[u][j] != -1:
                        temp = self.dp[u][j] + 1
                        if self.dp[i][self.ST[i] | j] == -1 or self.dp[i][self.ST[i] | j] > temp:
                            self.dp[i][self.ST[i] | j] = temp
                            self.pre[i][self.ST[i] | j][:] = [u - self.N, j]
                            if (self.ST[i] | j) != j or vis[i]:
                                continue
                            vis[i] = True
                            que.put(i)
        self.build_STtree(self.root, now)

    def build_STtree(self, root, state):
        """ build the tree with the dp and pre array

        Args:
            root(int): the i in dp[i][j]
            state(int): the j in dp[i][j]
        """
        if state == self.ST[root]:
            return
        _pre = self.pre[root][state]
        if _pre[0] == 0:
            return
        if _pre[0] > 0:
            self.build_STtree(root, _pre[0])
            self.build_STtree(root, _pre[1])
        else:
            self.sons[root].append(_pre[0] + self.N)
            self.father[_pre[0] + self.N] = root
            self.build_STtree(_pre[0] + self.N, _pre[1])

    def elimination_below(self, gauss_elimination: list, gates: list):
        """ elimination with some rows below ith row and ith column.

        Args:
            gauss_elimination(list<int>): the equations should be changed in the process.
        """

        self._elimination_below_dfs(self.root, gauss_elimination, gates)

    def _elimination_below_dfs(self, now, gauss_elimination: list, gates: list):
        """ elimination with dfs

        Args:
            now(int): vertex now
            gauss_elimination(list<int>): the equations should be changed in the process.
        """
        for son in self.sons[now]:
            if self.ST[son] == 0:
                gauss_elimination[son] ^= gauss_elimination[now]
                gate = build_gate(GateType.cx, [now, son])
                gates.append(gate)
            self._elimination_below_dfs(son, gauss_elimination, gates)
        if now != self.root:
            gauss_elimination[now] ^= gauss_elimination[self.father[now]]
            gate = build_gate(GateType.cx, [self.father[now], now])
            gates.append(gate)

    def elimination_above(self, gauss_elimination: list, gates: list):
        self._elimination_above_preorder(self.root, gauss_elimination, gates)
        self._elimination_above_postorder(self.root, gauss_elimination, gates)

    def _elimination_above_preorder(self, now, gauss_elimination: list, gates: list):
        for son in self.sons[now]:
            if self.ST[son] == 0:
                gauss_elimination[now] ^= gauss_elimination[son]
                gate = build_gate(GateType.cx, [son, now])
                gates.append(gate)

        for son in self.sons[now]:
            self._elimination_above_preorder(son, gauss_elimination, gates)

    def _elimination_above_postorder(self, now, gauss_elimination: list, gates: list):
        for son in self.sons[now]:
            self._elimination_above_postorder(son, gauss_elimination, gates)
        if now != self.root:
            gauss_elimination[self.father[now]] ^= gauss_elimination[now]
            gate = build_gate(GateType.cx, [now, self.father[now]])
            gates.append(gate)


class TopologicalCnot(object):
    """ optimize the cnot circuit on topological device
    https://arxiv.org/pdf/1910.14478.pdf

    use steiner tree to optimize a cnot circuit on topological device
    """
    def execute(self, circuit: Circuit):
        """
        Args:
            circuit(Circuit): the circuit to be optimize
        """
        cnot_struct = self.read_circuit(circuit)
        gates = self.__execute_with_cnot_struct(cnot_struct)

        if circuit.topology is None or len(circuit.topology.edge_list) == 0:
            topology = [[True for _ in range(self.width)] for _ in range(self.width)]
        else:
            topology = [[False for _ in range(self.width)] for _ in range(self.width)]
            for topo in circuit.topology.edge_list:
                topology[topo.u][topo.v] = True

        output = Circuit(self.width)
        for gate in gates:
            c = self.topo_backward_map[gate.carg]
            t = self.topo_backward_map[gate.targ]
            if topology[c][t]:
                CX | output([c, t])
            else:
                H | output(c)
                H | output(t)
                CX | output([t, c])
                H | output(c)
                H | output(t)
        return output

    def delete_dfs(self, now):
        """ search for a initial mapping to get (maybe) better topology

        in this order, vertex i is not cut in [i, n)

        Args:
            now(int): the index of vertex now
        """
        self.delete_vis[now] = True
        for i in range(self.width - 1, -1, -1):
            if now != i and self.undirected_topology[now][i] and not self.delete_vis[i]:
                self.delete_dfs(i)
        self.topo_forward_map[now] = self.delete_total
        self.topo_backward_map[self.delete_total] = now
        self.delete_total += 1

    def read_circuit(self, circuit: Circuit):
        """
        Transform input circuit to CNOT struct, with the forward and backward topology map calculated

        Args:
            circuit(Circuit): input circuit

        Returns:
            list<int>: CNOT struct read from the circuit
        """
        self.width = circuit.width()
        if circuit.topology is None or len(circuit.topology.edge_list) == 0:
            self.undirected_topology = [[True for _ in range(self.width)] for _ in range(self.width)]
        else:
            self.undirected_topology = [[False for _ in range(self.width)] for _ in range(self.width)]
            for topo in circuit.topology.edge_list:
                self.undirected_topology[topo.u][topo.v] = True
                self.undirected_topology[topo.v][topo.u] = True

        self.topo_forward_map = [0 for _ in range(self.width)]
        self.topo_backward_map = [0 for _ in range(self.width)]
        self.delete_vis = [0 for _ in range(self.width)]
        self.delete_total = 0
        self.delete_dfs(self.width - 1)

        cnot_struct = []
        for i in range(self.width):
            cnot_struct.append(1 << i)

        for i in range(len(circuit.gates)):
            gate = circuit.gates[i]
            if gate.type == GateType.cx:
                cnot_struct[self.topo_forward_map[gate.targ]] ^= cnot_struct[self.topo_forward_map[gate.carg]]

        return cnot_struct

    def __execute_with_cnot_struct(self, cnot_struct, topology=None):
        """
        Compute the optimized CNOT gates with given CNOT struct
        Be aware that if this function is used alone, a topology will be necessary

        Args:
            cnot_struct(list<int>): the struct of cnot circuit
            topology(list<tuple<int, int>>, optional): topology of circuit
        """
        if topology is not None:
            self.width = len(cnot_struct)
            if len(topology) == 0:
                self.undirected_topology = [[True for _ in range(self.width)] for _ in range(self.width)]
            else:
                self.undirected_topology = [[False for _ in range(self.width)] for _ in range(self.width)]
                for topo in topology:
                    self.undirected_topology[topo[0]][topo[1]] = self.undirected_topology[topo[1]][topo[0]] = True

            self.topo_forward_map = [0 for _ in range(self.width)]
            self.topo_backward_map = [0 for _ in range(self.width)]
            self.delete_vis = [0 for _ in range(self.width)]
            self.delete_total = 0
            self.delete_dfs(self.width - 1)

        steiner_tree = SteinerTree(self.width, self.undirected_topology)

        # apply Gaussian Elimination on the matrix
        gates = []

        for i in range(self.width):
            j = self.width
            for t in range(i, self.width):
                if cnot_struct[t] & (1 << i):
                    j = t
                    break

            if j >= self.width:
                raise Exception("the matrix is not singular matrix")

            # find a line that the ith bit is 1, and find a path to make the ith bit of ith line 1
            pre = [-1 for _ in range(self.width)]
            if i != j:
                bfs = Queue()
                bfs.put(j)
                while not bfs.empty():
                    u = bfs.get()
                    for j in range(i, self.width):
                        if j != u and self.undirected_topology[u][j]:
                            if pre[j] == -1:
                                pre[j] = u
                                if j == i:
                                    break
                                bfs.put(j)
                    if pre[i] != -1:
                        break

            paths = [i]
            u = pre[i]
            while u != -1:
                paths.append(u)
                u = pre[u]

            for j in range(len(paths) - 2, -1, -1):
                cnot_struct[paths[j]] ^= cnot_struct[paths[j + 1]]
                gate = build_gate(GateType.cx, [paths[j + 1], paths[j]])
                gates.append(gate)

            # elimination below rows
            needCover = []
            for j in range(i + 1, self.width):
                if cnot_struct[j] & (1 << i):
                    needCover.append(j)
            if len(needCover) > 0:
                needCover.append(i)
                steiner_tree.build_ST(needCover, i)
                steiner_tree.elimination_below(cnot_struct, gates)

            # elimination this row

            # find a set S whose summation in equal to row 1 except column i
            back_gauss_elimination = [0 for _ in range(i + 1)]
            xor_result = [0 for _ in range(i + 1)]
            for j in range(i + 1, self.width):
                back_gauss_elimination.append(cnot_struct[j])
                xor_result.append(1 << j)

            for j in range(i + 1, self.width):
                k = self.width
                for t in range(j, self.width):
                    if back_gauss_elimination[t] & (1 << j):
                        k = t
                        break
                if k == self.width:
                    raise Exception("the matrix is not singular matrix")
                back_gauss_elimination[k], back_gauss_elimination[j] = \
                    back_gauss_elimination[j], back_gauss_elimination[k]
                xor_result[k], xor_result[j] = xor_result[j], xor_result[k]
                for k in range(j + 1, self.width):
                    if back_gauss_elimination[k] & (1 << j):
                        back_gauss_elimination[k] ^= back_gauss_elimination[j]
                        xor_result[k] ^= xor_result[j]

            val = cnot_struct[i]
            S_element = 0
            for j in range(i + 1, self.width):
                if val & (1 << j):
                    val ^= back_gauss_elimination[j]
                    S_element ^= xor_result[j]

            needCover = []
            for j in range(i + 1, self.width):
                if S_element & (1 << j):
                    needCover.append(j)

            if len(needCover) > 0:
                needCover.append(i)
                steiner_tree.build_ST(needCover, i)
                steiner_tree.elimination_above(cnot_struct, gates)

        gates.reverse()
        return gates
