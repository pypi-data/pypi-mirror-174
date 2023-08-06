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

"""
Template matching for all possible qubit configurations and initial matches. It
returns the list of all matches obtained from this algorithm.


**Reference:**

[1] Iten, R., Moyard, R., Metger, T., Sutter, D. and Woerner, S., 2020.
Exact and practical pattern matching for quantum circuit optimization.
`arXiv:1909.05270 <https://arxiv.org/abs/1909.05270>`_

"""

import itertools

from .forward_match import ForwardMatch
from .backward_match import BackwardMatch


class TemplateMatching:
    """
    Class TemplatingMatching allows to apply the full template matching algorithm.
    """

    def __init__(self, circuit_dag_dep, template_dag_dep,
                 heuristics_qubits_param=None, heuristics_backward_param=None):
        """
        Create a TemplateMatching object with necessary arguments.
        Args:
            circuit_dag_dep (QuantumCircuit): circuit.
            template_dag_dep (QuantumCircuit): template.
            heuristics_backward_param (list[int]): [length, survivor]
            heuristics_qubits_param (list[int]): [length]
        """
        self.circuit_dag_dep = circuit_dag_dep
        self.template_dag_dep = template_dag_dep
        self.match_list = []
        self.heuristics_qubits_param = heuristics_qubits_param\
            if heuristics_qubits_param is not None else []
        self.heuristics_backward_param = heuristics_backward_param\
            if heuristics_backward_param is not None else []

    def _list_first_match_new(self, node_circuit, node_template, n_qubits_t):
        """
        Returns the list of qubit for circuit given the first match, the unknown qubit are
        replaced by -1.
        Args:
            node_circuit (DAGDepNode): First match node in the circuit.
            node_template (DAGDepNode): First match node in the template.
            n_qubits_t (int): number of qubit in the template.
        Returns:
            list: list of qubits to consider in circuit (with specific order).
        """
        l_q = []

        # 1-qubit gate
        if node_circuit.gate.is_single():
            l_q_sub = [-1] * n_qubits_t
            for q in node_template.qargs:
                l_q_sub[q] = node_circuit.qargs[node_template.qargs.index(q)]
            l_q.append(l_q_sub)
        # Controlled gate
        else:
            control = node_template.gate.controls
            control_qubits_circuit = node_circuit.qargs[:control]
            target_qubits_circuit = node_circuit.qargs[control::]

            for control_perm_q in itertools.permutations(control_qubits_circuit):
                control_perm_q = list(control_perm_q)
                l_q_sub = [-1] * n_qubits_t
                for q in node_template.qargs:
                    node_circuit_perm = control_perm_q + target_qubits_circuit
                    l_q_sub[q] = node_circuit_perm[node_template.qargs.index(q)]
                l_q.append(l_q_sub)

        return l_q

    def _sublist(self, lst, exclude, length):
        """
        Function that returns all possible combinations of a given length, considering an
        excluded list of elements.
        Args:
            lst (list): list of qubits indices from the circuit.
            exclude (list): list of qubits from the first matched circuit gate.
            length (int): length of the list to be returned (number of template qubit -
            number of qubit from the first matched template gate).
        Yield:
            iterator: Iterator of the possible lists.
        """
        for sublist in itertools.combinations([e for e in lst if e not in exclude], length):
            yield list(sublist)

    def _list_qubit_circuit(self, list_first_match, permutation):
        """
        Function that returns the list of the circuit qubits and clbits give a permutation
        and an initial match.
        Args:
            list_first_match (list): list of qubits indices for the initial match.
            permutation (list): possible permutation for the circuit qubit.
        Returns:
            list: list of circuit qubit for the given permutation and initial match.
        """
        list_circuit = []

        counter = 0

        for elem in list_first_match:
            if elem == -1:
                list_circuit.append(permutation[counter])
                counter = counter + 1
            else:
                list_circuit.append(elem)

        return list_circuit

    def _add_match(self, backward_match_list):
        """
        Method to add a match in list only if it is not already in it.
        If the match is already in the list, the qubit configuration
        is append to the existing match.
        Args:
            backward_match_list (list): match from the backward part of the
            algorithm.
        """

        already_in = False

        for b_match in backward_match_list:
            for l_match in self.match_list:
                if b_match.match == l_match.match:
                    index = self.match_list.index(l_match)
                    self.match_list[index].qubit.append(b_match.qubit[0])
                    already_in = True

            if not already_in:
                self.match_list.append(b_match)

    def _explore_circuit(self, node_id_c, node_id_t, n_qubits_t, length):
        """
        Explore the successors of the node_id_c (up to the given length).
        Args:
            node_id_c (int): first match id in the circuit.
            node_id_t (int): first match id in the template.
            n_qubits_t (int): number of qubits in the template.
            length (int): length for exploration of the successors.
        Returns:
            list: qubits configuration for the 'length' successors of node_id_c.
        """
        template_nodes = range(node_id_t + 1, self.template_dag_dep.size())
        circuit_nodes = range(0, self.circuit_dag_dep.size())
        successors_template = self.template_dag_dep.get_node(node_id_t).successors

        counter = 1
        qubit_set = set(self.circuit_dag_dep.get_node(node_id_c).qargs)
        if 2 * len(successors_template) > len(template_nodes):
            successors = self.circuit_dag_dep.get_node(node_id_c).successors
            for succ in successors:
                qarg = self.circuit_dag_dep.get_node(succ).qargs
                if (len(qubit_set | set(qarg))) <= n_qubits_t and counter <= length:
                    qubit_set = qubit_set | set(qarg)
                    counter += 1
                elif (len(qubit_set | set(qarg))) > n_qubits_t:
                    return list(qubit_set)
            return list(qubit_set)

        else:
            not_successors = list(set(circuit_nodes) - set(
                self.circuit_dag_dep.get_node(node_id_c).successors))
            candidate = [not_successors[j] for j in
                         range(len(not_successors) - 1, len(not_successors) - 1 - length, -1)]

            for not_succ in candidate:
                qarg = self.circuit_dag_dep.get_node(not_succ).qargs
                if counter <= length and (len(qubit_set | set(qarg))) <= n_qubits_t:
                    qubit_set = qubit_set | set(qarg)
                    counter += 1
                elif (len(qubit_set | set(qarg))) > n_qubits_t:
                    return list(qubit_set)
            return list(qubit_set)

    def run_template_matching(self):
        """
        Run the complete algorithm for finding all maximal matches for the given template and
        circuit. First it fixes the configuration of the the circuit due to the first match.
        Then it explores all compatible qubit configurations of the circuit. For each
        qubit configurations, we apply first the Forward part of the algorithm  and then
        the Backward part of the algorithm. The longest matches for the given configuration
        are stored. Finally the list of stored matches is sorted.
        """

        # Get the number of qubits for both circuit and template.
        n_qubits_c = self.circuit_dag_dep.num_qubits

        n_qubits_t = self.template_dag_dep.num_qubits

        # Loop over the indices of both template and circuit.
        for template_index in range(0, self.template_dag_dep.size()):
            for circuit_index in range(0, self.circuit_dag_dep.size()):
                # Operations match up to ParameterExpressions.
                # TODO: Implement more precise comparation(i.e. about parameters)
                if self.circuit_dag_dep.get_node(circuit_index).name ==\
                        self.template_dag_dep.get_node(template_index).name:

                    qarg_c = self.circuit_dag_dep.get_node(circuit_index).qargs

                    qarg_t = self.template_dag_dep.get_node(template_index).qargs

                    node_id_c = circuit_index
                    node_id_t = template_index

                    # Fix the qubits and clbits configuration given the first match.

                    all_list_first_match_q = \
                        self._list_first_match_new(self.circuit_dag_dep.get_node(circuit_index),
                                                   self.template_dag_dep.get_node(template_index),
                                                   n_qubits_t)

                    list_circuit_q = list(range(0, n_qubits_c))

                    # If the parameter for qubits heuristics is given then extracts
                    # the list of qubits for the successors (length(int)) in the circuit.

                    if self.heuristics_qubits_param:
                        heuristics_qubits = self._explore_circuit(node_id_c,
                                                                  node_id_t,
                                                                  n_qubits_t,
                                                                  self.heuristics_qubits_param[0])
                    else:
                        heuristics_qubits = []

                    for sub_q in self._sublist(list_circuit_q, qarg_c, n_qubits_t - len(qarg_t)):
                        # If the heuristics qubits are a subset of the given qubits configuration,
                        # then this configuration is accepted.
                        if set(heuristics_qubits).issubset(set(sub_q) | set(qarg_c)):
                            # Permute the qubit configuration.
                            for perm_q in itertools.permutations(sub_q):
                                perm_q = list(perm_q)
                                for list_first_match_q in all_list_first_match_q:
                                    list_qubit_circuit =\
                                        self._list_qubit_circuit(list_first_match_q, perm_q)

                                    # Apply the forward match part of the algorithm.
                                    forward = ForwardMatch(
                                        self.circuit_dag_dep,
                                        self.template_dag_dep,
                                        node_id_c, node_id_t,
                                        list_qubit_circuit
                                    )
                                    forward.run_forward_match()

                                    # Apply the backward match part of the algorithm.
                                    backward = BackwardMatch(
                                        forward.circuit_dag_dep,
                                        forward.template_dag_dep,
                                        forward.match,
                                        node_id_c,
                                        node_id_t,
                                        list_qubit_circuit,
                                        self.heuristics_backward_param
                                    )
                                    backward.run_backward_match()

                                    # Add the matches to the list.
                                    self._add_match(backward.match_final)

        # Sort the list of matches according to the length of the matches (decreasing order).
        self.match_list.sort(key=lambda x: len(x.match), reverse=True)
