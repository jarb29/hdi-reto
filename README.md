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
- [ ] Documentar el proceso
- [X] Implementar logging para manejo de errores

## Installation

1. Clona este repositorio en tu máquina local
2. Crea un entorno virtual
3. Instala las dependencias de Python

```python
pip install -r requirements.txt
```

4. Ejecuta el script principal para iniciar la aplicación

```python
uvicorn api.main:app
```

## Usage

La aplicación se ejecutará en `http://localhost:8000`. Puedes acceder a la documentación de la API en `http://localhost:8000/docs`.

Para probar la API, puedes utilizar el archivo `data/claims_dataset.csv` como entrada.

## Documentation

Puedes acceder a la documentación del proyecto [aquí](https://jarb29.github.io/desafio-hdi/).

## Endpoints

- `POST /api/v1/predict`: Genera una predicción para los registros recibidos.
- `POST /api/v1/train`: Entrena el modelo, si es requerido.

## License

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

## Contact

Si tienes alguna pregunta o sugerencia, no dudes en contactarme a través de [mi perfil de LinkedIn](https://www.linkedin.com/in/jarb29/).
# hdi-reto
