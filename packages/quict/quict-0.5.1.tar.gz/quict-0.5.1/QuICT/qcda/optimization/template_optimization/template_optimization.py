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
Given a template and a circuit: it applies template matching and substitutes
all compatible maximal matches that reduces the size of the circuit.

**Reference:**

[1] Iten, R., Moyard, R., Metger, T., Sutter, D. and Woerner, S., 2020.
Exact and practical pattern matching for quantum circuit optimization.
`arXiv:1909.05270 <https://arxiv.org/abs/1909.05270>`_
"""

from QuICT.core import *
from QuICT.qcda.utility import OutputAligner
from .template_matching.dagdependency.circuit_to_dagdependency import circuit_to_dagdependency
from .template_matching.dagdependency.dagdependency_to_circuit import dagdependency_to_circuit
from .templates import template_nct_2a_1, template_nct_2a_2, template_nct_2a_3
from .template_matching import TemplateMatching, TemplateSubstitution, MaximalMatches


class TemplateOptimization(object):
    """
    Class for the template optimization pass.
    """
    def __init__(self, template_list=None, heuristics_qubits_param=None, heuristics_backward_param=None):
        """
        Args:
            template_list (list[QuantumCircuit()]): list of the different template circuit to apply.
            heuristics_backward_param (list[int]): [length, survivor] Those are the parameters for
                applying heuristics on the backward part of the algorithm. This part of the
                algorithm creates a tree of matching scenario. This tree grows exponentially. The
                heuristics evaluates which scenarios have the longest match and keep only those.
                The length is the interval in the tree for cutting it and surviror is the number
                of scenarios that are kept. We advice to use l=3 and s=1 to have serious time
                advantage. We remind that the heuristics implies losing a part of the maximal
                matches. Check reference for more details.
            heuristics_qubits_param (list[int]): [length] The heuristics for the qubit choice make
                guesses from the dag dependency of the circuit in order to limit the number of
                qubit configurations to explore. The length is the number of successors or not
                predecessors that will be explored in the dag dependency of the circuit, each
                qubits of the nodes are added to the set of authorized qubits. We advice to use
                length=1. Check reference for more details.
        """
        # If no template is given; the template are set as x-x, cx-cx, ccx-ccx.
        if template_list is None:
            template_list = [template_nct_2a_1(), template_nct_2a_2(), template_nct_2a_3()]
        if heuristics_qubits_param is None:
            heuristics_qubits_param = []
        if heuristics_backward_param is None:
            heuristics_backward_param = []
        self.template_list = template_list
        self.heuristics_qubits_param = heuristics_qubits_param
        self.heuristics_backward_param = heuristics_backward_param

    @OutputAligner()
    def execute(self, circuit):
        """
        Args:
            circuit(Circuit): circuit.

        Returns:
            Circuit: optimized circuit.

        Raises:
            TypeError: If the template has not the right form or
             if the output circuit acts differently as the input circuit.
        """
        circuit_dag_dep = circuit_to_dagdependency(circuit)

        for template in self.template_list:
            if not isinstance(template, Circuit):
                raise TypeError('A template is a Circuit().')

            template_dag_dep = circuit_to_dagdependency(template)

            if template_dag_dep.num_qubits > circuit_dag_dep.num_qubits:
                continue

            template_m = TemplateMatching(circuit_dag_dep,
                                          template_dag_dep,
                                          self.heuristics_qubits_param,
                                          self.heuristics_backward_param)

            template_m.run_template_matching()

            matches = template_m.match_list

            if matches:
                maximal = MaximalMatches(matches)
                maximal.run_maximal_matches()
                max_matches = maximal.max_match_list

                substitution = TemplateSubstitution(max_matches,
                                                    template_m.circuit_dag_dep,
                                                    template_m.template_dag_dep)
                substitution.run_dag_opt()

                circuit_dag_dep = substitution.dag_dep_optimized
            else:
                continue

        circuit = dagdependency_to_circuit(circuit_dag_dep)
        return circuit
