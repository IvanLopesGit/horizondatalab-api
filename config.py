import logging
import os

from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()  # Carrega o arquivo .env (Variáveis de Ambiente)

# Configuração do logger
logging.basicConfig(level=logging.INFO)


class Config:
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")


def authenticate_huggingface():
    # Autentica no Hugging Face usando o token armazenado na variáveld e ambiente

    token = Config.HF_TOKEN

    print("Token carregado no config:", Config.HF_TOKEN)

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
