// database.js

'use strict';

var colors = require('colors');
const r = require('rethinkdb');
const { Config } = require('../../../../conversor/config/config');

const config = Config();
const rethinkdb = config.db.persistant.rethinkdb;
const port = rethinkdb.port.client;
const host = config.host;
const db = rethinkdb.db;

/**
 * Clase para manejar la conexión a la base de datos RethinkDB.
 * 
 */
class Database {


    /**
     * Crea una instancia de Database
     * 
     * @example
     * database.connection().then()
     */
    constructor() {
        /**
         * La conexión actual a la base de datos
         * @type {require('rethinkdb').Connection | null}
         */
        this.connection = null;
    }

    /**
     * Conexta a la base de datos RethinkDB
     * @returns {Promise<r.Connection>} Una promesa que se devuelve cuando se establece la conexión a la DB.
     */
    async connect() {

        try {
            console.log(`${rethinkdb}`)

            this.connection = await r.connect({
                host: host,
                port: port,
                db: db
            });
            console.log('-> RethinkDB:'.bgGreen + ' ' + 'Conectado a RethinkDB'.underline);
            console.log(`-> RethinkDB:`.bgGreen + ` ` + `PORT:`.green+`${port}, `+`HOST:`.green + `${host}, `+`DB:`.green+`${db}`);


        } catch (err) {
            console.error(`-> RethinkDB:`.bgGreen + ' ' + `Error al conectarse: ${err}`.bgRed);
        }
    }

    /**
     * 
     * @returns Instancia de la clase Database, lista para ser exportada.
     * @type {Database}
     */
    getConnection() {
        return this.connection;
    }
}


module.exports = new Database();