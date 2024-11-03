import os

import hydra
from dotenv import load_dotenv
from hydra import compose, initialize
from omegaconf import DictConfig

# load environment variables
load_dotenv()

def init_config(config_name: str = "config") -> DictConfig:
    """
    Inicializa Hydra y carga la configuración, utilizando una variable de entorno para el directorio de configuración.

    Args:
        config_name (str): Nombre del archivo de configuración (sin extensión).

    Returns:
        DictConfig: Configuración cargada por Hydra.
    """
    config_path = os.getenv('CONFIG_PATH')

    initialize(config_path=config_path, version_base=None)
    cfg = compose(config_name=config_name)
    return cfg
