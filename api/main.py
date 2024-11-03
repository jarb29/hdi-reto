import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
import yaml  # Use PyYAML to parse YAML content

from modules import init_config, setup_logger, get_logger
from routes import predict, train

# Inicialize FastAPI
app = FastAPI()

def custom_openapi():
    # Assuming swagger.yaml is in the /app/docs/ directory
    if app.openapi_schema:
        return app.openapi_schema
    with open("/app/docs/swagger.yaml", "r") as file:
        swagger_content = yaml.safe_load(file)  # Use yaml.safe_load to load the YAML file
    app.openapi_schema = swagger_content
    return swagger_content  # Directly return the dictionary



app.openapi = custom_openapi


# Inicialize configuration
cfg = init_config()
app.state.cfg = cfg

# Inicialize logger
setup_logger(cfg)
app.state.logger = get_logger()
app.state.logger.info("Logger inicializado en modo global.")

# Add routes
app.include_router(predict)
app.include_router(train)

@app.get("/")
def root():
    return {"message": "Bienvenido al API de predicción de siniestros de HDI"}

if __name__ == "__main__":
    imputacion_path = cfg.pipeline.imputacion_path
    print(f"Usando el archivo de imputación en la ruta: {imputacion_path}")

    # start FastAPI
    uvicorn.run(app, host=cfg.api.host, port=cfg.api.port)
