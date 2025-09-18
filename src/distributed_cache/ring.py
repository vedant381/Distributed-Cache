import hashlib
from bisect import bisect_left, insort
from typing import List, Dict, Optional, Set

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
        self._nodes: Set[Node] = set()

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the hash ring.

        Args:
            node: The node to add.
        """
        self._nodes.add(node)
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node.name}:{i}")
            self.ring[key] = node
            insort(self.sorted_keys, key)

    def remove_node(self, node: Node) -> dict:
        """
        Removes a node from the hash ring and returns its data.

        Args:
            node: The node to remove.

        Returns:
            The data stored in the node.
        """
        data_to_return = node._data.copy()
        self._nodes.discard(node)
        
        keys_to_remove = []
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node.name}:{i}")
            if key in self.ring:
                del self.ring[key]
                keys_to_remove.append(key)
        
        if keys_to_remove:
            self.sorted_keys = [k for k in self.sorted_keys if k not in keys_to_remove]
            
        return data_to_return

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
        # Use binary search to find the position
        pos = bisect_left(self.sorted_keys, hash_key)

        # If pos is at the end, wrap around to the first node
        if pos == len(self.sorted_keys):
            pos = 0
        
        return self.ring[self.sorted_keys[pos]]
    
    def get_nodes(self) -> Set[Node]:
        """Returns the set of all nodes in the ring."""
        return self._nodes

    def _hash(self, key: str) -> int:
        """

        Hashes a key to an integer.

        Args:
            key: The key to hash.

        Returns:
            An integer hash value.
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
