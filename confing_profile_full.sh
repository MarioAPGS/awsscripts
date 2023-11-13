#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Uso: $0 <file_csv>"
  exit 1
fi

file_csv="$1"

# Leer la segunda línea del archivo CSV y configurar las claves de acceso
aws_access_key_id=$(awk -F ',' 'NR == 2 {print $1}' "$file_csv")
aws_secret_access_key=$(awk -F ',' 'NR == 2 {print $2}' "$file_csv")
aws configure set aws_access_key_id "$aws_access_key_id"
aws configure set aws_secret_access_key "$aws_secret_access_key"

# Configurar la región en eu-west-2
aws configure set default.region eu-west-2

echo "Configuración completada."
