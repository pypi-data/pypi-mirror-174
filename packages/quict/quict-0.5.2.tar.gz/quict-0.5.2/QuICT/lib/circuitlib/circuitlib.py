from QuICT.tools.interface import OPENQASMInterface
from QuICT.lib.qasm.exceptions import QasmError
import os


class CircuitLib:

    """ Circuitlib

    A circuit library function. Get circuits with .qasm type

    """

    def load_qasm(self, filename):

        # load a qasm file

        qasm = OPENQASMInterface.load_file(filename)
        if not qasm.valid_circuit:
            raise QasmError("Missing input file")
        return qasm.circuit

    def load_all(self, filename):

        # load all qasm files under the same address

        circuit_all = []
        for root, dirs, files in os.walk(filename):
            for file in files:
                circuit_all.append(self.load_qasm(filename + '/' + file))
        return circuit_all

    def get_circuit(self, name="template", *args):

        '''

        name: "template", "random", "algorithm", "experiment"

        *args:

                template:   args[0]: qubit_num, upper bound of qubit number
                                     of templates
                            args[1]: size, upper bound of size of templates
                            args[2]: depth, upper bound of depth of templates

                random:     args[0]: circuit_type ("ctrl_diag"/"ctrl_unitary"
                                                    /"diag"/"qft"/"single_bit"
                                                    /"unitary"),
                                     type of random circuits
                            args[1]: qubit number (list/int), get a list of
                                     circuits (a single circuit) with given
                                     qubit numbers

                algorithm:  args[0]: circuit_type ("QFT"/"Grover"/"Supermacy"),
                                     type of algorithm circuits
                            args[1]: qubit number (list/int), get a list of
                                     circuits (a single circuit) with given
                                     qubit numbers

                experiment: args[0]: circuit_type("Mapping"/"Adder"), type of
                                     experiment circuits
                            args[1]: (for Adder)   qubit number (list/int), get
                                                   a list of circuits (a single
                                                   circuit) with given qubit
                                                   numbers
                                     (for Mapping) mapping_name, get all
                                                   mapping circuits under the
                                                   same qubit mapping type

        '''

        para = args
        circuit_list = []
        filename = os.path.dirname(__file__) + '/circuit_qasm/' + name

        if name == "template":

            # get all templates satisfying <=bit_num & <=size & <=depth

            for bit_num in range(para[0] + 1):
                for size in range(para[1] + 1):
                    for depth in range(para[2] + 1):
                        part_name = str(bit_num) + '_' + str(size)
                        part_name += '_' + str(depth)
                        for root, dirs, files in os.walk(filename):
                            for file in files:
                                if file.find(part_name) != -1:
                                    qaf = self.load_qasm(filename + '/' + file)
                                    circuit_list.append(qaf)

        elif name == "random":

            # get all random circuits

            filename += '/' + para[0]
            if isinstance(para[1], int):
                random_list = [para[1]]
            else:
                random_list = para[1]
            for list_name in random_list:
                filesname = filename + '/' + str(list_name) + ".qasm"
                circuit = self.load_qasm(filesname)
                if circuit is not None:
                    circuit_list.append(circuit)

        elif name == "algorithm":

            # get all algorithm circuits

            filename += '/' + para[0]
            al_dic = {"QFT": "/qft_", "Grover": "/grover_", "Supremacy": "/"}
            if para[0] in al_dic:
                if isinstance(para[1], int):
                    algorithm_list = [para[1]]
                else:
                    algorithm_list = para[1]
                for list_name in algorithm_list:
                    filesname = filename + al_dic[para[0]]
                    filesname += str(list_name) + ".qasm"
                    circuit = self.load_qasm(filesname)
                    if circuit is not None:
                        circuit_list.append(circuit)
            else:
                filename = ""

        elif name == "experiment":

            # get all experiment circuits

            filename += '/' + para[0]
            if para[0] == "Mapping":
                filename += '/' + para[1]
                circuit = self.load_all(filename)
                if circuit is not None:
                    circuit_list.append(circuit)
            elif para[0] == "Adder":
                filename += '/adder_n'
                if isinstance(para[1], int):
                    adder_list = [para[1]]
                else:
                    adder_list = para[1]
                for list_name in adder_list:
                    filesname = filename + str(list_name) + ".qasm"
                    circuit = self.load_qasm(filesname)
                    if circuit is not None:
                        circuit_list.append(circuit)
            else:
                filename = ""
        else:
            filename = ""
        return circuit_list
