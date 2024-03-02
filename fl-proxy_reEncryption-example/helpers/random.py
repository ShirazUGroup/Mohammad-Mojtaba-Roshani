import secrets


class Random:
    def __init__(self) -> None:
        pass

    def generate_random_hex(self, length: int = 6) -> str:
        return secrets.token_hex(length // 2)
