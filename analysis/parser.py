import re


def parse_insights_and_prepare_output(insight_text: str, report_dict, df) -> dict:
    # Analisa o texto/JSON gerado pelo modelo LLM e prepara a estrutura final que será
    # enviada ao frontend

    # - Extrai blocos de texto com: pontos positivos, negativos, sugestões e conclusão
    # - Sugere tipos de gráficos com base nas colunas do DataFrame
    # - Retorna um dicionário pronto para consumo no frontend

    # Expressões regulares para capturar os blocos de texto
    patterns = {
        "positives": r"(?i)(?:pontos?\s+)?positivos?:?\s*(.+?)(?=\n\s*(?:negativos?|sugest(ões|ões de melhoria)|conclusão|$))",
        "negatives": r"(?i)(?:pontos?\s+)?negativos?:?\s*(.+?)(?=\n\s*(?:sugest(ões|ões de melhoria)|conclusão|$))",
        "suggestions": r"(?i)sugest(ões|ões de melhoria):?\s*(.+?)(?=\n\s*(?:conclusão|$))",
        "conclusion": r"(?i)conclusão:?\s*(.+)",
    }

    insights = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, insight_text, re.DOTALL)

        if match:
            insights[key] = match.group(1).strip()
        else:
            insights[key] = "Não Identificado"

    # Sugestões de gráficos com base nas colunas
    numeric_columns = df.select_dtypes(
        include=["int64", "float64", "number"]
    ).columns.tolist()
    chart_suggestions = []

    if len(numeric_columns) >= 2:
        chart_suggestions.extend(["bar", "line", "scatter"])
    elif len(numeric_columns) == 1:
        chart_suggestions.append("bar")

    return {
        "insights": insights,
        "chartSuggestions": chart_suggestions,
        "chartData": report_dict,
        "columns": df.coilumns.tolist(),
    }
