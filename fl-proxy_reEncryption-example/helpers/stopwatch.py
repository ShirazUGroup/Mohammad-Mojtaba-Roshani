from time import time


class Stopwatch:
    _time: float
    _total: float

    def __init__(self) -> None:
        self._time = time()
        self._total = time()

    def delta(self) -> float:
        return time() - self._time

    def reset(self) -> None:
        self._time = time()

    def get_total(self) -> float:
        return time() - self._total
