import pandas as pd
from flask import jsonify


def validate_file(file):
    try:
        # Mensagem padrão de sucesso
        message = "Upload e validação realizados com sucesso!"

        df = pd.read_csv(file)

        if df.empty:
            return jsonify(
                {
                    "error": "O arquivo CSV está vazio ou contém apenas cabeçaldhos sem dados!"
                }
            ), 400

        # Verifica colunas sem nome ou dados
        invalid_columns = []

        for idx, col in enumerate(
            df.columns, start=1
        ):  # Começa o índice a partir de 1 para o usuário
            # Verifica se a coluna está sem nome, é "Unnamed:" ou contém apenas NaNs
            if not col or col.startswith("Unnamed:") or df[col].isnull().all():
                # Adiciona uma mensagem indicando a posição e o problema da coluna
                invalid_columns.append(f"Coluna {idx}")

        if invalid_columns:
            return jsonify(
                {
                    "error": "As seguintes colunas estão sem nome ou sem dados:",
                    "invalid_columns": invalid_columns,
                }
            ), 400

        return jsonify({"message": message}), 200

    # Captura erros de parsing do pandas
    except pd.errors.ParserError:
        return jsonify(
            {
                "error": "O arquivo CSV está vazio! Por favor, forneça um arquivo com dados."
            }
        ), 400

    # Captura erros de valor ou de tipo de dados
    except (ValueError, TypeError):
        return jsonify(
            {
                "error": "O arquivo CSV está vazio! Por favor, forneça um arquivo com dados."
            }
        ), 400

    # Fallback genérico para exceções inesperadas
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


def process_csv(file):
    try:
        # Leitura do arquivo CSV
        df = pd.read_csv(file)

        # Validação de Colunas
        # if 'colunas' not in df.co

        return df

    except Exception as e:
        raise e
