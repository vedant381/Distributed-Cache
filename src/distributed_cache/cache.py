from typing import Any, List, Optional

from .node import Node
from .ring import HashRing

class DistributedCache:
    """A distributed cache implementation using a consistent hash ring."""

    def __init__(self, nodes: Optional[List[Node]] = None, virtual_nodes: int = 3):
        """
        Initializes a new DistributedCache.

        Args:
            nodes: A list of initial nodes.
            virtual_nodes: The number of virtual nodes for each physical node.
        """
        self.ring = HashRing(nodes, virtual_nodes)

    def add_node(self, node: Node) -> None:
        """
        Adds a new node to the cache.

        Args:
            node: The node to add.
        """
        self.ring.add_node(node)

    def remove_node(self, node: Node) -> None:
        """
        Removes a node from the cache.

        Args:
            node: The node to remove.
        """
        self.ring.remove_node(node)

    def set(self, key: str, value: Any) -> None:
        """
        Stores a key-value pair in the cache.

        Args:
            key: The key to store.
            value: The value to associate with the key.
        """
        node = self.ring.get_node(key)
        if node:
            node.set(key, value)
        else:
            raise RuntimeError("No nodes available in the cache.")

    def get(self, key: str) -> Any:
        """
        Retrieves a value from the cache by its key.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key, or None if not found.
        """
        node = self.ring.get_node(key)
        if node:
            return node.get(key)
        return None

    def delete(self, key: str) -> bool:
        """
        Deletes a key-value pair from the cache.

        Args:
            key: The key to delete.

        Returns:
            True if the key was deleted, False otherwise.
        """
        node = self.ring.get_node(key)
        if node:
            return node.delete(key)
        return False
