import pytest
import pandas as pd
from fastapi.testclient import TestClient
from models import Claim
from modules import full_pipeline, load_model, config_manager
from api.main import app

# Crear un cliente de pruebas para la API
client = TestClient(app)

# Fixture para inicializar y limpiar configuración de Hydra en cada test
@pytest.fixture(scope="module")
def hydra_cfg():
    from hydra.core.global_hydra import GlobalHydra
    if GlobalHydra.instance().is_initialized():
        GlobalHydra.instance().clear()
    config = config_manager.init_config()
    return config  # Asegúrate de devolver el objeto DictConfig

def test_full_pipeline(hydra_cfg):
    # Datos de ejemplo para el pipeline
    data = pd.DataFrame({
        "claim_id": [1],
        "marca_vehiculo": ["ford"],
        "antiguedad_vehiculo": [5],
        "tipo_poliza": [2],
        "taller": [1],
        "partes_a_reparar": [3],
        "partes_a_reemplazar": [1]
    })

    try:
        result = full_pipeline(data, hydra_cfg)
        assert not result.isnull().values.any(), "El pipeline debe imputar todos los valores nulos"
        assert "log_total_piezas" in result.columns, "Falta la columna 'log_total_piezas' en el resultado del pipeline"
    except Exception as e:
        pytest.fail(f"Error en el pipeline: {str(e)}")

def test_load_model(hydra_cfg):
    # Prueba de carga de modelo
    try:
        model = load_model(hydra_cfg)
        assert model is not None, "El modelo no se ha cargado correctamente"
    except Exception as e:
        pytest.fail(f"Error al cargar el modelo: {str(e)}")

def test_predict_endpoint(hydra_cfg):
    # Datos de entrada para el endpoint predict
    payload = {
        "claim_id": 1,
        "marca_vehiculo": "ford",
        "antiguedad_vehiculo": 5,
        "tipo_poliza": 2,
        "taller": 1,
        "partes_a_reparar": 3,
        "partes_a_reemplazar": 1
    }

    response = client.post("/api/v1/predict/", json=payload)
    assert response.status_code == 200, "La respuesta del endpoint debe ser 200 OK"
    json_data = response.json()
    assert "prediccion" in json_data, "La respuesta debe contener el campo 'prediccion'"
