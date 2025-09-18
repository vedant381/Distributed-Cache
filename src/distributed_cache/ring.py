import hashlib
from typing import List, Dict, Optional

from .node import Node

class HashRing:
    """Implements a consistent hash ring."""

    def __init__(self, nodes: Optional[List[Node]] = None, virtual_nodes: int = 3):
        """
        Initializes a new HashRing.

        Args:
            nodes: A list of nodes to add to the ring.
            virtual_nodes: The number of virtual nodes to create for each physical node.
        """
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, Node] = {}
        self.sorted_keys: List[int] = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the hash ring.

        Args:
            node: The node to add.
        """
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node.name}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node: Node) -> None:
        """
        Removes a node from the hash ring.

        Args:
            node: The node to remove.
        """
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node.name}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)

    def get_node(self, key: str) -> Optional[Node]:
        """
        Gets the node responsible for the given key.

        Args:
            key: The key to look up.

        Returns:
            The node responsible for the key, or None if the ring is empty.
        """
        if not self.ring:
            return None

        hash_key = self._hash(key)
        # Find the first key in the sorted list that is greater than or equal to the hash_key
        for node_key in self.sorted_keys:
            if hash_key <= node_key:
                return self.ring[node_key]

        # If no such key is found, wrap around to the first node in the ring
        return self.ring[self.sorted_keys[0]]

    def _hash(self, key: str) -> int:
        """

        Hashes a key to an integer.

        Args:
            key: The key to hash.

        Returns:
            An integer hash value.
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
