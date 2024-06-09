import yaml
import os

def Config() -> dict:

    # Obtener la ruta absoluta del directorio actual del script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta absoluta del archivo config.yml
    config_path = os.path.join(current_dir, '../../../config.yml')

    with open(config_path, 'r') as file:
        try:
            return yaml.safe_load(file)
            
        except yaml.YAMLError as e:
            print(e)

#print(Config()["host"])


'''
net = {
    'host': 'localhost',

    'api': {
        'protocol': 'https',
        'port': '8000'
    },
    'apiws': {
        'protocol': 'ws',
        'port': '8100'
    },
    'cryptoapi': {
        'protocol': 'https',
        'port': '8200'
    },
    'statusapi': {
        'protocol': 'https',
        'port': '8300'
    },
}'''