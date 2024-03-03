from cryptography.fernet import Fernet


class AES:
    @staticmethod
    def gen_key() -> bytes:
        key = Fernet.generate_key()
        return key

    @staticmethod
    def gen_cipher(key: bytes) -> Fernet:
        cipher_suite = Fernet(key)
        return cipher_suite
