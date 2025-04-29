import json

# Importação do Hugging Face Transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import authenticate_huggingface, get_llama_model_name

# Autenticação no Hugging Face
authenticate_huggingface()

# Inicializando o modelo e tokenizador do Hugging Face
MODEL_NAME = get_llama_model_name()

# Carrega o modelo e o tokenizaro do Hugging Face
# model = LlamaForCausalLM.from_pretrained(MODEL_NAME)
# tokenizer = LlamaTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def generate_insight_with_agent(report_dict: dict) -> str:
    # Obtém o overview do dicionário
    overview = report_dict.get("overview", {})

    # Converte o overview para uma string formatada (JSON) para o prompt
    overview_str = json.dumps(overview, indent=2, ensure_ascii=False)

    # Prompt com instrução clara ao modelo
    prompt = (
        "Você é um analista de dados. Com base no resumo a seguir, "
        "gere insights em Português do Brasil (pt-BR), incluindo pontos positivos, negativos e sugestões de melhoria.\n\n"
        f"Resumo dos dados:\n{overview_str}"
    )

    # Tokeniza a entrada para o LLaMA
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    # Geração de texto usando o modelo LLaMA
    outputs = model.generate(
        **inputs, max_new_tokens=1000, do_sample=True, temperature=0.7
    )

    # Decodifica a saída do modelo
    insight = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return insight.strip()
