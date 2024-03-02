import multiprocessing


class System:
    def __init__(self) -> None:
        pass

    def get_cpu_core_count(self) -> int:
        return multiprocessing.cpu_count()
