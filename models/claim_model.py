from pydantic import BaseModel


class Claim(BaseModel):
    claim_id: int
    marca_vehiculo: str
    antiguedad_vehiculo: int
    tipo_poliza: int
    taller: int
    partes_a_reparar: int
    partes_a_reemplazar: int
