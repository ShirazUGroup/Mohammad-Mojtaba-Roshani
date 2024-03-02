from cryptography.fernet import Fernet


class AES:
    def __init__(self) -> None:
        pass

    def gen_key(self) -> bytes:
        key = Fernet.generate_key()
        return key

    def gen_cipher(self, key: bytes) -> Fernet:
        cipher_suite = Fernet(key)
        return cipher_suite
