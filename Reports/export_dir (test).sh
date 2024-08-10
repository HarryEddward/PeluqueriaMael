#!/bin/bash

# Nombre del archivo de salida
output_file="informacion_archivos.txt"

# Limpiar el archivo de salida si ya existe
> "$output_file"

# Directorio a recorrer (puedes cambiarlo si es necesario)
directorio="../Backend/microservices/app/CryptoAPI/v1"

# Función para comprobar si un archivo es de texto
es_texto() {
    local archivo="$1"
    # Comprobar si el archivo es de texto usando el comando 'file'
    if file "$archivo" | grep -q 'text'; then
        return 0  # Es un archivo de texto
    else
        return 1  # Es un archivo binario
    fi
}

# Función para recorrer los archivos
recorrer_archivos() {
    local dir="$1"
    # Recorrer todos los archivos en el directorio
    for archivo in "$dir"/*; do
        if [ -d "$archivo" ]; then
            # Si es un directorio, llamar recursivamente a la función
            recorrer_archivos "$archivo"
        elif [ -f "$archivo" ]; then
            # Si es un archivo, verificar si es de texto o binario
            if es_texto "$archivo"; then
                # Si es de texto, leer su contenido y registrar la información
                echo "Archivo: $archivo" >> "$output_file"
                cat "$archivo" >> "$output_file"
                echo -e "\n\n" >> "$output_file"
            else
                # Si es binario, solo registrar la ruta del archivo
                echo "Archivo binario: $archivo" >> "$output_file"
                echo -e "\n\n" >> "$output_file"
            fi
        fi
    done
}

# Llamar a la función con el directorio inicial
recorrer_archivos "$directorio"

echo "Información de los archivos registrada en $output_file"
