// server.js

'use strict';

var colors = require('colors');
const path = require('path');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const r = require('rethinkdb');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const { Config } = require('../../../conversor/config/config');
const database = require('./db/database');
const AsyncTableBookingSheet = require('./db/asyncTableBookingSheet');
const { isValidISODate } = require('./services/iso');
const { replaceAt } = require('./utils/index');

const config = Config();

const port = config.app.APIWS.net.port;
const ssl = config.app.APIWS.ssl;
const host = config['host'];
const v = config['name_version']

const app = express();
app.use(cors({ origin: '*', credentials: true }));


const server = http.createServer(app);
const io = socketIo(server);

const protocol_verified_ws = () => ssl ? 'wss' : 'ws'
const protocol_verified_http = () => ssl ? 'https' : 'http'

// Configuración Swagger
const swaggerOptions = {
    swaggerDefinition: {
        openapi: '3.0.0',
        info: {
            title: 'APIWS (API WebSockets)',
            version: '1.0.0',
            description: 'An real time API operations with RethinkDB',
        },
        servers: [
            {
                url: `${protocol_verified_ws()}://${host}:${port}`
            },
            {
                url: `${protocol_verified_http()}://${host}:${port}`
            }
        ],
    },
    apis: ['./swaggerDoc.js', './server.js'], // Tu archivo de documentación
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));


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
//const router = (path) => basePath + path;

//module.exports = { config, basePath, router };


const base_url_ws_router_retinkdb = "/rethinkdb";


database.connect().then(() => {
    
    
    io.on('connection', (socket) => {
        console.log("Cliente conectado");

        // Escuchar evento del cliente para recibir la fecha
        socket.on('set_date_filter', (isoDate) => {
            console.log(`Fecha recibida del cliente: ${isoDate}`);
            
            //console.log(`${isValidISODate(isoDate)}`);

            // Validar si la fecha es válida y tiene el formato ISO 8601
            if (!isValidISODate(isoDate)) {
                socket.emit('error', 'Fecha inválida. Por favor, use el formato ISO 8601.');
                socket.disconnect();
            }

            //isoDate = isoJsToIsoPy(isoDate);
            const isoDateFormated = isoDate.slice(0,19)

            const table = new AsyncTableBookingSheet('Reservas', isoDateFormated);

            // console.log("Fecha válida en formato ISO");
            //socket.emit('booking_card_change', "hello");

            // Iniciar la escucha de cambios en la tabla solo si la fecha es válida
            table.start();

            // Emitir solo los cambios que coincidan con la fecha
            table.on('change', (row) => {
                //const bookingDate = new Date(row.new_val.fecha_reserva).toISOString();
                
                console.log(`->CHANGES: ${row}`);
                // Compara la fecha del cliente con la fecha del cambio en la tablas
                socket.emit('booking_card_change', row);
                
            });
        });

        socket.on('disconnect', () => {
            console.log("Cliente desconectado");
        });
    });
}).catch((err) => {
    console.error('Se desconectó de la base de datos:', err);
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

// Opción 1: Usar una carpeta estática (recomendado si tienes varios archivos HTML)
app.use(express.static(path.join(__dirname, 'view')));

// Opción 2: Enviar un archivo HTML específico cuando visitas una ruta
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'view', 'index.html'));
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
