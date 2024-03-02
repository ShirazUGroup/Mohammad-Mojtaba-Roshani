#############
#   MODULES #
#############
import sys
import argparse
from typing import List
from helpers.console import Console
from helpers.random import Random
from helpers.system import System
from components.peers_creator import PeersCreator
from time import time


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
                        help="Enable debug mode to print extra information", default=(System().get_cpu_core_count() - 1))

    return parser.parse_args()

#################
#   starter kit #
#################


if __name__ == "__main__":
    stopwatch = time()
    args = parse_arguments()
    clg = Console()

    if args.debug_mode:
        peers = PeersCreator(args.debug_mode, stopwatch, args.peer_counts, args.dataset_path,
                             _generate_random_peer_names(args.peer_counts))
        peers.parallel_encryption()

    else:
        clg.bg_red("i am not production ready")
        sys.exit(1)
