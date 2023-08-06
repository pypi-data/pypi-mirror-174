import collections
import datetime
from io import BytesIO

import numpy as np
import requests
from dateutil.parser import parse


class JobResult:
    def __init__(self, data):
        #  "PENDING" | "QUEUED" |"RUNNING" | "COMPLETED"
        self.run_status = data.get("run_status")
        self.job_id = data.get("job_id")
        self.sv_link = data.get("sv_link")
        self.top_100_results = data.get("top_100_results")
        self.num_qubits = data.get("num_qubits")
        self.circuit = data.get("qc")
        self.tags = data.get("tags")

        self.created_on = data.get("created_on")

        self.queue_start = data.get("queue_start")
        if self.queue_start is not None:
            self.queue_start = parse(self.queue_start)

        self.run_start = data.get("run_start")
        if self.run_start is not None:
            self.run_start = parse(self.run_start)

        self.run_end = data.get("run_end")
        if self.run_end is not None:
            self.run_end = parse(self.run_end)

        if self.queue_start is not None and self.run_start is not None:
            self.queue_time_ms = int(
                (self.run_start - self.queue_start) / datetime.timedelta(milliseconds=1)
            )
        else:
            self.queue_time_ms = None

        if self.run_start is not None and self.run_end is not None:
            self.run_time_ms = round(
                (self.run_end - self.run_start) / datetime.timedelta(milliseconds=1)
            )
        else:
            self.run_time_ms = None

        Status = collections.namedtuple("Status", ["success", "error_message"])
        self.status = Status(data.get("success"), data.get("error_message"))

        self.cost = data.get("cost")
        if self.cost is not None:
            self.cost /= 100.0

    def get_statevector(self):
        if self.sv_link is not None:
            data = requests.get(self.sv_link, timeout=100).content
            return np.load(BytesIO(data))
        return None

    def __str__(self):
        return f"Job ID: {self.job_id}, run status: {self.run_status}, queue time (ms): {self.queue_time_ms}, run time (ms): {self.run_time_ms}, cost ($): {self.cost}, num qubits: {self.num_qubits}, status: {self.status}"
