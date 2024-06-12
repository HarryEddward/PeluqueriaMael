const io = require('socket.io-client');

// Cambia esto a la URL que tu servidor está escuchando
const socket = io('ws://localhost:8100/apiws/app/api/v1/booking_card_change');

console.log('wtf?');

socket.on('connect', () => {
  console.log('Connected to WebSocket server');
  
  // Envía un mensaje al servidor WebSocket
  socket.emit('init', 'Hello, server!');
});

socket.on('message', (data) => {
  console.log('Received message from server:', data);
});

socket.on('disconnect', () => {
  console.log('Disconnected from WebSocket server');
});
