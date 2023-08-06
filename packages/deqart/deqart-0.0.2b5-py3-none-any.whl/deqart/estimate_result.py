class EstimateResult:
    """This class contains information about the estimated runtime/cost that
    will be incurred from running the given circuit on the given quantum
    machine/simulator. WARNING: this is just an estimate, the actual runtime
    may be less or more."""

    def __init__(self, data):
        self.device = data.get("device")
        self.estimate_ms = data.get("estimate_ms")
        self.num_qubits = data.get("num_qubits")
        self.circuit = data.get("qc")
        self.warning_message = data.get("warning_message")
