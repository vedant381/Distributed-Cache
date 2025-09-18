import logging
from typing import Any, List, Optional

from .node import Node
from .ring import HashRing

logging.basicConfig(level=logging.INFO)


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
        Adds a new node to the cache and rebalances only the necessary keys.

        Args:
            node: The node to add.
        """
        logging.info(f"Adding node: {node.name}")
        if any(n.name == node.name for n in self.ring.get_nodes()):
            logging.warning(f"Node {node.name} already exists.")
            return

        self.ring.add_node(node)
        self._rebalance_on_add(node)

    def _rebalance_on_add(self, new_node: Node) -> None:
        """
        Rebalances the keys when a new node is added.
        Only moves keys that should now belong to the new node.
        """
        logging.info(f"Starting rebalance for new node: {new_node.name}")
        keys_to_move = {}

        for existing_node in self.ring.get_nodes():
            if existing_node == new_node:
                continue

            keys_to_check = list(existing_node._data.keys())
            for key in keys_to_check:
                correct_node = self.ring.get_node(key)
                if correct_node == new_node:
                    keys_to_move[key] = existing_node.get(key)
                    existing_node.delete(key)
        
        logging.info(f"Moving {len(keys_to_move)} keys to {new_node.name}.")
        for key, value in keys_to_move.items():
            new_node.set(key, value)
        
        logging.info(f"Rebalance for {new_node.name} complete.")

    def remove_node(self, node: Node) -> None:
        """
        Removes a node from the cache and rehashes its keys.

        Args:
            node: The node to remove.
        """
        logging.info(f"Removing node: {node.name}")
        if not any(n.name == node.name for n in self.ring.get_nodes()):
            logging.warning(f"Node {node.name} not found.")
            return

        data_to_migrate = self.ring.remove_node(node)
        if not data_to_migrate:
            logging.info(f"Node {node.name} was empty. No keys to migrate.")
            return

        logging.info(f"Migrating {len(data_to_migrate)} keys from removed node {node.name}.")
        for key, value in data_to_migrate.items():
            self.set(key, value)
        logging.info(f"Migration from {node.name} complete.")

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
