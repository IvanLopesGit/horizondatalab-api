import pandas as pd
from flask import Flask, jsonify, request

from analysis.identifier import process_dataframe


# Função para carregar o arquivo CSV
def load_data(file):
    # Carrega o arquivo CSV.

    try:
        # Verifica se o arquivo tem a extensão .csv
        if not file.filename.endswith(".csv"):
            return jsonify({"error": "O arquivo deve estar com a extensão .csv"}), 400

        # Tenta carregar o arquivo como DataFrame
        df = pd.read_csv(file)

        return df, None  # Retorna o Dataframe e nenhum erro

    except pd.errors.ParserError:
        return jsonify(
            {
                "error": "Erro ao processar o CSV. O arquivo pode estar vazio ou mal formatado"
            }
        ), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


# Função para validar o DataFrame carregado
def validate_data(df):
    # Validações básicas no DataFrame

    try:
        # Mensagem padrão de sucesso
        message = "Upload e validações do arquivo realizados com sucesso!"

        if df.empty:
            return jsonify(
                {"error": "O arquivo está vazio ou contém apenas cabeçalhos sem dados!"}
            ), 400

        # Verifica colunas sem nome ou dados
        invalid_columns = []
        for idx, col in enumerate(df.columns, start=1):
            if not col or col.startswith("Unnamed") or df[col].isnull().all():
                invalid_columns.append(
                    f"Coluna: {idx}"
                )  # Índice inicia em 1 para o usuário

        if invalid_columns:
            return jsonify(
                {
                    "error": "As seguintes colunas estão sem nome ou sem dados:",
                    "invalid_columns": invalid_columns,
                }
            ), 400

        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"error": f"Erro inesperado na validação: {str(e)}"}), 500


# Pipeline inicial[=]
if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]

        # Passo 1: Carregar o arquivo
        df, error = load_data(file)
        if error:
            return jsonify({"error": error}), 400

        # Passo 2: Validar os dados
        validation_response, status_code = validate_data(df)

        if status_code != 200:
            return validation_response, status_code

        # Passo 3: Identificar colunas e sugerir gráficos
        try:
            analysis_result = process_dataframe(df)
            return jsonify(
                {
                    "message": "Arquivo processado com sucesso",
                    "analysis": analysis_result,
                }
            ), 200

        except Exception as e:
            return jsonify(
                {
                    "error": f"Erro durante a análise de identificação de colunas e gráficos: {str(e)}"
                }
            ), 500

    app.run(debug=True)
