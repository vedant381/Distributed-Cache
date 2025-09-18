new Vue({
    el: '#app',
    data: {
        nodes: [],
        newKey: '',
        newValue: '',
        keyToDelete: '',
        newNodeName: '',
        nodeToRemove: '',
        apiBaseUrl: 'http://127.0.0.1:8000'
    },
    methods: {
        async fetchState() {
            try {
                const nodesResponse = await fetch(`${this.apiBaseUrl}/nodes`);
                const nodeNames = await nodesResponse.json();
                
                const nodePromises = nodeNames.map(async (nodeName) => {
                    const dataResponse = await fetch(`${this.apiBaseUrl}/data/${nodeName}`);
                    const data = await dataResponse.json();
                    return { name: nodeName, data: data.data };
                });

                this.nodes = await Promise.all(nodePromises);
            } catch (error) {
                console.error('Error fetching cache state:', error);
                alert('Failed to fetch cache state. Make sure the backend is running.');
            }
        },
        async setKey() {
            if (!this.newKey || !this.newValue) {
                alert('Please provide both a key and a value.');
                return;
            }
            try {
                await fetch(`${this.apiBaseUrl}/set/${this.newKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ value: this.newValue })
                });
                this.newKey = '';
                this.newValue = '';
                this.fetchState();
            } catch (error) {
                console.error('Error setting key:', error);
                alert('Failed to set key.');
            }
        },
        async deleteKey() {
            if (!this.keyToDelete) {
                alert('Please provide a key to delete.');
                return;
            }
            try {
                await fetch(`${this.apiBaseUrl}/delete/${this.keyToDelete}`, {
                    method: 'DELETE'
                });
                this.keyToDelete = '';
                this.fetchState();
            } catch (error) {
                console.error('Error deleting key:', error);
                alert('Failed to delete key.');
            }
        },
        async addNode() {
            if (!this.newNodeName) {
                alert('Please provide a node name.');
                return;
            }
            try {
                await fetch(`${this.apiBaseUrl}/nodes/${this.newNodeName}`, {
                    method: 'POST'
                });
                this.newNodeName = '';
                this.fetchState();
            } catch (error) {
                console.error('Error adding node:', error);
                alert('Failed to add node.');
            }
        },
        async removeNode() {
            if (!this.nodeToRemove) {
                alert('Please provide a node name to remove.');
                return;
            }
            try {
                await fetch(`${this.apiBaseUrl}/nodes/${this.nodeToRemove}`, {
                    method: 'DELETE'
                });
                this.nodeToRemove = '';
                this.fetchState();
            } catch (error) {
                console.error('Error removing node:', error);
                alert('Failed to remove node.');
            }
        }
    },
    created() {
        this.fetchState();
    }
});
