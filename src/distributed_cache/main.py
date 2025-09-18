from distributed_cache.cache import DistributedCache
from distributed_cache.node import Node

def main():
    # Create some nodes
    node1 = Node("node1")
    node2 = Node("node2")
    node3 = Node("node3")

    # Create a distributed cache with the nodes
    cache = DistributedCache(nodes=[node1, node2, node3])

    # Add some data to the cache
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    # Retrieve data from the cache
    print(f"key1: {cache.get('key1')}")
    print(f"key2: {cache.get('key2')}")
    print(f"key3: {cache.get('key3')}")

    # Add a new node
    node4 = Node("node4")
    cache.add_node(node4)
    print("\nAdded node4")

    # The distribution of keys might change
    print(f"key1 is now on node: {cache.ring.get_node('key1').name}")
    print(f"key2 is now on node: {cache.ring.get_node('key2').name}")
    print(f"key3 is now on node: {cache.ring.get_node('key3').name}")

    # Remove a node
    cache.remove_node(node1)
    print("\nRemoved node1")

    # The distribution of keys will change again
    print(f"key1 is now on node: {cache.ring.get_node('key1').name}")
    print(f"key2 is now on node: {cache.ring.get_node('key2').name}")
    print(f"key3 is now on node: {cache.ring.get_node('key3').name}")

if __name__ == "__main__":
    main()
