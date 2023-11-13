#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Uso: $0 <file_csv>"
  exit 1
fi

file_csv="$1"

awk -F ',' 'NR == 2 {print "aws configure set aws_access_key_id", $1} NR == 2 {print "aws configure set aws_secret_access_key", $2}' "$file_csv" | sh
