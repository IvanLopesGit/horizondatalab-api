import numpy as np
import pandas as pd


def check_dataframe(df: pd.DataFrame) -> dict:
    # Verifica problemas básicos no DataFrame

    # Args:
    # df (pd.DataFrame): O dataframe a ser analisado

    # Returns:
    # dict: Um dicionário contendo informações sobre os problemas identificados

    try:        
        issues = {
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=["object"]).columns.tolist(),
            "datetime_columns": df.select_dtypes(include=["datetime"]).columns.tolist(),
            "boolean_columns": df.select_dtypes(include=["bool"]).columns.tolist(),
            "null_columns": [col for col in df.columns if df[col].isnull().all()],
        }

        return issues
    except Exception as e:
        raise ValueError(f"Erro ao verificar o DataFrame: {str(e)}") from e

def identify_problemns_and_suggestions(issues):
    # Identifica problemas no DataFrame e sugere possíveis soluções.
    
    # Args: 
        # issue (dict): Dicionário contendo informações sobre os problemas identificados
    
    # Returns
        # list: Lista de dicionário com problemas e sugestões de solução
