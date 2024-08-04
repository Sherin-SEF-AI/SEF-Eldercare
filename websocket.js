const socket = new WebSocket('ws://localhost:5000/socket');

socket.onopen = function(event) {
    console.log('WebSocket connection established.');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'alert') {
        alert(`New alert: ${data.message}`);
    }
};

socket.onclose = function(event) {
    console.log('WebSocket connection closed.');
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};
