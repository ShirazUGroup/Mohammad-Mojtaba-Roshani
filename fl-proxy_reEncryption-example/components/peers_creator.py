from typing import Generator, List

from traitlets import Any
from helpers.console import Console
from helpers.stopwatch import Stopwatch
from components.peer import Peer
import pandas as pd
import numpy as np


class PeersCreator:
    _clg = None
    peer_list: List[Peer] = []

    def __init__(self, debug_mode: bool, stopwatch: Stopwatch, count: int, dataset_path: str, peer_names=List[str]) -> None:

        self._clg = Console()

        if count % 2 == 0:
            self._clg.error("please pass odd number of peers")
            raise TypeError("please pass odd number of peers")

        if len(peer_names) != count:
            self._clg.error("peer_names must have the same length like count")
            raise TypeError("peer_names must have the same length like count")

        self._clg.bg_blue(f"creating {count} peers...")
        self.peer_list = self._create_peers(debug_mode, stopwatch, count,
                                            dataset_path, peer_names)

    def _create_peers(self, debug_mode: bool, stopwatch: Stopwatch, count: int, dataset_path: str, peer_names: List[str]) -> List[Peer]:
        peers: List[Peer] = []

        self._clg.debug(debug_mode, f"reading dataset from {dataset_path}...")

        df = pd.read_csv(dataset_path)
        sub_df = np.array_split(df, count)

        for i in range(count):
            peer = Peer(debug_mode, stopwatch, sub_df[i], peer_names[i])
            peers.append(peer)

        return peers

    def get_peers(self):
        return self.peer_list

    # TODO: make it parallel
    # TODO: make it type safe
    def parallel_encryption(self) -> Generator[Any, Any, Any]:

        for peer in self.peer_list:
            yield peer.encrypt_local()
