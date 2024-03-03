#############
#   MODULES #
#############
import io
from typing import List, Tuple
import pandas as pd
from cryptography.fernet import Fernet
from umbral import Capsule, PublicKey, VerifiedKeyFrag
from helpers.console import Console
from helpers.security.aes import AES
from helpers.security.pre import ProxyReEncryption
from helpers.stopwatch import Stopwatch


class Peer:
    _clg = None
    _df: pd.DataFrame
    _key: bytes
    _cipher: Fernet
    _debug: bool
    _name: str
    pre: ProxyReEncryption

    def __init__(self, debug_mode: bool, stopwatch: Stopwatch, dataframe: pd.DataFrame, name: str) -> None:
        self._clg = Console()
        self._clg.bg_blue(f"peer {name} is initializing...")

        if not isinstance(dataframe, pd.DataFrame):
            self._clg.error("input (dataframe) must be a pandas DataFrame")
            raise TypeError("input (dataframe) must be a pandas DataFrame")

        # Assignment
        self._df = dataframe
        self._debug = debug_mode
        self._name = name
        # Generating
        self._key = AES.gen_key()
        self._cipher = AES.gen_cipher(self._key)
        self.pre = ProxyReEncryption(self._debug)

    def assimetric_key_encryption(self) -> Tuple[Capsule, bytes]:
        capsule, ciphertext = self.pre.encryption(
            self._key)

        return capsule, ciphertext

    def encrypt_local(self) -> bytes:
        df_str = self._df.to_csv(index=False).encode()
        encrypted_data = self._cipher.encrypt(df_str)
        self._clg.debug(self._debug, f"""the encrypted data for: {
                        self._name} have done and the data length is: {len(encrypted_data)}""")

        return encrypted_data

    def decrypt_dataframe(self, key: bytes, encrypted_data_bytes: bytes, node_name: str | None = None) -> pd.DataFrame:
        new_cipher: Fernet = AES.gen_cipher(key)
        decrypted_data = new_cipher.decrypt(
            encrypted_data_bytes).decode('utf-8')

        generated_df: pd.DataFrame = pd.read_csv(io.StringIO(decrypted_data))

        if node_name == None:
            node_name = self._name

        self._clg.debug(self._debug, f"""the decrypted data for: {
                        node_name} have done""")

        return generated_df
