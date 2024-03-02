from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from helpers.console import Console
from typing import Type, Any


class RSA:
    _clg: Console
    _debug: bool
    _password: bytes
    _name: str
    private_key = None
    private_key_bytes: bytes
    public_key = None
    public_key_byte: bytes

    def __init__(self, debug: bool, name: str, password: str):
        self._clg = Console()
        self._password = str.encode(password)
        self._debug = debug
        self._name = name

    def gen_pme_keys(self) -> Type['RSA']:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.private_key = private_key

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                self._password)
        )
        self.private_key_bytes = encrypted_pem_private_key.splitlines()[0]

        self._clg.debug(self._debug, f"private key (byte) is: {
                        self.private_key_bytes}")

        self.public_key = private_key.public_key()
        pem_public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.public_key_byte = pem_public_key.splitlines()[0]

        self._clg.debug(self._debug, f"public key (byte) is: {
                        self.public_key_byte}")

        return self

    def write_private_key(self) -> Type['RSA']:
        private_key_file = open(f"keys/{self._name}-rsa.pem", "w")
        private_key_file.write(self.private_key.decode())
        private_key_file.close()

        return self

    def write_public_key(self) -> Type['RSA']:
        public_key_file = open(f"keys/{self._name}-rsa.pub", "w")
        public_key_file.write(self.public_key.decode())
        public_key_file.close()

        return self

    def encryption(self, message: str) -> Any:  # TODO: make typing exact
        ciphertext = self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        self._clg.debug(self._debug, f"ciphertext for message: {
                        message} is {ciphertext}")

        return ciphertext

    def decryption(self, ciphertext):
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        self._clg.debug(self._debug, f"plaintext for ciphertext: {
                        ciphertext} is {plaintext}")

        return plaintext
