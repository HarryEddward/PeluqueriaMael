import logging
import logging.config
import os
from logging.handlers import RotatingFileHandler

# Crea la carpeta de logs si no existe
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_directory, 'info.log'),
            'formatter': 'detailed',
            'level': 'INFO',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_directory, 'error.log'),
            'formatter': 'detailed',
            'level': 'ERROR',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
        },
        'user_creation_handler': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_directory, 'user_creation.log'),
            'formatter': 'detailed',
            'level': 'INFO',
        },
    },
    'loggers': {
        'peluqueria_mael': {
            'handlers': [
                'console',
                'info_file_handler',
                'error_file_handler'
            ],
            'level': 'INFO',
            'propagate': False,
        },
        'user_registered': {
            'handlers': ['user_creation_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'info_file_handler', 'error_file_handler'],
        'level': 'INFO',
    },
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger('peluqueria_mael')
user_registered_logger = logging.getLogger('user_registered')
