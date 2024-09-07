'use strict';


function isoJsToIsoPy(dateIsoFormatJs) {

    const str = dateIsoFormatJs.slice(0, 22);

    // Encuentra el índice del último punto
    const lastDotIndex = str.lastIndexOf('.');
    if (lastDotIndex === -1) {
        // Si no hay puntos en la cadena, retorna la cadena original
        return str;
    }

    // Encuentra el índice del penúltimo punto
    const penultimateDotIndex = str.lastIndexOf('.', lastDotIndex - 1);
    if (penultimateDotIndex === -1) {
        // Si no hay un penúltimo punto, retorna la cadena original
        return str;
    }

    // Reemplaza el penúltimo punto por `:`
    return str.substring(0, penultimateDotIndex) + ':' + str.substring(penultimateDotIndex + 1);
}


// Función para validar la fecha en formato ISO 8601
const isValidISODate = (dateString) => {
    const isoRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
    return isoRegex.test(dateString) && !isNaN(Date.parse(dateString));
};

module.exports = { isValidISODate, isoJsToIsoPy };