"""
Este módulo define uma API usando Flask para processar dados CSV,
analisar e gerar gráficos interativos.

Funções:
- recieve_data: Recebe um arquivo CSV e retorna um DataFrame.
- analyse_data: Realiza uma análise básica dos dados e retorna um dicionário com os resultados.
- generate_graph: Gera um gráfico interativo e retorna o HTML do gráfico.
- process_data: Endpoint para processar os dados recebidos na solicitação POST.

ativar o ambiente -> source data-analysis-api/Scripts/activate
rodar o codigo
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from utils import validate_file

data_analysis = Flask(__name__)

CORS(data_analysis, resources={r"/upload_csv": {"origins": "http://localhost:4200"}})


# def analyse_data(df):
#     # Análise de dados
#     first_column = df.columns[0]  # Pega o nome da primeira coluna para labels
#     second_column = df.columns[1]  # Pega o nome da segunda coluna para values

#     # Supondo que a primeira coluna seja labels e a segunda seja values
#     labels = df[
#         first_column
#     ].tolist()  # Converte a primeira coluna para uma lista (labels)
#     values = df[
#         second_column
#     ].tolist()  # Converte a segunda coluna para uma lista (values)

#     # Montar os dados para o gráfico
#     analysed_data = {
#         "labels": labels,
#         "values": values,
#         "label_column": first_column,  # Nome da coluna de labels
#         "value_column": second_column,  # Nome da coluna de valores
#     }

#     return analysed_data


# def generate_graph(df):
#     # Exemplo de gráfico de linhas
#     trace = go.Scatter(
#         x=df["Coluna_X"],  # Substitua pela sua coluna X
#         y=df["Coluna_Y"],  # Substitua pela sua coluna Y
#         mode="lines+markers",
#     )

#     layout = go.Layout(
#         title="Título do Gráfico",
#         xaxis=dict(title="Eixo X"),
#         yaxis=dict(title="Eixo Y"),
#     )

#     return {"data": [trace], "layout": layout}


# @data_analysis.route("/process_data", methods=["POST"])
# def process_data():
#     # Receber o arquivo CSV enviado pelo frontend
#     file = request.files["file"]
#     df = pd.read_csv(file)

#     # Processar os dados
#     analysed_data = analyse_data(df)

#     return jsonify(analysed_data)


@data_analysis.route("/upload_csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    # Chamando a função validate_file para validar o CSV
    validation_response = validate_file(file)

    # Se a validação retornar um erro, retorna a resposta de erro
    # if isinstance(validation_response, tuple) and validation_response[1] != 200:
    #     return validation_response

    # Após a validação, processa o CSV e retorna a mensagem de sucesso
    # df = process_csv(file)  # Aqui será onde trabalharemos os dados
    # data_preview = df.head().to_dict()

    # return jsonify(
    #     {
    #         # "data_preview": data_preview,
    #         "message": "Upload e processamento realizados com sucesso!",
    #     }
    # ), 200

    return validation_response


if __name__ == "__main__":
    data_analysis.run(debug=True)
