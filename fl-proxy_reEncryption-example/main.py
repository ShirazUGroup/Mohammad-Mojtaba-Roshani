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

        clg.success(f"""consumed time for peers initialization is {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase one ->    encrypt dataset
        """
        encrypted_data_list: List[str] = []

        for encrypted_data in peers.parallel_encryption():
            encrypted_data_list.append(encrypted_data)

        clg.success(f"""consumed data encryption time is {
            stopwatch.delta()}""")
        stopwatch.reset()

        """
            phase two ->    encrypt alice asymmetric key
            a test to see if bob can open alice encrypted capsule with his own secret key (must be fail)
        """
        alice__assimetric_key_capsule, alice_assimetric_key_encrypted = alice.assimetric_key_encryption()
        clg.debug(debug, f"""the alice encrypted assimetric capsule is {
                  alice__assimetric_key_capsule}""")

        clg.success(f"""consumed symmetric key encryption time is  {
            stopwatch.delta()}""")

        try:
            fail_decrypted_data = bob.pre.decrypt_original(
                capsule=alice__assimetric_key_capsule,
                ciphertext=alice_assimetric_key_encrypted)
        except ValueError:
            clg.warn("decryption failed! Bob doesn't has access granted yet.")
        finally:
            stopwatch.reset()

        """
            phase three ->    grant decryption
            alice provide encryption grant to bob
        """
    else:
        clg.bg_red("i am not production ready yet!")
        sys.exit(1)
