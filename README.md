# HDI Challenge

This repository contains the code for the HDI challenge solution.

## To-do

- [X] Verify column format
- [X] Implement null value imputation
- [X] Apply the imputation dictionary
- [X] Build the preprocessing pipeline
- [X] Implement special condition for type 4 policies
- [X] Ensure features match training format
- [X] Pass preprocessed data to the predictive model
- [X] Get prediction in weeks
- [X] Validate results for different types of policies
- [X] Integrate stress tests for the API
- [X] Perform input case tests
- [X] Document the process
- [X] Implement logging for error handling

## Installation

Follow these steps to install and run the application in your local environment:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/jarb29/hdi-reto
   ```

2. Navigate to the project directory:
   ```bash
   cd desafio-hdi
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `.\env\Scripts\activate`
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the main script to start the application:
   ```bash
   uvicorn api.main:app --reload
   ```

## Usage

The application will run on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

To test the API, you can use the file `data/claims_dataset.csv` as input.

## Documentation

You can access the full project documentation [here](https://github.com/jarb29/hdi-reto).

## Dockerfile

The `Dockerfile` is used to create a Docker container for your FastAPI application. Below is a breakdown of each command:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

# upgrade and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements/requirements.txt

ENV HOST="0.0.0.0" \
    PORT="8000" \
    CONFIG_PATH="../config"

EXPOSE ${PORT}

# run the app
CMD ["uvicorn", "api.main:app", "--host", "${HOST}", "--port", "${PORT}"]
```

### Explanation

- **Base Image**: Use the slim variant of Python 3.11.
- **Working Directory**: Set the working directory inside the container to `/app`.
- **Copy Files**: Copy all files from the current directory to `/app`.
- **Upgrade and Install Dependencies**: Update package lists and install the necessary dependencies to build Python packages.
- **Python Dependencies**: Install Python dependencies from `requirements.txt`.
- **Environment Variables**: Set environment variables for the host, port, and config path.
- **Expose Port**: Expose port 8000 for the application.
- **Run Command**: Run the Uvicorn server, loading the FastAPI application from `api.main:app`.

## docker-compose.yml

The `docker-compose.yml` file is used to manage multi-container Docker applications.

```yaml
services:
  app:
    container_name: HDI-Challenge
    image: jarb29/hdi-challenge:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      HOST: "0.0.0.0"
      PORT: "8000"
    command: >
      uvicorn api.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}
```

### Explanation

- **Service Definition**: Define a service named `app`.
- **Container Name**: Name the container `HDI-Challenge`.
- **Image**: Specify the Docker image to use.
- **Build Context**: Define the build context and Dockerfile location.
- **Ports**: Map port `8000` on the host to port `8000` in the container.
- **Environment Variables**: Set environment variables for the application.
- **Command**: Specify the command to run the Uvicorn server.

## Makefile

The `Makefile` provides convenient shortcuts for building, deploying, and stopping Docker containers.

```makefile
build: ## Build the Docker image
	docker-compose up --build

deploy: build ## Deploy the app to the server
	docker-compose up -d

deploy-stop: ## Stop the app from the server
	docker-compose down
```

### Explanation

- **build**:
    - **Command**: `docker-compose up --build`
    - **Description**: Builds the Docker image and starts the container.

- **deploy**:
    - **Command**: `docker-compose up -d`
    - **Description**: First runs the `build` target, then deploys the application in detached mode.

- **deploy-stop**:
    - **Command**: `docker-compose down`
    - **Description**: Stops and removes containers, networks, and volumes associated with the Docker Compose project.

## Using Docker

### Build the Docker Image

Run the following command to build the Docker image:

```bash
make build
```

### Deploy the Application

Run the following command to deploy the application:

```bash
make deploy
```

### Stop the Application

Run the following command to stop the application:

```bash
make deploy-stop
```

## Endpoints

### Prediction
- **`POST /api/v1/predict`**: Generates a prediction for the received records.

  **Body**:
  ```json
  {
    "claims": [
      {
        "claim_id": "1",
        "policy_type": "4",
        "incident_date": "2023-01-01",
        "claim_amount": 5000.00,
        ...
      },
      ...
    ]
  }
  ```
  **Response**:
  ```json
  {
    "prediction": [
      {
        "claim_id": "1",
        "predicted_weeks": 6
      },
      ...
    ]
  }
  ```

## License

This project is under the MIT License. See the `LICENSE` file for more details.

## Contact

If you have any questions or suggestions, feel free to contact me via [my LinkedIn profile](https://www.linkedin.com/in/jarb29/).