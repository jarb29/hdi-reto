# HDI Claims Prediction API Documentation

Inspired by Swagger API docs style & structure

---

## Table of Contents
- [API Host Configuration](#api-host-configuration)
- [Root Endpoint](#root-endpoint)
- [Predict Claim](#predict-claim)
- [Train Model](#train-model)
- [Error Handling](#error-handling)
- [Data Preprocessing](#data-preprocessing)
- [Model](#model)

---

## API Host Configuration

The API is hosted on the following address:

- **Host:** `127.0.0.1`
- **Port:** `8000`

When making requests to the API, ensure that you use this base URL: `http://127.0.0.1:8000`

---

## Root Endpoint

<details>
 <summary><code>GET</code> <code><b>/</b></code> <code>(Check if the API is up and running)</code></summary>

### Description

This endpoint is used to check if the API server is running. If the server is up, it returns a welcome message.

### Parameters

None

### Responses

> | HTTP Code | Content-Type       | Response                                      |
> |-----------|--------------------|-----------------------------------------------|
> | `200`     | `application/json` | `{"message": "Bienvenido al API de predicción de siniestros de HDI"}` |

### Example cURL

```bash
curl -X GET http://127.0.0.1:8000/
```

</details>

---

## Predict Claim

<details>
 <summary><code>POST</code> <code><b>/api/v1/predict/</b></code> <code>(Predicts the repair time for a given claim)</code></summary>

### Description

This endpoint predicts the repair time for a given claim based on various parameters.

### Parameters

> | Name           | Type   | Data Type | Description       |
> |----------------|--------|-----------|-------------------|
> | (Request Body) |        | JSON      | See example below  |

### Request Body Example

```json
{
  "claim_id": 123,
  "marca_vehiculo": "Toyota",
  "antiguedad_vehiculo": 5,
  "tipo_poliza": 2,
  "taller": 10,
  "partes_a_reparar": 2,
  "partes_a_reemplazar": 1
}
```

### Responses

> | HTTP Code | Content-Type      | Response                                                                    |
> |-----------|-------------------|-----------------------------------------------------------------------------|
> | `200`     | `application/json`| ```json { "prediccion": 2.5 } ```                                            |
> | `400`     | `application/json`| `{"code":"400","message":"Bad Request"}`                                     |
> | `500`     | `application/json`| `{"code":"500","message":"Internal Server Error (See logs for details)"}`    |

### Example cURL

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "claim_id": 123,
  "marca_vehiculo": "Toyota",
  "antiguedad_vehiculo": 5,
  "tipo_poliza": 2,
  "taller": 10,
  "partes_a_reparar": 2,
  "partes_a_reemplazar": 1
}' http://127.0.0.1:8000/api/v1/predict/
```

### Special Condition

If `tipo_poliza` is 4, the prediction will always be -1.

</details>

---

## Train Model

<details>
 <summary><code>POST</code> <code><b>/api/v1/train/</b></code> <code>(Endpoint for training the model)</code></summary>

### Description

This endpoint allows for training the model using a provided dataset file.

### Parameters

> | Name | Type        | Data Type           | Description                      |
> |------|-------------|---------------------|----------------------------------|
> | file | binary file | `multipart/form-data` | The file to be used for training. |

### Responses

> | HTTP Code | Content-Type       | Response                                    |
> |-----------|--------------------|---------------------------------------------|
> | `200`     | `text/plain`       | "Training successful"                       |
> | `422`     | `application/json` | `{"code":"422", "message":"Validation Error"}` |

### Example cURL

```bash
curl -X POST -F "file=@/path/to/your/file.csv" http://127.0.0.1:8000/api/v1/train/
```

</details>

---

## Error Handling

See individual endpoint responses for specific error codes. Common codes include:

- **`400 Bad Request`:** The request was invalid or cannot be otherwise served.
- **`500 Internal Server Error`:** An error occurred on the server side.

---

## Data Preprocessing

A summary of the five-step preprocessing pipeline applied before prediction, including null imputation. See the code for details.

---

## Model

A linear regression model (`linear_regression.pkl`) is used to predict repair time based on preprocessed features.

---
