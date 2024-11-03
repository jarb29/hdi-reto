import csv
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from omegaconf import DictConfig

logger = None

def setup_logger(cfg: DictConfig) -> logging.Logger:
    """Configura el logger de la aplicación.

    Args:
        cfg (DictConfig): Configuración de Hydra que contiene la configuración de logger.

    Returns:
        logging.Logger: Logger configurado.
    """
    # Configuración del archivo de log desde config.yaml
    log_path = cfg.logger.log_file
    log_level = cfg.logger.level
    max_bytes = cfg.logger.max_bytes
    backup_count = cfg.logger.backup_count

    global logger

    if logger is None:
        # Crear el logger
        logger = logging.getLogger("process_logger")
        logger.setLevel(log_level)

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Configurar el manejador de rotación de archivo
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )

        # Configurar el manejador de consola (terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Formato del logger
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Añadir ambos manejadores al logger
        if not logger.hasHandlers():
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger


def log_to_csv(data: dict, cfg: DictConfig):
    """Registra los datos de consulta en un archivo CSV para monitoreo.

    Args:
        data (dict): Información de entrada y salida de la consulta.
        cfg (DictConfig): Configuración de Hydra para la ruta del archivo CSV.
    """
    csv_path = cfg.logger.csv_file
    fieldnames = [
        "timestamp", "claim_id", "marca_vehiculo", "antiguedad_vehiculo",
        "tipo_poliza", "taller", "partes_a_reparar", "partes_a_reemplazar",
        "prediction", "execution_time"
    ]

    # Crear el archivo si no existe y escribir la cabecera
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def get_logger():
    global logger
    if logger is None:
        raise Exception("Logger is not initialized. Call setup_logger() first.")
    return logger
