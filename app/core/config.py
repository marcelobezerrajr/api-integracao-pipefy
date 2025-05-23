from dotenv import load_dotenv
import os

load_dotenv()

PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")
PIPEFY_API_URL = os.getenv("PIPEFY_API_URL")
PIPE_ID = int(os.getenv("PIPE_ID"))
FINAL_PHASE_ID = os.getenv("FINAL_PHASE_ID")
