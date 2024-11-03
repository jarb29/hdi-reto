import numpy as np
import pandas as pd
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from models import Claim
from modules import full_pipeline, load_model, log_to_csv

router = APIRouter()

@router.post("/api/v1/predict/", include_in_schema=True)
async def predict_claim(claim: Claim, request: Request):
    cfg = request.app.state.cfg
    logger = request.app.state.logger
    start_time = time.time()

    logger.info("Solicitud recibida en /api/v1/predict/")

    # convert claim to dataframe
    data = pd.DataFrame([claim.dict()])

    # load model asynchronously
    try:
        logger.info("Cargando el modelo...")
        modelo = await run_in_threadpool(load_model, cfg)
    except Exception as e:
        logger.error(f"Error al cargar el modelo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al cargar el modelo: {str(e)}")

    # full pipeline asynchronously
    try:
        logger.info("Ejecutando el pipeline de transformación...")
        df_procesado = await run_in_threadpool(full_pipeline, data, cfg)
    except Exception as e:
        logger.error(f"Error en el pipeline de transformación: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en el pipeline de transformación: {str(e)}")

    # predict asynchronously
    try:
        logger.info("Realizando la predicción...")
        if claim.tipo_poliza == 4:
            logger.info("Tipo de póliza es 4, devolviendo predicción -1")
            prediccion = [-1]
        else:
            logger.info("Tipo de póliza no es 4, realizando predicción...")
            model_features = modelo.feature_names_in_
            df_for_prediction = df_procesado[model_features]
            prediccion = await run_in_threadpool(modelo.predict, df_for_prediction)
            logger.info(f"Predicción: {prediccion[0]}")
    except Exception as e:
        logger.error(f"Error en la predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")

    end_time = time.time()
    execution_time = round(end_time - start_time, 4)

    # log to csv
    log_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "claim_id": claim.claim_id,
            "marca_vehiculo": claim.marca_vehiculo,
            "antiguedad_vehiculo": claim.antiguedad_vehiculo,
            "tipo_poliza": claim.tipo_poliza,
            "taller": claim.taller,
            "partes_a_reparar": claim.partes_a_reparar,
            "partes_a_reemplazar": claim.partes_a_reemplazar,
            "prediction": prediccion[0],
            "execution_time": execution_time
        }
    log_to_csv(log_data, cfg)

    logger.info(f"Predicción realizada para claim_id {claim.claim_id} en {execution_time}s")

    return {"prediccion": prediccion[0]}
