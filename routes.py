from flask import Blueprint, jsonify, request

from analysis.data_cleaning import clean_data

# Importa a função de identificação e funções do AI Agent
from analysis.identifier import generate_profile_report, process_dataframe

# Funções de processamento
from analysis.loader import load_data, validate_data
from utils import convert_numpy

# Criação do blueprint
routes = Blueprint("routes", __name__)


@routes.route("/process", methods=["POST"])
def process_file():
    # Endpoint que processa o arquivo CSV enviado pelo usuário:
    # 1. Carrega, valida e elimpa o arquivo.
    # 2. Gera o relatório via ydata-profiling.
    # 3. Gera o insight automatizado usando AI Agent (LangChain).
    # 4. Consolida as informações e retorna o JSON para o frontend.
    # - 'chartData': dados para renderização dos gráficos.
    # - 'insightText': texto gerado com a análise.
    # - 'columns': lista de colunas do DataFRame limpa.

    try:
        # Verifica se o arquivo foi enviado
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
        process_result = process_dataframe(df_cleaned)
        columns_info = process_result.get("columns_info", df_cleaned.columns.tolist())

        # Etapa 3: Gerar relatório via ydata-profiling
        report_dict = generate_profile_report(df_cleaned)

        # Etapa 4: Gerar o insight automatizado usando AI Agent(LangChain)
        # insight_text = generate_insight_with_agent(report_dict)

        # Etapa 5: Monta e retorna a resposta para o frontend

        analysis_result = {
            "chartData": convert_numpy(report_dict),
            # "insightText": insight_text,
            "colums": convert_numpy(columns_info),
        }

        return jsonify(
            {
                "message": "Arquivo processado com sucesso",
                "data": analysis_result,
            }
        )

    except Exception as e:
        # print("erro detectado", str(e))

        # import traceback

        # traceback.print_exc()
        return jsonify(
            {"error": f"Erro durante o processamento do arquivo: {str(e)}"}
        ), 500
