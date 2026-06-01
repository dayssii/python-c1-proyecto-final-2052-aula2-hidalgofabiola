# Imagen base de Python 3.11 versión ligera
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero solo el requeriments.txt para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de código
COPY . .

# Puerto que expone el servicio
EXPOSE 5001

# Comando para arrancar el servidor
CMD ["python", "app.py"]