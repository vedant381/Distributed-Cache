import unittest

from src.distributed_cache.cache import DistributedCache
from src.distributed_cache.node import Node


class TestDistributedCache(unittest.TestCase):

    def test_remove_node_and_migrate_keys(self):
        """
        Tests that when a node is removed, its keys are migrated to the next node in the ring.
        """
        # 1. Create a cache with 3 nodes
        nodes = [Node(f"node{i}") for i in range(3)]
        cache = DistributedCache(nodes)

        # 2. Add some data to the cache
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        # 3. Get the node for a key
        node_for_key1 = cache.ring.get_node("key1")
        self.assertIsNotNone(node_for_key1)

        # 4. Remove the node
        cache.remove_node(node_for_key1)

        # 5. Verify that the data is still accessible
        self.assertEqual(cache.get("key1"), "value1")

        # 6. Verify that the key is now on a different node
        new_node_for_key1 = cache.ring.get_node("key1")
        self.assertIsNotNone(new_node_for_key1)
        self.assertNotEqual(node_for_key1.name, new_node_for_key1.name)

    def test_add_node_and_rebalance_keys(self):
        """
        Tests that when a new node is added, the keys are rebalanced.
        """
        # 1. Create a cache with 2 nodes
        nodes = [Node(f"node{i}") for i in range(2)]
        cache = DistributedCache(nodes)

        # 2. Add some data
        for i in range(10):
            cache.set(f"key{i}", f"value{i}")

        # 3. Get the initial distribution of keys
        initial_distribution = {node.name: len(node._data) for node in nodes}

        # 4. Add a new node
        new_node = Node("node2")
        cache.add_node(new_node)

        # 5. Verify that the keys are rebalanced
        new_distribution = {node.name: len(node._data) for node in set(cache.ring.ring.values())}
        
        # Check that the new node has some keys
        self.assertGreater(new_distribution.get("node2", 0), 0)
        
        # Check that the total number of keys is the same
        self.assertEqual(sum(initial_distribution.values()), sum(new_distribution.values()))


if __name__ == '__main__':
    unittest.main()
