const fs = require('fs');
const path = require('path');

const rootFolder = '/Users/yeray/Documents/GIT/GIT/BAckend/microservices/app/APIWS/routes'; // Cambia esto a la ruta de tu carpeta principal

function processFolder(folderPath, relativePath = '') {
    console.log(`Procesando carpeta: ${folderPath}`);
    const files = fs.readdirSync(folderPath);
    files.forEach(file => {
        const filePath = path.join(folderPath, file);
        const stats = fs.statSync(filePath);
        if (stats.isDirectory()) {
            const newRelativePath = path.join(relativePath, file);
            processFolder(filePath, newRelativePath);
        } else if (file === 'index.js') {
            modifyIndexFile(filePath, relativePath);
        }
    });
}

function modifyIndexFile(filePath, relativePath) {
    console.log(`Modificando archivo: ${filePath}`);
    try {
        const lines = fs.readFileSync(filePath, 'utf8').split('\n');
        if (lines.length > 0) {
            // Buscar la línea donde se declara la variable "_"
            //const index = lines.findIndex(line => line.trim().startsWith('const _ ='));
            
            // Reemplazar la línea con la nueva ruta relativa
            lines[0] = `const _ = "/${relativePath}";`;
            const newContent = lines.join('\n');
            fs.writeFileSync(filePath, newContent, 'utf8');
            console.log(`Modificado ${filePath}`);
            
        }
    } catch (error) {
        console.error(`Error al modificar archivo ${filePath}:`, error);
    }
}

processFolder(rootFolder);
