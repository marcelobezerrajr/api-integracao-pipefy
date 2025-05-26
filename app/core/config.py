from dotenv import load_dotenv
import os

load_dotenv()

PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")
PIPEFY_API_URL = os.getenv("PIPEFY_API_URL")

if not PIPEFY_TOKEN or not PIPEFY_API_URL:
    raise ValueError(
        "As variaveis de ambiente PIPEFY_TOKEN e PIPEFY_API_URL devem ser definidas."
    )
