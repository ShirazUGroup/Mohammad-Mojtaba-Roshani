#############
#   MODULES #
#############
import pandas as pd
# from cryptography.fernet import Fernet
from helpers.console import Console
from helpers.random import Random


class Peer:
    _clg = None

    def __init__(self, debug_mode: bool, stopwatch: float, dataframe: pd.DataFrame, name: str) -> None:
        self._clg = Console()
        self._clg.debug(debug_mode, f"peer {name} is initializing...")

        if not isinstance(dataframe, pd.DataFrame):
            self._clg.error("input (dataframe) must be a pandas DataFrame")
            raise TypeError("input (dataframe) must be a pandas DataFrame")
