// errorHandler.js

const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Algo salió mal en el servidor');

};

module.exports = errorHandler;