// errorHandler.js

/**
 * Maneja los errores inesperdados del mismo servidor
 * @param {any} err - Error produccido
 * @param {any} req - La información enviada por el usuario
 * @param {any} res - La respuesta que devolveremos
 * @param {any} next - Función para acabar con el middleware en cualquier punto del código
 */
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Algo salió mal en el servidor');

};

module.exports = errorHandler;