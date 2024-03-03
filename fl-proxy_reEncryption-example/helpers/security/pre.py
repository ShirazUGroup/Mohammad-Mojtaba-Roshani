from typing import List, Tuple
from ..console import Console
from umbral import Capsule, PublicKey, SecretKey, Signer, VerifiedCapsuleFrag, VerifiedKeyFrag, decrypt_reencrypted, encrypt, decrypt_original, generate_kfrags, reencrypt
from umbral.keys import PublicKey as PKT, SecretKey as SKT


class ProxyReEncryption:
    _clg: Console
    _debug: bool
    secret_key: SKT
    signing_key: SKT
    public_key: PKT
    verifying_key: PKT
    signer: None

    def __init__(self, debug_mode: bool) -> None:
        self._debug = debug_mode
        self._clg = Console()
        self._clg.debug(self._debug, "initializing the pre")

        # assignment
        self.secret_key = SecretKey.random()
        signing_key = SecretKey.random()

        self.public_key = self.secret_key.public_key()

        self.signing_key = SecretKey.random()
        self.verifying_key = signing_key.public_key()
        self.signer = Signer(signing_key)

    def encryption(self, plaintext: bytes) -> Tuple[Capsule, bytes]:
        capsule, ciphertext = encrypt(self.public_key, plaintext)
        return capsule, ciphertext

    def decrypt_original(self, capsule: Capsule, ciphertext: bytes) -> bytes:

        cleartext = decrypt_original(self.secret_key, capsule, ciphertext)

        return cleartext

    def transfer_encryption(self, receiving_pk: PublicKey, threshold: int = 1, shares: int = 10) -> List[VerifiedKeyFrag]:

        kfrags = generate_kfrags(delegating_sk=self.secret_key,
                                 receiving_pk=receiving_pk,
                                 signer=self.signer,
                                 threshold=threshold,
                                 shares=shares)

        return kfrags

    def re_encryption(self, capsule: Capsule, kfrags: List[VerifiedKeyFrag], kfrag: VerifiedKeyFrag, threshold: int = 1,):

        cfrags = list()                     # receiver cfrag collection
        for kfrag in kfrags[:threshold]:
            cfrag = reencrypt(capsule=capsule, kfrag=kfrag)
            cfrags.append(cfrag)

        return cfrags

    def decrypt(self, receiver_secret_key, sender_public_key, capsule: Capsule, cfrags: List[VerifiedCapsuleFrag], ciphertext: bytes) -> bytes:
        cleartext = decrypt_reencrypted(receiving_sk=receiver_secret_key,
                                        delegating_pk=sender_public_key,
                                        capsule=capsule,
                                        cfrags=cfrags,
                                        ciphertext=ciphertext)

        return cleartext
