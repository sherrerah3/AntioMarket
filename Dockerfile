# Imagen base de Python
FROM python:3.11-slim

# Evita que Python cree archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto (incluye db.sqlite3 y manage.py)
COPY . .

# Ejecuta collectstatic (para archivos estáticos de Django)
RUN python mercado_campesino/manage.py collectstatic --noinput || true

# Expone el puerto que usará Django
EXPOSE 8000

# Comando para ejecutar Django usando Gunicorn
CMD ["gunicorn", "mercado_campesino.wsgi:application", "--bind", "0.0.0.0:8000"]
