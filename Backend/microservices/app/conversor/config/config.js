const fs = require('fs');
const yaml = require('js-yaml');
const path = require('path');


const configPath = path.join(__dirname, '../../config.yml');


const Config = () => {
    try {

        const fileContent = fs.readFileSync(configPath, 'utf8');
        return yaml.load(fileContent);

    } catch (e) {
        console.error(e);
    }
};

//console.log(Config());