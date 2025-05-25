from dotenv import load_dotenv
import os

load_dotenv()

PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")
PIPEFY_API_URL = os.getenv("PIPEFY_API_URL")
