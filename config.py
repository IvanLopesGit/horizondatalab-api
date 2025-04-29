import logging
import os

from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()  # Carrega o arquivo .env (Variáveis de Ambiente)

# Chave obrigatória para acesso à API do Hugging Face
HUGGINGFACE_API_KEY = os.environ["HUGGINGFACE_API_KEY"]

# Ambiente atual (development, QA, production)
ENVIRONMENT = os.environ["ENVIRONMENT"]

# Modelos de Linguagem(LLM)
LLAMA_MODEL_NAME_DEV = os.environ["LLAMA_MODEL_NAME_DEV"]
LLAMA_MODEL_NAME_PROD = os.environ["LLAMA_MODEL_NAME_PROD"]


# Função para obter o nome do modelo LLM com base no ambiente
def get_llama_model_name():
    if ENVIRONMENT == "development":
        return LLAMA_MODEL_NAME_DEV
    elif ENVIRONMENT == "production":
        return LLAMA_MODEL_NAME_PROD
    else:
        raise ValueError("Ambiente não reconhecido")


# Configuração do logger
logging.basicConfig(level=logging.INFO)


def authenticate_huggingface():
    # Autentica no Hugging Face usando o token armazenado na variáveld e ambiente

    token = HUGGINGFACE_API_KEY

    if not token:
        logging.error(
            "Token não encontrado, configure a variável de ambiente HUGGINGFACE_TOKEN."
        )
        raise ValueError("Token do Hugging Face não encontrado")

    try:
        login(token=token)
        logging.info("Autenticação no Hugging Face bem-sucedida.")
    except Exception as e:
        logging.error("Erro na autenticação no Hugging Face: %s", e)
        raise
