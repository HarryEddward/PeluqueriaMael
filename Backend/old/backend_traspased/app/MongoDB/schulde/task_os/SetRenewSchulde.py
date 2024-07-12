import os
import platform
import schedule
import time
import subprocess
from datetime import datetime, timedelta

def configurar_tarea_programada():
    # Ruta al script que deseas ejecutar
    ruta_script = os.path.abspath(r"C:\Users\micro\Documents\PeluqueriaMael\backend\app\RenewDays.py")

    # Ruta al ejecutable de Python
    ruta_python = os.path.abspath(r"C:\Users\micro\Documents\PeluqueriaMael\backend\.venv\Scripts\python.exe")

    # Contenido del archivo por lotes
    contenido_bat = fr"""@echo off
    cd "{os.path.dirname(ruta_script)}"
    "{ruta_python}" "{ruta_script}"
    """

    # Ruta al archivo por lotes
    ruta_bat = os.path.abspath(r"C:\Users\micro\Documents\PeluqueriaMael\backend\app\utils\schulde.bat")

    # Guarda el contenido del archivo por lotes
    with open(ruta_bat, 'w') as archivo_bat:
        archivo_bat.write(contenido_bat)

    if platform.system() == "Windows":
        # Comando para crear la tarea programada en Windows
        comando_creacion_tarea = [
            "schtasks", "/create", "/tn", "RenewDatabaseMongoDB", "/tr", ruta_bat, "/sc", "daily", "/st", "00:01"
        ]
    else:
        # Comando para crear la tarea programada en Linux
        comando_creacion_tarea = [
             "echo", f"1 0 * * * {ruta_script} >> /var/log/syslog 2>&1 | crontab -"
        ]

    # Ejecuta el comando para crear la tarea programada
    subprocess.run(comando_creacion_tarea, shell=True)

    print("Configuración completa. Tarea programada creada.")

# Configura la tarea programada al iniciar el script
configurar_tarea_programada()

# Define la programación de la tarea (puedes ajustar esto según tus necesidades)
schedule.every().day.at("00:01").do(configurar_tarea_programada)

while True:
    # Ejecuta las tareas programadas
    schedule.run_pending()
    time.sleep(1)
