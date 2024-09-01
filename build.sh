#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Asegúrate de que la carpeta staticfiles existe y tiene los permisos correctos
mkdir -p staticfiles
chmod -R 755 staticfiles