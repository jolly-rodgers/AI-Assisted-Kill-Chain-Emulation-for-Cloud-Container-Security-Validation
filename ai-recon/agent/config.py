import os

AI_RUNTIME = os.getenv("AI_RUNTIME", "ollama")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama.myserver.local:11434"
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
