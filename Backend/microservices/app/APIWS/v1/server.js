// server.js

'use strict';

var colors = require('colors');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const r = require('rethinkdb');
const { Config } = require('../../conversor/config/config');

const config = Config();
module.exports = { config };

const port = config.app.APIWS.net.port;
const host = config['host'];

const app = express();
const server = http.createServer(app);
const io = socketIo(server);


// Local pkg
const database = require('./db/database');
const AsyncTable = require('./db/asyncTable');

database.connect().then(() => {
    
    const table = new AsyncTable('booking_card');
    table.start();
    table.on('change', (row) => {
        io.emit('booking_card_change', row);
    })

})
.catch((err) => {
    console.error('Se desconecto de forma repentina la base de datos:', err);
});



// Ruta de prueba
app.get('/', (req, res) => {
    res.send('Servidor Socket.io funcionando correctamente.');
});

// Manejo de conexiones de Socket.io
io.on('connection', (socket) => {
    console.log('Un cliente se ha conectado');

    // Ruta: "booking_card_change"
    socket.on('booking_card_change', (data) => {

    });

    socket.on('status', (data) => {
        socket.emit('status', 'ok');
    });

    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });
});

const PORT = process.env.PORT || port;
const HOST = host;
server.listen(PORT, () => {
    console.log('\nENCENDIENDO SERVIDOR...'.green);
    console.log('->'.bgGreen + ` Servidor Socket.io escuchando en el puerto`.underline + ' ' + ` ws://${HOST}:${PORT} `.underline.bgGreen);
});


/**
 * 
 * Que hacer?
 * 
 * - Crear unarchivo de node.js para su configuracion
 * - O crear un archivo json para luego adaptarlo a su lengauje!
 */
