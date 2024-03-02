#############
#   MODULES #
#############
import pandas as pd
from cryptography.fernet import Fernet
from helpers.console import Console
from helpers.random import Random
from helpers.aes import AES


class Peer:
    _clg = None
    _df: pd.DataFrame
    _key: bytes
    _cipher: Fernet
    _debug: bool

    def __init__(self, debug_mode: bool, stopwatch: float, dataframe: pd.DataFrame, name: str) -> None:
        self._clg = Console()
        self._clg.debug(debug_mode, f"peer {name} is initializing...")

        if not isinstance(dataframe, pd.DataFrame):
            self._clg.error("input (dataframe) must be a pandas DataFrame")
            raise TypeError("input (dataframe) must be a pandas DataFrame")

        # Assignment
        self._df = dataframe
        self._debug = debug_mode
        # Generating
        self._key = AES().gen_key()
        self._cipher = AES().gen_cipher(self._key)

    def encrypt_local(self) -> None:
        df_str = self._df.to_csv(index=False).encode()
        encrypted_data = self._cipher.encrypt(df_str).decode()
        self._clg.debug(self._debug, f"the encrypted data is: \n{
                        encrypted_data} \nand the data length is: {len(encrypted_data)}")
