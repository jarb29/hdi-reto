# Desafio HDI

Este repositorio contiene el código de la solución del desafío de HDI.

## To-do

- [X] Verificar el formato de las columnas
- [X] Implementar la imputación de valores nulos
- [X] Aplicar el diccionario de imputación
- [X] Construir el pipeline de preprocesamiento
- [X] Implementar la condición especial para pólizas tipo 4
- [X] Asegurar que las features coincidan con el formato de entrenamiento
- [X] Pasar los datos preprocesados al modelo predictivo
- [X] Obtener la predicción del tiempo en semanas
- [X] Validar los resultados para los diferentes tipos de pólizas
- [X] Integrar pruebas de estrés para la API
- [X] Realizar pruebas con casos de entrada
- [X] Documentar el proceso
- [X] Implementar logging para manejo de errores

## Instalación

Sigue estos pasos para instalar y ejecutar la aplicación en tu entorno local:

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/jarb29/desafio-hdi.git
   ```

2. Navega al directorio del proyecto:
   ```bash
   cd desafio-hdi
   ```

3. Crea un entorno virtual:
   ```bash
   python3 -m venv env
   source env/bin/activate  # En Windows usa `.\env\Scripts\activate`
   ```

4. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta el script principal para iniciar la aplicación:
   ```bash
   uvicorn api.main:app --reload
   ```

## Uso

La aplicación se ejecutará en `http://localhost:8000`. Puedes acceder a la documentación de la API en `http://localhost:8000/docs`.

Para probar la API, puedes utilizar el archivo `data/claims_dataset.csv` como entrada.

## Documentación

Puedes acceder a la documentación completa del proyecto [aquí](https://jarb29.github.io/hdi-reto/).

## Dockerfile

El `Dockerfile` se utiliza para crear un contenedor Docker para tu aplicación FastAPI. A continuación, se muestra un desglose de cada comando:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

# upgrade and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements/requirements.txt

ENV HOST="0.0.0.0" \
    PORT="8000" \
    CONFIG_PATH="../config"

EXPOSE ${PORT}

# run the app
CMD ["uvicorn", "api.main:app", "--host", "${HOST}", "--port", "${PORT}"]
```

### Explicación

- **Imagen Base**: Usa la variante slim de Python 3.11.
- **Directorio de Trabajo**: Establece el directorio de trabajo dentro del contenedor en `/app`.
- **Copiar Archivos**: Copia todos los archivos del directorio actual a `/app`.
- **Instalar Dependencias**: Actualiza las listas de paquetes e instala las dependencias necesarias para construir paquetes de Python.
- **Dependencias de Python**: Instala las dependencias de Python desde `requirements.txt`.
- **Variables de Entorno**: Establece variables de entorno para el host, puerto y ruta de configuración.
- **Exponer Puerto**: Expone el puerto 8000 para la aplicación.
- **Comando de Ejecución**: Ejecuta el servidor Uvicorn, cargando la aplicación FastAPI desde `api.main:app`.

## docker-compose.yml

El archivo `docker-compose.yml` se utiliza para gestionar aplicaciones Docker de múltiples contenedores.

```yaml
services:
  app:
    container_name: HDI-Challenge
    image: jarb29/hdi-challenge:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      HOST: "0.0.0.0"
      PORT: "8000"
    command: >
      uvicorn api.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}
```

### Explicación

- **Definición del Servicio**: Define un servicio llamado `app`.
- **Nombre del Contenedor**: Nombra el contenedor `HDI-Challenge`.
- **Imagen**: Especifica la imagen Docker a utilizar.
- **Contexto de Construcción**: Define el contexto de construcción y la ubicación del Dockerfile.
- **Puertos**: Mapea el puerto `8000` en el host al puerto `8000` en el contenedor.
- **Variables de Entorno**: Establece variables de entorno para la aplicación.
- **Comando**: Especifica el comando para ejecutar el servidor Uvicorn.

## Makefile

El `Makefile` proporciona accesos directos convenientes para construir, desplegar y detener los contenedores Docker.

```makefile
build: ## Build the Docker image
	docker-compose up --build

deploy: build ## Deploy the app to the server
	docker-compose up -d

deploy-stop: ## Stop the app from the server
	docker-compose down
```

### Explicación

- **build**:
    - **Comando**: `docker-compose up --build`
    - **Descripción**: Construye la imagen Docker y arranca el contenedor.

- **deploy**:
    - **Comando**: `docker-compose up -d`
    - **Descripción**: Ejecuta primero el objetivo `build`, luego despliega la aplicación en modo desconectado.

- **deploy-stop**:
    - **Comando**: `docker-compose down`
    - **Descripción**: Detiene y elimina contenedores, redes y volúmenes asociados con el proyecto Docker Compose.

## Uso de Docker

### Construir la Imagen Docker

Ejecuta el siguiente comando para construir la imagen Docker:

```bash
make build
```

### Desplegar la Aplicación

Ejecuta el siguiente comando para desplegar la aplicación:

```bash
make deploy
```

### Detener la Aplicación

Ejecuta el siguiente comando para detener la aplicación:

```bash
make deploy-stop
```

## Endpoints

### Predicción
- **`POST /api/v1/predict`**: Genera una predicción para los registros recibidos.

  **Body**:
  ```json
  {
    "claims": [
      {
        "claim_id": "1",
        "policy_type": "4",
        "incident_date": "2023-01-01",
        "claim_amount": 5000.00,
        ...
      },
      ...
    ]
  }
  ```
  **Respuesta**:
  ```json
  {
    "prediction": [
      {
        "claim_id": "1",
        "predicted_weeks": 6
      },
      ...
    ]
  }
  ```

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarme a través de [mi perfil de LinkedIn](https://www.linkedin.com/in/jarb29/).