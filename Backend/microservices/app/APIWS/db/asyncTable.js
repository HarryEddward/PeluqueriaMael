'use strict';

const EventEmitter = require('events');
const r = require('rethinkdb');
const database = require('./database');

class AsyncTable extends EventEmitter {

    constructor(tableName) {
        super();
        this.tableName = tableName
    }

    async start() {

        try {

            const connection = database.getConnection();
            const cursor = await r.table(this.tableName).changes().run(connection);
            cursor.each((err, row) => {
                if (err) throw err;
                this.emit('change', row);
            })

        } catch (err) {
            console.error('Error al iniciar feed de la tabla:', err);
        }
    }
}

module.exports = AsyncTable;