// index.js
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const r = require('rethinkdb');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
    cors: {
        origin: "http://localhost:5173", // Permite solicitudes desde tu frontend
        methods: ["GET", "POST"],
        allowedHeaders: ["Content-Type"],
        credentials: true
    }
});

// Habilitar CORS en todas las rutas de Express
app.use(cors());

const dbName = 'PeluqueriaMael'; // Cambia esto si tienes otro nombre de base de datos
const tableName = 'Reservas';

// Conexión a RethinkDB
r.connect({ host: 'localhost', port: 28015 }, (err, conn) => {
    if (err) throw err;

    // Asegúrate de que la base de datos y la tabla existan
    r.dbList().contains(dbName)
        .do(dbExists => r.branch(dbExists, { created: 0 }, r.dbCreate(dbName)))
        .run(conn, (err) => {
            if (err) throw err;

            r.db(dbName).tableList().contains(tableName)
                .do(tableExists => r.branch(tableExists, { created: 0 }, r.db(dbName).tableCreate(tableName)))
                .run(conn, (err) => {
                    if (err) throw err;

                    // Escucha cambios en la tabla
                    r.db(dbName).table(tableName).changes().run(conn, (err, cursor) => {
                        if (err) throw err;
                        
                        cursor.each((err, change) => {
                            if (err) throw err;
                            io.emit('data_update', change);
                        });
                    });
                });
        });
});

// Servir archivos estáticos del directorio "public"
app.use(express.static('public'));

io.on('connection', (socket) => {
    console.log('Nuevo cliente conectado');

    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });
});

// Inicia el servidor
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});
