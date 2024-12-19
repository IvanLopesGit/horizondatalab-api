import lux
import pandas as pd
from pandas_profiling import ProfileReport


def identify_columns(df):
    # Identifica e categoriza as colunas do DataFrame
    # com base em seus tipos e sugere análise e gráficos

    # Args:
    # df(DataFrame): O DataFrame carregado

    # Returns:
    # dict: Um dicionário com informações das colunas categorizadas
    # (nome, tipo, sugestão de análise e gráfico)

    try:
        # Inicialização das estruturas de saída
        columns_info = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
            "boolean": [],
            "null_columns": [],
        }

        # Verifica cada coluna e classifica
        for col in df.columns:
            # Verifica se a coluna é nula ou inválida

            if df[col].isnull().all():
                columns_info["null_columns"].append(col)

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


def generate_pandas_profile(df, output_path="report.html"):
    # Gera um relatório do Pandas Profiling para explorar os dados

    # Args:
    # df(DataFrame): O Dataframe carregado
    # output_path(str): Caminho para salvar o relatório em HTML

    # Returns:
    # str: Caminho para o relatório gerado

    try:
        profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
        profile.to_file(output_path)
        return output_path

    except Exception as e:
        raise ValueError(f"Erro na geração do relatório: {str(e)}") from e


def suggest_lux_charts(df):
    # Gera sugestões de gráficos usando Lux

    # Args:
    # df(DataFrame): P Dataframe carregado

    # Returns:
    # dict: Dicionário com os gráficos sugeridos pelo Lux

    try:
        # Ativa o modo de sugestão do Lux
        lux.config.default_display = "lux"

        # Coleta as sugestões
        recommendations = df.recommendation

        if not recommendations:
            raise ValueError("Nenhuma sugestão de gráfico disponível.")

        suggested_charts = {}

        for action, charts in recommendations.items():
            suggested_charts[action] = [
                {
                    "description": viz.description,
                    "columns": [str(intent) for intent in viz.intent],
                }
                for viz in charts
            ]

        return suggested_charts

    except Exception as e:
        raise ValueError(f"Erro na sugestão de gráficos: {str(e)}") from e


def process_dataframe(df, pandas_profile_path="report.html"):
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
        profile_path = generate_pandas_profile(df, output_path=pandas_profile_path)

        # Etapa 3: Sugerir gráficos com lux
        chart_suggestions = suggest_lux_charts(df)

        # Retorno consolidado
        return {
            "columns_info": columns_info,
            "pandas_profile_repot": profile_path,
            "lux_chart_suggestion": chart_suggestions,
        }

    except Exception as e:
        raise ValueError(f"Erro no processamento do DataFrame: {str(e)}") from e
