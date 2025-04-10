# test_env.py
import os

from dotenv import load_dotenv

load_dotenv()

print("Token carregado:", os.getenv("HUGGINGFACE_TOKEN"))
