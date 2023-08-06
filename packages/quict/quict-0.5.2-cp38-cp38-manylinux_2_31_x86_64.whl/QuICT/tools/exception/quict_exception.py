ERROR_CODE = {
    # Error code table for the QuICT system.
    1000: "QuICT Exception",
    # 1001-1999: QuICT Core Module Exception
    # 1001-1100: QuICT Circuit Module Exception
    1001: "QuICT Circuit's Type Exception",
    1002: "QuICT Circuit's Qubits Exception",
    1003: "QuICT Circuit's Fidelity Exception",
    1004: "QuICT Circuit Append Operator Exception",
    1005: "QuICT Circuit Replace Operator Exception",
    1006: "QuICT Circuit Random or Supremacy Append Exception",
    1007: "QuICT DAG Circuit Exception",
    1008: "QuICT Circuit Draw Exception",
    # 2000-2999: QuICT Simulation Module Exception

    # 3000-3999: QuICT Algorithm Module Exception

    # 4000-4999: QuICT QCDA Module Exception

    # 9000-9999: QuICT Utility Module Exception

}


class QuICTException(Exception):
    """The base exception class for QuICT.

    Args:
        error_code (int): the predefined QuICT error code.
        msg (str): the description of the error. If is None, which will
        show the base error information.
    """

    def __init__(self, error_code: int = 1000, msg: str = None):
        self.ecode = error_code
        self.strerror = msg if msg else ERROR_CODE[self.ecode]
        if not isinstance(self.strerror, str):
            self.strerror = str(msg)

    def __str__(self):
        return self.strerror

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"
