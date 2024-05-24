// database.js

'use strict';

const r = require('rethinkdb');

class Database {

    constructor() {
        this.connection = null;
    }

    async connect() {

        try {
            this.connection = await r.connect({
                host: 'localhost',
                port: 28015,
                db: 'test'
            });
            console.log('Conectado a RethinkDB');

        } catch (err) {
            console.error('Error al conectar a RethinkDB:', err)
        }
    }

    getConnection() {
        return this.connection;
    }
}


module.exports = new Database();