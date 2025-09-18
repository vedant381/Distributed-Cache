from typing import Any

class Node:
    """Represents a node in the distributed cache."""

    def __init__(self, name: str):
        """
        Initializes a new Node.

        Args:
            name: The name of the node (e.g., server IP address).
        """
        if not name:
            raise ValueError("Node name cannot be empty.")
        self.name = name
        self._data = {}

    def set(self, key: str, value: Any) -> None:
        """
        Stores a key-value pair in the node.

        Args:
            key: The key to store.
            value: The value to associate with the key.
        """
        self._data[key] = value

    def get(self, key: str) -> Any:
        """
        Retrieves a value from the node by its key.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key, or None if not found.
        """
        return self._data.get(key)

    def delete(self, key: str) -> bool:
        """
        Deletes a key-value pair from the node.

        Args:
            key: The key to delete.

        Returns:
            True if the key was deleted, False otherwise.
        """
        if key in self._data:
            del self._data[key]
            return True
        return False

    def __repr__(self) -> str:
        return f"Node('{self.name}')"
