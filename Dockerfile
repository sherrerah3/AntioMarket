# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar archivos .pyc y buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Ejecutar collectstatic (para archivos estáticos de Django)
RUN python mercado_campesino/manage.py collectstatic --noinput || true

# Exponer el puerto interno donde corre Django
EXPOSE 8000

# Comando para iniciar el servidor con Gunicorn (modo producción)
CMD ["gunicorn", "mercado_campesino.wsgi:application", "--bind", "0.0.0.0:8000"]
