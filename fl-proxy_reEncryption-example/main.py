#############
#   MODULES #
#############
import sys
import argparse
from typing import List
from helpers.console import Console
from helpers.random import Random
from helpers.stopwatch import Stopwatch
from components.peer import Peer
from components.peers_creator import PeersCreator


###########
#   utils #
###########


def _generate_random_peer_names(count: int) -> List[str]:
    peer_names: List[str] = []
    for _ in range(count):
        random_hex_name = Random().generate_random_hex()
        peer_names.append(random_hex_name)
    return peer_names


def parse_arguments():
    parser = argparse.ArgumentParser(description="Secure Federated Learning")

    parser.add_argument("dataset_path",
                        help="Dataset path")
    parser.add_argument("--debug_mode", action="store_true",
                        help="Enable debug mode to print extra information", default=False)

    parser.add_argument("--peer_counts", action="store_true",
                        help="Enable debug mode to print extra information", default=3)

    return parser.parse_args()

#################
#   starter kit #
#################


if __name__ == "__main__":
    args = parse_arguments()
    clg = Console()
    debug: bool = args.debug_mode
    stopwatch = Stopwatch()

    if debug:
        """
            phase zero ->   peers initialization
        """
        peers = PeersCreator(debug, stopwatch, args.peer_counts, args.dataset_path,
                             _generate_random_peer_names(args.peer_counts))

        alice: Peer = peers.peer_list[0]
        bob: Peer = peers.peer_list[1]
        idle: Peer = peers.peer_list[2]

        clg.success(f"""consumed time for peers initialization is {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase one ->    encrypt dataset
        """

        encrypted_data_list: List[str] = []

        for encrypted_data in peers.parallel_encryption():
            encrypted_data_list.append(encrypted_data)

        alice_encrypted_dataframe: bytes = encrypted_data_list[0]
        bob_encrypted_dataframe: bytes = encrypted_data_list[1]

        clg.success(f"""consumed data encryption time is {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase two ->    encrypt alice asymmetric key
            -   a test to see if bob can open alice encrypted capsule with his own secret key (must be fail)
        """

        alice_assimetric_key_capsule, alice_assimetric_key_encrypted = alice.assimetric_key_encryption()
        clg.debug(debug, f"""the alice encrypted assimetric capsule is {
                  alice_assimetric_key_capsule}""")

        clg.success(f"""consumed symmetric key encryption time is  {
            stopwatch.delta()}""")

        try:
            fail_decrypted_data = bob.pre.decrypt_original(
                capsule=alice_assimetric_key_capsule,
                ciphertext=alice_assimetric_key_encrypted)
        except ValueError:
            clg.warn("decryption failed! Bob doesn't has access granted yet")
        finally:
            stopwatch.reset()

        """
            phase three ->    grant decryption
            -   alice provide encryption grant to bob
            -   giving bob public key only
            -   `kfrags` stands for `re-encryption key fragments`
        """

        alice_kfrags = alice.pre.transfer_encryption_grant(
            bob.pre.public_key, 2, 3)
        clg.success(f"""consumed time for transfer encryption grant is  {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase four ->    this phase includes several steps:
            1)  alice sends here `kfrags` to proxy(ies)
                -   note that the network consist of three node and each node can have a
                    -   `federated learning node` role,
                    -   `proxy` role,
                    -   `compute` role,
                    -   `data storage` role,
                    -   all of the above role.
                    for example in this problem:
                        -   alice is `federated learning node` and `proxy`
                        -   bob is `compute`
                        -   the third other node is `proxy`
            2)  bob asks these proxies to re-encrypt the `alice_assimetric_key_capsule` so he can open it
            3)  bob must receive at lease same amount as `threshold` from `shares` to be able active the `alice_assimetric_key_capsule`
            4)  bob collect these frames by the name of `cfrags`
        """
        alice_proxy_cfrags = alice.pre.re_encryption(
            alice_assimetric_key_capsule, alice_kfrags, 2)
        idle_proxy_cfrags = idle.pre.re_encryption(
            alice_assimetric_key_capsule, alice_kfrags, 2)

        clg.success(f"""consumed time for ReEncryption on two is  {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase five ->    bob must insure that capsule came from alice
        """
        # TODO: implementation
        """
            phase six ->    bob now can open the `alice_capsule`
        """

        try:
            symmetric_key_clear_text_decrypted_by_bob = bob.pre.decrypt(
                bob.pre.secret_key,
                alice.pre.public_key,
                alice_assimetric_key_capsule,  # or idle_assimetric_key_capsule
                alice_proxy_cfrags,
                alice_assimetric_key_encrypted)

            if alice._key == symmetric_key_clear_text_decrypted_by_bob:
                clg.bg_green(
                    f"bob encrypted alice symmetric key and the key is {symmetric_key_clear_text_decrypted_by_bob}")
        except ValueError:
            clg.error("decryption failed! Bob doesn't has access granted")
        finally:
            stopwatch.reset()

        clg.success(f"""consumed time for bob to decrypt the alice's symmetric key is  {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase seven ->    bob now can open the alice dataset
            -   bob must not be able to decrypt the `alice_encrypted_dataframe`
                by its own symmetric key
        """

        alice_decrypted_dataframe_by_bob = bob.decrypt_dataframe(
            symmetric_key_clear_text_decrypted_by_bob, alice_encrypted_dataframe)

        clg.debug(debug, f"""alice decrypted dataframe by bob is:\n{
                  alice_decrypted_dataframe_by_bob.head()}""")

        clg.success(f"""consumed time for bob to decrypt alice dataset is {
            stopwatch.delta()}""")
        stopwatch.reset()

        try:
            _ = bob.decrypt_dataframe(
                bob._key, alice_encrypted_dataframe)
        except:
            clg.error(
                "decryption failed! bob must use the given symmetric key by alice")

        """
            end
        """
        clg.success(f"""total consumed time is  {stopwatch.get_total()}""")
    else:
        clg.bg_red("i am not production ready yet!")
        sys.exit(1)
