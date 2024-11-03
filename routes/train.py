import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from sklearn.model_selection import train_test_split
from starlette.concurrency import run_in_threadpool

from modules import train_model

router = APIRouter()

@router.post("/api/v1/train/")
async def train(file: UploadFile = File(...)):
    try:
        # get logger from api state
        logger = request.app.state.logger
        logger.info("Solicitud recibida en /api/v1/train/")

        df = await run_in_threadpool(pd.read_csv, file.file)
        logger.info(f"Datos recibidos: {df}")

        logger.info("Iniciando el entrenamiento del modelo...")
        resultado = await run_in_threadpool(train_model, df)

        return {
            "message": "Modelo entrenado con éxito",
            "details": resultado
        }
    except Exception as e:
        logger.error(f"Error en el entrenamiento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en el entrenamiento: {str(e)}")
