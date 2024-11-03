import json
import os


def load_dict(imputacion_path):
    """Carga el diccionario de imputaciones de los datos.

    Args:
        imputacion_path (_type_): Path del archivo de imputaciones.

    Raises:
        FileNotFoundError: Error si no se encuentra el archivo de imputaciones.

    Returns:
        _type_: Diccionario de imputaciones
    """
    if not os.path.exists(imputacion_path):
        raise FileNotFoundError(f"No se encontró el archivo de imputación en la ruta: {imputacion_path}")

    with open(imputacion_path, 'r') as file:
        imputation_dict = json.load(file)

    return imputation_dict
