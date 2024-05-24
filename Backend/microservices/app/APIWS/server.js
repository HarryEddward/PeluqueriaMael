'use strict';

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const r = require('rethinkdb');


const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Local pkg
const database = require('./db/database');
const AsyncTable = require('./db/asyncTable');

database.connect().then(() => {
    
    const table = new AsyncTable('authors');
    table.start();
    table.on('change', (row) => {
        io.emit('mensaje', row);
    })

})
.catch((err) => {
    console.error('Error al conectar a la base de datos:', err);
});



// Ruta de prueba
app.get('/', (req, res) => {
    res.send('Servidor Socket.io funcionando correctamente.');
});

// Manejo de conexiones de Socket.io
io.on('connection', (socket) => {
    console.log('Un cliente se ha conectado');

    // Manejar eventos de ejemplo
    socket.on('mensaje', (data) => {
        //console.log('Mensaje recibido:', data);
        // Puedes hacer cualquier cosa con el mensaje recibido aquí
        //socket.emit('mensaje', '¡Mensaje recibido! A llegado el mensaje.');

    });

    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Servidor Socket.io escuchando en el puerto ${PORT}`);
});
