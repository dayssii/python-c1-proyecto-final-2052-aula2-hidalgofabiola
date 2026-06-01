# Imagen base de Python 3.11 versión ligera
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero solo el requirements.txt para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de código
COPY . .

# Puerto que expone este servicio
EXPOSE 5000

# Comando para arrancar el servidor
CMD ["python", "app.py"]