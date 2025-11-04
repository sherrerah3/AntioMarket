# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar archivos .pyc y salida en buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear y usar el directorio de trabajo
WORKDIR /app/mercado_campesino

# Copiar los requerimientos al contenedor
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar todo el código del proyecto
COPY . /app/

# Ejecutar collectstatic (para archivos estáticos)
RUN python manage.py collectstatic --noinput || true

# Exponer el puerto donde correrá Django
EXPOSE 8000

# Iniciar el servidor con Gunicorn
CMD ["gunicorn", "mercado_campesino.wsgi:application", "--bind", "0.0.0.0:8000"]
