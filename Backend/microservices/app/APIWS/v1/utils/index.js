// Función utilitaria replaceAt
function replaceAt(str, index, replacement) {
    return str.substring(0, index) + replacement + str.substring(index + replacement.length);
}

// Exporta la función
module.exports = {
    replaceAt
};