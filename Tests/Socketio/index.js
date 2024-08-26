const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const r = require('rethinkdb');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
    cors: {
        origin: "http://localhost:5173",
        methods: ["GET", "POST"],
        allowedHeaders: ["Content-Type"],
        credentials: true
    }
});

const dbName = 'PeluqueriaMael';
const tableName = 'Reservas';

app.use(cors());

r.connect({ host: 'localhost', port: 28015 }, (err, conn) => {
    if (err) throw err;

    r.dbList().contains(dbName)
        .do(dbExists => r.branch(dbExists, { created: 0 }, r.dbCreate(dbName)))
        .run(conn, (err) => {
            if (err) throw err;

            r.db(dbName).tableList().contains(tableName)
                .do(tableExists => r.branch(tableExists, { created: 0 }, r.db(dbName).tableCreate(tableName)))
                .run(conn, (err) => {
                    if (err) throw err;

                    io.on('connection', (socket) => {
                        console.log('Nuevo cliente conectado');
                        
                        // Enviar datos iniciales al cliente
                        r.db(dbName).table(tableName).run(conn, (err, cursor) => {
                            if (err) throw err;
                            cursor.toArray((err, result) => {
                                if (err) throw err;
                                socket.emit('initial_data', result);
                            });
                        });

                        // Escuchar cambios en la tabla y enviar a todos los clientes conectados
                        r.db(dbName).table(tableName).changes().run(conn, (err, cursor) => {
                            if (err) throw err;
                            cursor.each((err, change) => {
                                if (err) throw err;
                                io.emit('data_update', change);
                            });
                        });

                        socket.on('disconnect', () => {
                            console.log('Cliente desconectado');
                        });
                    });
                });
        });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});
