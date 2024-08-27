# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos
COPY ./requirements.txt /app/

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto en el contenedor
COPY . /app/

# Recolección de archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para correr la aplicación con Gunicorn
CMD ["gunicorn", "cannaTech.wsgi:application", "--bind", "0.0.0.0:8000"]

