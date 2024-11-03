import os

import joblib
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from modules.logger_manager import get_logger

# set the path of the root dir
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_model(cfg):
    """Carga el modelo preentrenado basado en la configuración de Hydra.

    Args:
        cfg (DictConfig): Configuración cargada por Hydra.

    Returns:
        joblib(pkl): Modelo cargado.
    """
    logger = get_logger()

    model_path = cfg.models.model_path
    abs_model_path = os.path.join(root_dir, model_path)

    logger.info(f"Cargando el modelo desde: {model_path}")

    return joblib.load(abs_model_path)


def train_model(df, cfg):
    """Entrena o reentrena el modelo basado en la configuración proporcionada por Hydra.

    Args:
        df (DataFrame): Dataframe con nuevos datos de entrenamiento.
        cfg (DictConfig): Configuración cargada por Hydra que define las columnas, el modelo y otros parámetros.

    Returns:
        str: Mensaje de éxito con las métricas obtenidas.
    """
    logger.info("Iniciando el entrenamiento del modelo...")
    # load model
    modelo = load_model(cfg.train.model_path)

    # load features and target column
    X = df[cfg.train.features]
    y = df[cfg.train.target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=cfg.train.test_size, random_state=cfg.train.random_state
    )

    # train the model
    logger.info("Entrenando el modelo...")
    modelo.fit(X_train, y_train)

    # evaluate the model
    logger.info("Evaluando el modelo...")
    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # log the model
    logger.info("Registrando el modelo en MLflow...")
    with mlflow.start_run():
        mlflow.log_param("test_size", cfg.train.test_size)
        mlflow.log_param("random_state", cfg.train.random_state)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(modelo, "modelo_reentrenado")

    logger.info("Modelo reentrenado guardado en MLflow")
    save_model(modelo, cfg.models.retrained_model_path)

    return f"Modelo reentrenado con accuracy de: {accuracy}"


def save_model(model, path):
    """Guarda el modelo entrenado en la ruta especificada.

    Args:
        model (joblib): Modelo entrenado que se va a guardar.
        path (str): Ruta donde se guardará el archivo del modelo.
    """
    # get absolute path
    abs_model_path = os.path.abspath(path)

    # create directory if it doesn't exist
    os.makedirs(os.path.dirname(abs_model_path), exist_ok=True)

    # save the model
    logger.info(f"Guardando el modelo en: {abs_model_path}")
    joblib.dump(model, abs_model_path)
