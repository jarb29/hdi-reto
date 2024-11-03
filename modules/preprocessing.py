import os

import dill
import numpy as np
import pandas as pd

from modules.logger_manager import get_logger
from utils import load_dict, validate_types

from .imputation import null_imputation

# root dir
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pipeline_run(df, pipeline_file):
    """Ejecuta un pipeline de transformación sobre los datos en un contexto de ejecución donde np está disponible.

    Args:
        df (DataFrame): DataFrame con datos a transformar.
        pipeline_file (str): Ruta al archivo del pipeline.

    Returns:
        DataFrame: DataFrame transformado.
    """
    abs_pipeline_file = os.path.join(root_dir, pipeline_file)

    logger = get_logger()

    # Cargar el pipeline
    logger.info(f'Cargando el pipeline: {abs_pipeline_file}')
    with open(abs_pipeline_file, 'rb') as file:
        pipeline = dill.load(file)

    if hasattr(pipeline, '__globals__'):
        pipeline.__globals__['np'] = np
        pipeline.__globals__['pd'] = pd

    # Ejecutar el pipeline directamente
    try:
        # logger.info("Ejecutando el pipeline...")
        result = pipeline(df)
    except NameError as e:
        logger.error(f'Error al ejecutar el pipeline: {e}')
        raise RuntimeError(f'Error al ejecutar el pipeline: {e}')

    return result


def full_pipeline(df, cfg):
    """Ejecuta el pipeline basado en pasos de transformación sobre los datos.

    Args:
        df (DataFrame): Dataframe con datos a transformar.
        cfg (DictConfig): Configuración de Hydra que contiene las rutas de los pipelines e imputaciones.

    Returns:
        DataFrame: Dataframe con datos transformados por el pipeline completo.
    """
    logger = get_logger()

    # pipeline steps
    for step in cfg.pipeline.steps:
        logger.info(f'Ejecutando {step.name} con pipeline: {step.pipeline}')
        df = pipeline_run(df, step.pipeline)

    # df to json
    # logger.info("Transformando a JSON...")
    # df_json = df.to_json(orient="records")
    # print(f"Pipeline completo: {df_json}")

    # load imputation dict
    logger.info('Cargando el diccionario de imputaciones...')
    imputation_path = cfg.pipeline.imputacion_path
    imputation_dict = load_dict(imputation_path)

    # null imputation
    logger.info('Imputando valores nulos...')
    df = null_imputation(df, imputation_dict)

    # print("Transformando a JSON...")
    # df_json = df.to_json(orient="records")
    # print(f"Datos post imputación: {df_json}")

    # validate columns and types
    logger.info('Validando columnas y tipos...')
    validate_types(df)

    return df
