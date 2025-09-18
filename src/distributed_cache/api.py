from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from .cache import DistributedCache
from .node import Node

app = FastAPI()

# In a real application, you would manage nodes more dynamically.
# For this example, we'll start with a few nodes.
initial_nodes = [Node(name=f"node{i}") for i in range(3)]
cache = DistributedCache(nodes=initial_nodes)

class Item(BaseModel):
    value: str

@app.get("/get/{key}")
def get_value(key: str):
    """
    Retrieve a value from the cache.
    """
    value = cache.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

@app.post("/set/{key}")
def set_value(key: str, item: Item):
    """
    Set a value in the cache.
    """
    try:
        cache.set(key, item.value)
        node = cache.ring.get_node(key)
        return {"message": f"Key '{key}' set on node '{node.name}'"}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{key}")
def delete_value(key: str):
    """
    Delete a value from the cache.
    """
    if cache.delete(key):
        return {"message": f"Key '{key}' deleted"}
    raise HTTPException(status_code=404, detail="Key not found")

@app.get("/nodes", response_model=List[str])
def get_nodes():
    """
    Get the list of nodes in the cache.
    """
    # This is a simplified representation. In a real system, you'd have a better way to list nodes.
    return [node.name for node in set(cache.ring.ring.values())]

@app.post("/nodes/{name}")
def add_node(name: str):
    """
    Add a new node to the cache.
    """
    # Simple check to avoid duplicate node names
    existing_nodes = {node.name for node in set(cache.ring.ring.values())}
    if name in existing_nodes:
        raise HTTPException(status_code=400, detail="Node already exists")
    
    new_node = Node(name)
    cache.add_node(new_node)
    return {"message": f"Node '{name}' added"}

@app.delete("/nodes/{name}")
def remove_node(name: str):
    """
    Remove a node from the cache.
    """
    node_to_remove = None
    for node in set(cache.ring.ring.values()):
        if node.name == name:
            node_to_remove = node
            break
    
    if node_to_remove:
        cache.remove_node(node_to_remove)
        return {"message": f"Node '{name}' removed"}
    
    raise HTTPException(status_code=404, detail="Node not found")
