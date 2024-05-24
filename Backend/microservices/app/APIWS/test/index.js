const io = require('socket.io-client');

// URL del servidor Socket.io
const serverUrl = 'http://localhost:3000';

// Conexión al servidor
const socket = io.connect(serverUrl);

// Manejar eventos del cliente
socket.on('connect', () => {
    console.log('Conectado al servidor');
});

socket.on('mensaje', (data) => {
    console.log(data);
});

socket.on('disconnect', () => {
    console.log('Desconectado del servidor');
});

// Enviar un mensaje al servidor
socket.emit('mensaje', 'Hola servidor, soy el cliente');
