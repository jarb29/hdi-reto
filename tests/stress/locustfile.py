from locust import HttpUser, TaskSet, task, between

class PredictTaskSet(TaskSet):

    @task
    def predict(self):

        payload = {
            "claim_id": 1,
            "marca_vehiculo": "ford",
            "antiguedad_vehiculo": 5,
            "tipo_poliza": 2,
            "taller": 1,
            "partes_a_reparar": 3,
            "partes_a_reemplazar": 1
        }

        response = self.client.post("/api/v1/predict/", json=payload)

        assert response.status_code == 200, f"Error: {response.status_code}"


class PredictTestUser(HttpUser):
    tasks = [PredictTaskSet]
    wait_time = between(1, 5)
