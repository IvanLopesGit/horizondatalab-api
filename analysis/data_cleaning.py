from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Trata valores ausentes no DataFrame substituindo por valores adequados

    try:
        for column in df.columns:
            if df[column].isnull().sum() > 0:
                if df[column].dtype in [np.float64, np.int64]:
                    df[column].fillna(df[column].mean(), inplace=True)
                elif df[column].dtype == "object":
                    df[column].fillna(df[column].mode()[0], inplace=True)
                elif pd.api.types.is_datetime64_any_dtype(df[column]):
                    df[column].fillna(df[column].median(), inplace=True)
                elif pd.api.types.is_bool_dtype(df[column]):
                    df[column].fillna(False, inplace=True)
        return df
    except Exception as e:
        raise ValueError(f"Erro ao lidar com valores ausentes: {str(e)}") from e


def detect_outliers(df: pd.DataFrame) -> pd.DataFrame:
    # Identifica e trata outliers em colunas numéricas

    try:
        numeric_columns = df.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            df[column] = np.where(
                (df[column] < lower_bound) | (df[column] > upper_bound),
                np.nan,
                df[column],
            )
        df = handle_missing_values(df)
        return df
    except Exception as e:
        raise ValueError(f"Erro ao detectar e tratar outliers: {str(e)}") from e


def normalize_and_scale(df: pd.DataFrame) -> pd.DataFrame:
    # Normaliza e escala colunas numéricas

    try:
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        scaler = StandardScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

        return df
    except Exception as e:
        raise ValueError(f"Erro ao normalizar e escalar colunas: {str(e)}") from e


def handle_duplicatres(df: pd.DataFrame) -> pd.DataFrame:
    # Remove colunas com conteúdo duplicado do DataFrame

    # Args:
    # df (pd.DataFrame): O DataFrame original

    # Returns:
    # pd.DataFrame: O DataFrame sem colunas duplicatas

    try:
        df = df.loc[:, ~df.T.duplicated(keep="first")]  # Remove colunas duplicadas
        return df
    except Exception as e:
        raise ValueError(f"Erro ao remover colunas duplicadas: {str(e)}") from e


def clean_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    # Realiza todo o processo de limpeza de dados

    # Args:
    # df (pd.DataFrame): O DataFrame a ser limpo

    # Returns:
    # Tuple[pd.DataFrame, dict]: O DataFrame limpo e um relatório(dicionário) de limpeza

    try:
        # Detectar e tratar colunas duplicadas
        df = handle_duplicatres(df)

        # Resolver valores ausentes
        df = handle_missing_values(df)

        # Detectar e tratar outliers
        df = detect_outliers(df)

        # Normalizar e escalar dados
        df = normalize_and_scale(df)

        return df

    except Exception as e:
        raise ValueError(f"Erro ao limpar os dados do DataFrame: {str(e)}") from e
