import typer
import requests
from typing import Optional

app = typer.Typer()

BASE_URL = "http://127.0.0.1:8000"

@app.command()
def get(key: str):
    """
    Get a value from the cache.
    """
    response = requests.get(f"{BASE_URL}/get/{key}")
    if response.status_code == 200:
        typer.echo(response.json()["value"])
    else:
        typer.echo(f"Error: {response.text}")

@app.command()
def set(key: str, value: str):
    """
    Set a value in the cache.
    """
    response = requests.post(f"{BASE_URL}/set/{key}", json={"value": value})
    if response.status_code == 200:
        typer.echo(f"Value set for key '{key}'")
    else:
        typer.echo(f"Error: {response.text}")

@app.command()
def delete(key: str):
    """
    Delete a value from the cache.
    """
    response = requests.delete(f"{BASE_URL}/delete/{key}")
    if response.status_code == 200:
        typer.echo(f"Value for key '{key}' deleted")
    else:
        typer.echo(f"Error: {response.text}")

@app.command()
def add_node(node: str):
    """
    Add a new node to the cache ring.
    """
    response = requests.post(f"{BASE_URL}/nodes/{node}")
    if response.status_code == 200:
        typer.echo(f"Node '{node}' added")
    else:
        typer.echo(f"Error: {response.text}")

@app.command()
def remove_node(node: str):
    """
    Remove a node from the cache ring.
    """
    response = requests.delete(f"{BASE_URL}/nodes/{node}")
    if response.status_code == 200:
        typer.echo(f"Node '{node}' removed")
    else:
        typer.echo(f"Error: {response.text}")

@app.command()
def list_nodes():
    """
    List all nodes in the cache ring.
    """
    response = requests.get(f"{BASE_URL}/nodes")
    if response.status_code == 200:
        nodes = response.json()
        for node in nodes:
            typer.echo(node)
    else:
        typer.echo(f"Error: {response.text}")


if __name__ == "__main__":
    app()
