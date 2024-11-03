from modules.logger_manager import get_logger

def null_imputation(df, imputation_dict):
    """Imputa nulos en los datos.

    Args:
        df (DataFrame): Dataframe con datos a imputar.
        imputation_dict (dict): Diccionario con columnas y valores para imputar nulos.

    Returns:
        DataFrame: Dataframe con nulos imputados.
    """
    logger = get_logger()

    for column, value in imputation_dict.items():
        df[column] = df[column].fillna(value)

    logger.info("Valores nulos imputados.")
    return df
