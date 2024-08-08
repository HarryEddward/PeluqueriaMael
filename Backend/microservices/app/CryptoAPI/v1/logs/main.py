# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os
from playsound import playsound

def play_error_sound():
    # Ruta al archivo de sonido que quieres reproducir
    error_sound_path = 'error_sound.mp3'
    if os.path.exists(error_sound_path):
        playsound(error_sound_path)
    else:
        print("Archivo de sonido no encontrado!")

class SoundHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        if record.levelno >= logging.ERROR:
            play_error_sound()

def setup_logging():
    # Directorio para almacenar los archivos de log
    log_directory = 'logs'
    os.makedirs(log_directory, exist_ok=True)

    # Configuración del handler para el archivo de logs
    file_handler = RotatingFileHandler(
        os.path.join(log_directory, 'app.log'), 
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Configuración del handler para la salida en consola
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Configuración del handler para reproducir sonido en caso de errores críticos
    sound_handler = SoundHandler()
    sound_handler.setLevel(logging.ERROR)
    sound_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    sound_handler.setFormatter(sound_formatter)

    # Obtener el logger root
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Establecer el nivel de logging global

    # Añadir handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(sound_handler)
