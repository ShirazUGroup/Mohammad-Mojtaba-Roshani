from typing import List
from helpers.console import Console
from time import time
from components.peer import Peer
import pandas as pd
import numpy as np
import multiprocessing


class PeersCreator:
    _clg = None
    peers: List[Peer] = []

    def __init__(self, debug_mode: bool, stopwatch: float, count: int, dataset_path: str, peer_names=List[str]) -> None:

        self._clg = Console()

        if count % 2 == 0:
            self._clg.error("please pass odd number of peers")
            raise TypeError("please pass odd number of peers")

        if len(peer_names) != count:
            self._clg.error("peer_names must have the same length like count")
            raise TypeError("peer_names must have the same length like count")

        self._clg.bg_blue(f"creating {count} peers...")
        self.peers = self._create_peers(debug_mode, stopwatch, count,
                                        dataset_path, peer_names)

    def _create_peers(self, debug_mode: bool, stopwatch: float, count: int, dataset_path: str, peer_names: List[str]) -> List[Peer]:
        peers: List[Peer] = []

        self._clg.debug(debug_mode, f"reading dataset from {dataset_path}...")

        df = pd.read_csv(dataset_path)
        sub_df = np.array_split(df, count)

        for i in range(count):
            peer = Peer(debug_mode, stopwatch, sub_df[i], peer_names[i])
            peers.append(peer)

        return peers

    def get_peers(self):
        return self.peers

    def parallel_encryption(self) -> bool:
        processes = []
        for peer in self.peers:
            peer.encrypt_local()
        #     process = multiprocessing.Process(target=peer.encrypt_local)
        #     processes.append(process)
        #     process.start()

        # for process in processes:
        #     process.join()

        return True
