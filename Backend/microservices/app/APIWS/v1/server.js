// server.js

'use strict';

var colors = require('colors');
const path = require('path');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const r = require('rethinkdb');
const { Config } = require('../../../conversor/config/config');

const config = Config();

const port = config.app.APIWS.net.port;
const ssl = config.app.APIWS.ssl;
const host = config['host'];
const v = config['name_version']

const app = express();
app.use(cors({ origin: '*' }));


const server = http.createServer(app);
const io = socketIo(server);


const v_proj = path.basename(path.resolve(__dirname, '.')).toLowerCase();
const name_proj = path.basename(path.resolve(__dirname, '..')).toLowerCase();

/*
 * Comprueba si la ruta esta relacionada con la
 * estrctura de la capreta y el archivo principal
 * de configruación con la versión
 */
// console.log(v_proj, v, name_proj, 'apiws');

if (v_proj === v && name_proj === 'apiws'){
    var basePath = `/${name_proj}/app/api/${v}`;
    //module.exports += { basePath };
}
else if (v_proj !== v) {
    console.log('La versión no cuadra con el de la API'.red);

} else if (name_proj !== 'apiws') {
    console.log('El nombre del proyecto no cuadra con el de la API'.red);

} else {
    console.log('La versión/nombre del proyecto no cuadra con el de la API'.red);
}


/**
 * Junta el prefijo de la misma api para juntarlo con el
 * prefijo de la msima ruta
 */
const router = (path) => basePath + path;

module.exports = { config, basePath, router };


// Local pkg
const database = require('./db/database');
const AsyncTable = require('./db/asyncTable');

database.connect().then(() => {
    
    const table = new AsyncTable('Reservas');
    table.start();
    table.on('change', (row) => {
        io.emit('booking_card_change', row);
    });

})
.catch((err) => {
    console.error('Se desconecto de forma repentina la base de datos:', err);
});


// Rutas Estaticas
app.get('/status', (req, res) => {
    res.json({
        'info': 'Servidor Socket.io funcionando correctamente.',
        'status': 'ok'
    });
});

app.get('/routes', (req, res) => {
    res.json({
        'data': available_routes
    });
});


/**
 * RUTA GENERAL WS
 */
/*
const general_rp = router('/general');
const generalNamespace = io.of(general_rp);

generalNamespace.on('connection', (socket) => {
    console.log('Un cliente se ha conectado');

    // Ruta: "booking_card_change"
    socket.on('booking_card_change', (data) => {
        console.log(data);
    });

    
    socket.on('status', (data) => {
        socket.emit('status', 'ok');
    });
    

    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });
});
*/

const PORT = process.env.PORT || port;
const HOST = host;
const secure = ssl ? "wss" : "ws";
const base_url = `${secure}://${HOST}:${PORT}`

server.listen(PORT, () => {
    console.log('\nENCENDIENDO SERVIDOR...'.green);
    console.log('->'.bgGreen + ` Servidor Socket.io escuchando en el puerto`.underline + ' ' + ` ${base_url} `.underline.bgGreen);
});

/**
 * ROUTES
 * ------
 * rp -> router_prefix
 */
/*
var available_routes = {};
const formatUrl = (rp) => base_url + rp;

//-------------
const {
    Router: booking_card_change,
    router_prefix: booking_card_change_rp
} = require('./namespaces/rethinkdb/booking_card_change');

booking_card_change(io);
//-------------

available_routes['general'] = formatUrl(general_rp);
available_routes['booking_card_change'] = formatUrl(booking_card_change_rp);

console.log(available_routes);
*/
//*
 //* 
 //* Que hacer?
 //* 
 //* - Crear unarchivo de node.js para su configuracion
 //* - O crear un archivo json para luego adaptarlo a su lengauje!
 //*
