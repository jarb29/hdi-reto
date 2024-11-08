# Stress Tests

This document provides details on the stress testing strategy for the HDI Claims Prediction API, evaluating its performance and stability under high load.

---

## Tool

We use **Locust** for stress testing. Locust is an open-source load testing tool that simulates many concurrent users by defining user behavior.

---

## Test Scenarios

Stress test scenarios are defined in `tests/stress/locustfile.py`. This script simulates user behavior, such as sending requests to the `/api/v1/predict/` endpoint.

### Locust File (`test/stress/locustfile.py`)

```python
from locust import HttpUser, TaskSet, task, between
import logging
from random import randint
import time

class PredictTaskSet(TaskSet):

    def on_start(self):
        """ This method is called when a simulated user starts """
        logging.info("Starting a new simulated user session.")
    
    @task
    def predict(self):
        payload = {
            "claim_id": randint(1, 100),
            "marca_vehiculo": "ford",
            "antiguedad_vehiculo": randint(1, 10),
            "tipo_poliza": randint(1, 3),
            "taller": randint(1, 2),
            "partes_a_reparar": randint(1, 5),
            "partes_a_reemplazar": randint(0, 3)
        }

        start_time = time.time()
        response = self.client.post("/api/v1/predict/", json=payload)
        end_time = time.time()

        response_time = end_time - start_time

        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}, Response: {response.text}")
        else:
            logging.info(f"Response time: {response_time:.2f} seconds")

        assert response.status_code == 200, f"Error: {response.status_code}"

    def on_stop(self):
        """ This method is called when a simulated user stops """
        logging.info("Stopping the simulated user session.")

class PredictTestUser(HttpUser):
    tasks = [PredictTaskSet]
    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000"  # Adjust host as necessary
```

---

## Running Stress Tests

1. **Start the API Server**
   - Ensure the API server is running (e.g., `make run`).

2. **Execute Locust**
    ```bash
    make stress-tests
    ```
   - This starts Locust and opens a web interface at [http://127.0.0.1:8089](http://127.0.0.1:8089).

3. **Configure and Run**
   - In the Locust UI, set the number of users and hatch rate. Start the test to simulate traffic.

---

## Results and Analysis

Locust provides charts and reports on the requests per second (RPS), response times, and failures. Analyze these results to identify bottlenecks under high load.

### Example Results

Example results are detailed below. These are located in `tests/stress/results/results.md`.

# Stress Test Results Analysis

## Requests per Second (RPS)

- The "Total Requests per Second" chart shows a request rate of around 0.6 RPS. This suggests that the system is continuously managing requests, although the rate isn't very high.
- For a stress test, this could indicate slow request processing speeds, possibly due to the workload or the capacity of the model running on the endpoint.

![Total Requests per Second](images/C1.png)

## Response Times

- The "Response Times" chart shows high response times, with an average of around 12064 ms and a similar median, indicating most requests take over 12 seconds to process.
- The minimum recorded time is 12064 ms, while the maximum reaches 12369 ms. This suggests consistent latency, possibly due to heavy models and processing pipelines taking considerable time to complete.
- High latency could be an area for improvement since lower response times are preferable in production applications to provide an adequate user experience.

![Response Times](images/C2.png)

## Concurrent Users

- In the "Number of Users" chart, the number of users remains steady at 10. This was the peak number of concurrent users configured during the test, and the system was able to handle this load without response errors (failures).
- The fact that the system can support 10 users without failures is positive, but the high latency indicates it might not scale well with a much larger number of concurrent users.

## Tabular Summary

- In the results table, we observe that a total of 117 requests were made, and none failed. This is positive and shows that the endpoint is robust in handling requests without errors.
- The average response size is 32 bytes, which is low, suggesting that the response probably only contains the prediction result and no additional data.