from QuICT.tools.exception import QuICTException


class CircuitTypeError(QuICTException):
    """ Circuit Type Error, including Layout, Fidelity, Qureg, ... """
    def __init__(self, msg: str = None):
        super().__init__(1001, msg)


class CircuitQubitsError(QuICTException):
    """ Circuit's Qubits Error, including qubit index exceed or unmatched qureg. """
    def __init__(self, msg: str = None):
        super().__init__(1002, msg)


class CircuitFidelityError(QuICTException):
    """ Circuit Fidelity Error. """
    def __init__(self, msg: str = None):
        super().__init__(1003, msg)


class CircuitAppendError(QuICTException):
    """ Circuit Append Operator Error. """
    def __init__(self, msg: str = None):
        super().__init__(1004, msg)


class CircuitReplaceError(QuICTException):
    """ Circuit Replace Gate Error. """
    def __init__(self, msg: str = None):
        super().__init__(1005, msg)


class CircuitSpecialAppendError(QuICTException):
    """ Circuit special append including Random Append and Supremacy Append. """
    def __init__(self, msg: str = None):
        super().__init__(1006, msg)


class CircuitDAGError(QuICTException):
    """ DAG Circuit Error. """
    def __init__(self, msg: str = None):
        super().__init__(1007, msg)


class CircuitDrawError(QuICTException):
    """ Circuit Draw Error. """
    def __init__(self, msg: str = None):
        super().__init__(1008, msg)
