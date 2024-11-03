import pandas as pd


def validate_columns_and_types(df):
    """Valida y convierte las columnas al tipo requerido antes de ejecutar el predict.

    Args:
        df (DataFrame): DataFrame con datos a validar y convertir.

    Returns:
        DataFrame: DataFrame con columnas convertidas al tipo requerido.
    """
    expected_columns = {
        'log_total_piezas': float,
        'marca_vehiculo_encoded': int,
        'valor_vehiculo': int,
        'valor_por_pieza': int,
        'antiguedad_vehiculo': int
    }

    try:
        for column, dtype in expected_columns.items():
            if column not in df.columns:
                raise ValueError(f"Falta la columna '{column}' en el DataFrame.")

            # Convertir la columna al tipo esperado si es diferente
            if not pd.api.types.is_dtype_equal(df[column].dtype, dtype):
                try:
                    df[column] = df[column].astype(dtype)
                except ValueError as e:
                    raise TypeError(f"No se pudo convertir la columna '{column}' al tipo {dtype}. Error: {str(e)}")

    except Exception as e:
        raise ValueError(f"Error al validar los datos: {e}")

    return df
