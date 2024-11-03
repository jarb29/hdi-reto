from pydantic import BaseModel


class TrainModelRequest(BaseModel):
    param1: float
    param2: float
    model_path: str

    class Config:
        protected_namespaces = ()
