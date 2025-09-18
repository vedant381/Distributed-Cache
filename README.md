# Distributed Cache

A simple distributed cache implementation in Python using FastAPI.

## How to run

1.  Install dependencies:
    ```bash
    poetry install
    ```
2.  Run the application:
    ```bash
    poetry run uvicorn distributed_cache.main:app --reload
    ```

## API Usage

The API will be available at `http://127.0.0.1:8000`.

### Set a value

To store a key-value pair in the cache:

```bash
curl -X POST "http://127.0.0.1:8000/set/mykey" -H "Content-Type: application/json" -d '{"value": "myvalue"}'
```

### Get a value

To retrieve a value for a given key:

```bash
curl -X GET "http://127.0.0.1:8000/get/mykey"
```

### Delete a value

To delete a key-value pair:

```bash
curl -X DELETE "http://127.0.0.1:8000/delete/mykey"
```

### List nodes

To see the list of nodes in the cache ring:

```bash
curl -X GET "http://127.0.0.1:8000/nodes"
```

### Add a node

To add a new node to the cache ring:

```bash
curl -X POST "http://127.0.0.1:8000/nodes/node3"
```

### Remove a node

To remove a node from the cache ring:

```bash
curl -X DELETE "http://127.0.0.1:8000/nodes/node2"

## How to run the CLI locally

1.  **Run the main application:**
    Open a terminal and run the following command to start the distributed cache server:
    ```bash
    poetry run uvicorn distributed_cache.main:app --reload
    ```

2.  **Run CLI commands:**
    Open a *new* terminal, and activate the virtual environment:
    ```bash
    source $(poetry env info --path)/bin/activate
    ```
    Now you can run the CLI commands directly.

## CLI Usage

### Set a value

```bash
cli set mykey myvalue
```

### Get a value

```bash
cli get mykey
```

### Delete a value

```bash
cli delete mykey
```

### Add a node

```bash
cli add-node node3
```

### Remove a node

```bash
cli remove-node node2
```

### List nodes

```bash
cli list-nodes
```
