# Imagen base ligera de Python
FROM python:3.11-slim

# Configuración básica
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer puerto (documentación)
EXPOSE 8080

# Comando de arranque
CMD ["python", "main.py"]
