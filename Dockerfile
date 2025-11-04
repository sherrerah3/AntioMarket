# Imagen base liviana de Python
FROM python:3.11-slim

# Evita archivos pyc y buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del proyecto
COPY . .

# Ejecuta collectstatic (para los archivos estáticos)
RUN python mercado_campesino/manage.py collectstatic --noinput || true

# Exponer el puerto interno donde corre Django
EXPOSE 8000

# Comando para ejecutar Django con Gunicorn (modo producción)
CMD ["gunicorn", "mercado_campesino.wsgi:application", "--bind", "0.0.0.0:8000"]
