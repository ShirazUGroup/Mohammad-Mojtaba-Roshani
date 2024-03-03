from time import time


class Stopwatch:
    _time: float

    def __init__(self) -> None:
        self._time = time()

    def delta(self, time: float = time()) -> float:
        return self._time - time

    def reset(self) -> None:
        self._time = time()
