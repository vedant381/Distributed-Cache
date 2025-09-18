from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from .cache import DistributedCache
from .node import Node

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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
    return [node.name for node in cache.ring.get_nodes()]

@app.post("/nodes/{name}")
def add_node(name: str):
    """
    Add a new node to the cache.
    """
    # The check for existing nodes is now handled in cache.add_node
    new_node = Node(name)
    cache.add_node(new_node)
    return {"message": f"Node '{name}' added"}

@app.delete("/nodes/{name}")
def remove_node(name: str):
    """
    Remove a node from the cache.
    """
    node_to_remove = None
    for node in cache.ring.get_nodes():
        if node.name == name:
            node_to_remove = node
            break
    
    if node_to_remove:
        cache.remove_node(node_to_remove)
        return {"message": f"Node '{name}' removed"}
    
    raise HTTPException(status_code=404, detail="Node not found")

@app.get("/data/{node_name}", response_model=Dict)
def get_node_data(node_name: str):
    """
    Retrieve all data from a specific node.
    """
    node_to_find = None
    for node in cache.ring.get_nodes():
        if node.name == node_name:
            node_to_find = node
            break
    
    if node_to_find:
        return {"data": node_to_find._data}
    
    raise HTTPException(status_code=404, detail="Node not found")
