import json

import pandas as pd
from ydata_profiling import ProfileReport


def identify_columns(df):
    # Identifica e categoriza as colunas do DataFrame
    # com base em seus tipos e sugere análise e gráficos

    # Args:
    # df(DataFrame): O DataFrame carregado e, preferencialmente, limpo

    # Returns:
    # dict: Um dicionário com informações das colunas categorizadas:

    try:
        # Inicialização das estruturas de saída
        columns_info = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
            "boolean": [],
            "null_columns": [],
            "constant_columns": [],
            "missing_values": {},
            "duplicates": 0,
        }

        # Conta valores ausentes por coluna
        columns_info["missing_values"] = df.isnull().sum().to_dict()

        # Conta número de linhas duplicadas no DataFrame
        columns_info["duplicates"] = df.duplicated().sum()

        # Verifica cada coluna e classifica
        for col in df.columns:
            # Verifica se a coluna é nula ou inválida
            if df[col].isnull().all():
                columns_info["null_columns"].append(col)

            # Verifica se a coluna é constante
            elif df[col].nunique() == 1:
                columns_info["constant_columns"].append(col)

            # Classifica se a coluna é numérica
            elif pd.api.types.is_numeric_dtype(df[col]):
                columns_info["numeric"].append(col)

            # Classifica se a coluna é categorica
            elif (
                pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == "object"
            ):
                columns_info["categorical"].append(col)

            # Classifica se a coluna é datetime
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                columns_info["datetime"].append(col)

            # Classifica se a coluna é booleana
            elif pd.api.types.is_bool_dtype(df[col]):
                columns_info["boolean"].append(col)

        return columns_info

    except Exception as e:
        raise ValueError(f"Erro na identificação de colunas: {str(e)}") from e


def generate_profile_report(df):
    # Gera um relatório do YData Profiling para explorar os dados

    # Args:
    # df(DataFrame): O Dataframe carregado
    # output_path(str): Caminho para salvar o relatório em HTML

    # Returns:
    # str: Caminho para o relatório gerado

    try:
        profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

        # Converte para json e depois para dict
        report_json = profile.to_json()
        report_dict = json.loads(report_json)
        return report_dict

    except Exception as e:
        raise ValueError(f"Erro na geração do relatório: {str(e)}") from e


def process_dataframe(df):
    # Realiza todas as etapas de identificação e análise automática em um DataFrame

    # Args:
    # df(DataFrame): O DataFrame carregado
    # pandas_profile_path (str): Caminho para salvar o relatório do Pandas Profiling

    # Returns:
    # dict: Informações sobre as colunas e sugestões de análise

    try:
        # Etapa 1: Identificar as colunas
        columns_info = identify_columns(df)

        # Etapa 2: Gerar relatório do Pandas Profiling
        profile_path = generate_profile_report(df)

        # Retorno consolidado
        return {
            "columns_info": columns_info,
            "pandas_profile_repot": profile_path,
        }

    except Exception as e:
        raise ValueError(f"Erro no processamento do DataFrame: {str(e)}") from e
