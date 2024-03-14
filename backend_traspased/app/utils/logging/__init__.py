import logging
from fastapi import Request



def setup_log():

    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )



#Define la esquema request de astapi
#Default: level -> info;

def log_request(request: Request, level='info'):

    logger = logging.getLogger(__name__)
    
    match level:
        case 'info':
            logger.info(f"Request received: {request.method} {request.url.path}")
        case 'warning':
            logger.warning(f"Warning: {request.method} {request.url.path}")
        case 'error':
            logger.error(f"Error: {request.method} {request.url.path}")
        case _:
            raise ValueError('Tipo de parametro de logging incorrecto')