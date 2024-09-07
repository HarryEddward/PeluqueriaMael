

'use strict';

const EventEmitter = require('events');
const r = require('rethinkdb');
const database = require('./database');

/**
 * Clase para manejar la escucha de cambios asincrónicos en una tabla de RethinkDB.
 * @extends EventEmitter
 */
class AsyncTableBookingSheet extends EventEmitter {

    /**
     * Crea una instancia de AsyncTable.
     * @param {string} tableName El nombre de la tabla a escuchar.
     */
    constructor(tableName, dateISOFormat) {
        super();
        /**
         * El nombre de la tabla.
         * @type {string}
         * @type {string}
         */
        this.tableName = tableName;
        this.dateISOFormat = dateISOFormat;
    }

    /**
     * Inicia la escucha de cambios en la tabla especificada.
     * @returns {Promise<void>} Una promesa que se resuelve cuando se inicia la escucha de cambios.
     */
    async start() {
        try {
            const connection = database.getConnection();
            /**
             * Cursor que representa la secuencia de cambios en la tabla.
             * @type {require('rethinkdb').Cursor}
             */

            const cursorData = await r.table(this.tableName).filter({ "fecha": String(this.dateISOFormat) }).limit(1).run(connection);
            const cursorChanges = await r.table(this.tableName).changes().run(connection);
            
            console.log(` await r.table(${this.tableName}).filter({ "fecha": String(${this.dateISOFormat}) }).limit(1).run(${connection});`);

            this.emit('change', "cursorData.next()");
            
            cursorChanges.each((err, row) => {
                if (err) throw err;
                /**
                 * Evento que se emite cuando hay un cambio en la tabla.
                 * @event AsyncTable#change
                 * @type {Object}
                 */
                this.emit('change', row);
            });
        } catch (err) {
            console.error('Error al iniciar feed de la tabla:', err);
        }
    }
}

module.exports = AsyncTableBookingSheet;
