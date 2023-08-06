#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2020/11/5 8:59
# @Author  : Han Yu
# @File    : topological_cnot_rz.py

from QuICT.qcda.optimization import TopologicalCnot
from QuICT.core import Circuit
from QuICT.core.gate import build_gate, CX, H, Rz, GateType


class TopologicalCnotRz(object):
    """ optimize the cnot_Rz circuit on topological device

    use topological_cnot to optimize a cnot circuit on topological device
    """
    def execute(self, circuit: Circuit):
        """
        Args:
            circuit(Circuit): the circuit to be optimize
        """
        cnot_struct, input, th, waitDeal = self.read_circuit(circuit)

        undirected_topology = []
        if circuit.topology is not None:
            for topology in circuit.topology.edge_list:
                undirected_topology.append((topology.u, topology.v))
                undirected_topology.append((topology.v, topology.u))

        result = self.solve(cnot_struct, input, th, waitDeal, undirected_topology)

        if circuit.topology is None or len(circuit.topology.edge_list) == 0:
            topology = [[True for _ in range(self.width)] for _ in range(self.width)]
        else:
            topology = [[False for _ in range(self.width)] for _ in range(self.width)]
            for topo in circuit.topology.edge_list:
                topology[topo.u][topo.v] = True

        output = Circuit(self.width)
        for gate in result:
            if gate.type == GateType.cx:
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
            else:
                Rz(gate.parg) | output(self.topo_backward_map[gate.targ])
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
        """ get description from the circuit

        Args:
            circuit(Circuit): the input circuit, contained the information of topology and (maybe) cnot
        Returns:
            list<int>: the struct of cnot circuit
            list<int>: the Rz_state wait to be deal
            list<float>: the Rz_angle wait to be deal
            set<int>: the index of Rz_state wait to be deal
        """
        waitDeal = set()
        self.width = circuit.width()
        if circuit.topology is None or len(circuit.topology.edge_list) == 0:
            self.undirected_topology = [[True for _ in range(self.width)] for _ in range(self.width)]
        else:
            self.undirected_topology = [[False for _ in range(self.width)] for _ in range(self.width)]
            for topology in circuit.topology.edge_list:
                self.undirected_topology[topology.u][topology.v] = True
                self.undirected_topology[topology.v][topology.u] = True
        self.topo_forward_map = [0 for _ in range(self.width)]
        self.topo_backward_map = [0 for _ in range(self.width)]
        self.delete_vis = [0 for _ in range(self.width)]
        self.delete_total = 0
        self.delete_dfs(self.width - 1)

        cnot_struct = []
        for i in range(self.width):
            cnot_struct.append(1 << i)

        termNumber = 0

        cnot_index = dict()
        input = []
        th = []

        for i in range(len(circuit.gates)):
            gate = circuit.gates[i]
            if gate.type == GateType.cx:
                cnot_struct[self.topo_forward_map[gate.targ]] ^= cnot_struct[self.topo_forward_map[gate.carg]]
            elif gate.type == GateType.rz:
                index = cnot_index.setdefault(cnot_struct[self.topo_forward_map[gate.targ]], 0)
                if index != 0:
                    th[index - 1] += gate.parg
                else:
                    termNumber += 1
                    cnot_index[cnot_struct[self.topo_forward_map[gate.targ]]] = termNumber
                    th.append(gate.parg)
                    input.append(cnot_struct[self.topo_forward_map[gate.targ]])
                    waitDeal.add(termNumber - 1)

        return cnot_struct, input, th, waitDeal

    def solve(self, cnot_struct, input, th, waitDeal, undirected_topology):
        """ main part of the algorithm

        Args:
            input(list<int>): the Rz_state wait to be deal
            th(list<float>): the Rz_angle wait to be deal
            waitDeal(set<int>): the index of Rz_state wait to be deal)
            undirected_topology(list<tuple<int, int>>): make topology undirected

        Returns:
            list<CXGates>: the result of the algorithm
        """
        result = []
        flag = False
        firstIn = True
        stateChange = []
        for i in range(self.width):
            stateChange.append(1 << i)

        while len(waitDeal) > 0 or not flag:
            gates = []
            a = [0 for _ in range(self.width)]
            total = 0
            gsxy = []
            needDeal = []
            if len(waitDeal) > 0:
                for it in waitDeal:
                    val = input[it]
                    for i in range(self.width - 1, -1, -1):
                        if (val & (1 << i)) != 0:
                            if a[i] == 0:
                                a[i] = val
                                break
                            val ^= a[i]

                    if val > 0:
                        gsxy.append(input[it])
                        gate = build_gate(GateType.rz, total, th[it])
                        gates.append(gate)
                        needDeal.append(it)
                        total += 1
                        if total >= self.width:
                            break

                for i in range(total):
                    waitDeal.remove(needDeal[i])

                for j in range(self.width):
                    val = 1 << j
                    for i in range(self.width - 1, -1, -1):
                        if val & (1 << i) != 0:
                            if a[i] == 0:
                                a[i] = val
                                break
                            val ^= a[i]

                    if val > 0:
                        gsxy.append(1 << j)
                        total += 1
                        if total >= self.width:
                            break
            else:
                for i in range(self.width):
                    gsxy.append(cnot_struct[i])
                    total += 1
                flag = True
            if not firstIn:
                u = []
                v = []
                tempChange = []
                for i in range(self.width):
                    tempChange.append(stateChange[i])
                for i in range(self.width):
                    j = self.width
                    for t in range(i, self.width):
                        if (1 << i) & tempChange[t]:
                            j = t
                            break
                    if j == self.width:
                        raise Exception("algorithm error")
                    if j != i:
                        u.append(j)
                        v.append(i)
                        tempChange[i] ^= tempChange[j]
                    for j in range(self.width):
                        if j != i:
                            if (1 << i) & tempChange[j]:
                                u.append(i)
                                v.append(j)
                                tempChange[j] ^= tempChange[i]
                length = len(u)
                for i in range(length - 1, -1, -1):
                    for j in range(self.width):
                        if gsxy[j] & (1 << v[i]):
                            gsxy[j] ^= 1 << u[i]
            else:
                firstIn = False

            if total == 0:
                break

            if total != self.width:
                raise Exception("algorithm error")

            TC = TopologicalCnot()
            gsxy_gate = TC._TopologicalCnot__execute_with_cnot_struct(cnot_struct=gsxy, topology=undirected_topology)
            gsxy_gate.reverse()

            gates.extend(gsxy_gate)

            length = len(gates)
            for j in range(length - 1, -1, -1):
                result.append(gates[j])
                if gates[j].type == GateType.cx:
                    stateChange[gates[j].targ] ^= stateChange[gates[j].carg]

        return result
