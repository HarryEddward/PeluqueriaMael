const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:3000/test');
console.log('wtf?')

ws.on('open', function open() {
  console.log('Connected to WebSocket server');
  
  // Envía un mensaje al servidor WebSocket
  ws.send('Hello, server!');
});

ws.on('message', function incoming(data) {
  console.log('Received message from server:', data);
});

ws.on('close', function close() {
  console.log('Disconnected from WebSocket server');
});
