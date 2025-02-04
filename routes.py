from flask import Blueprint, jsonify, request

from analysis.data_cleaning import clean_data
from analysis.identifier import process_dataframe
from analysis.loader import load_data, validate_data

# Criação do blueprint
routes = Blueprint("routes", __name__)

# Mapeamento de colunas
COLUMN_MAPPINGS = {
    "sales": ["sales", "vendas", "venda", "sale"],
    "stock": ["stock", "inventory", "estoque"],
    "product": ["product", "item", "produto"],
}


@routes.route("/process", methods=["POST"])
def process_file():
    # Processa o arquivo enviado pelo usuário, tentando identificar automaticamente
    # as colunas e os gráficos possíveis.

    try:
        # Verificar se o arquivo foi enviado
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        # Etapa 1: Carregar e validar o arquivo
        file = request.files["file"]
        df, error = load_data(file)

        if error:
            return jsonify({"error": error}), 400

        validation_response, status_code = validate_data(df)

        if status_code != 200:
            return validation_response, status_code

        # Etapa 2: Limpeza e preparação dos dados
        df_cleaned = clean_data(df)

        # Etapa 3: Identificar colunas, gerar relatórios e sugerir gráficos
        process_result = process_dataframe(df_cleaned)

        # Se não houver sugestões de gráficos, retornamos para o usuário selecionar
        if not process_result.get("lux_chart_suggestion"):
            return jsonify(
                {
                    "message": "Nenhum gráfico identificado automaticamente",
                    "available_columns": df_cleaned.columns.tolist(),
                }
            )

        # Etapa 4: Realizar análise detalhada com base nos gráficos e problemas identificados
        analysis_result = process_analysis(process_result)

        # Etapa 5: Retornar os resultados consolidados
        return jsonify(
            {
                "message": "Arquivo processado com sucesso",
                "data": analysis_result,
            }
        )

    except Exception as e:
        return jsonify(
            {"error": f"Erro durante o processamento do arquivo: {str(e)}"}
        ), 500


def process_analysis(process_result):
    # Processa as análises com base nos gráficos identificados e informações das colunas

    # Args:
    # df (DataFrame): DataFrame limpo e validado
    # process_result (dict): Resultado do processamento inicial contendo colunas, relatórios e sugestões

    # Returns:
    # dict: Insights, problemas e sugestões baseados nas análises realizadas

    try:
        # Informações básicas das colunas (já obtidas no process_dataframe)
        columns_info = process_result.get("columns_info", {})

        # Sugestões de gráficos do Lux (já obtidas no process_dataframe)
        lux_suggestions = process_result.get("lux_chart_suggestions", {})

        # Consolidar os resultados
        return {
            "message": "Análise realizadas com sucesso",
            "columns": columns_info,
            "graph_suggestions": lux_suggestions,
        }

    except Exception as e:
        raise ValueError(f"Erro no processamento das análises: {str(e)}") from e
